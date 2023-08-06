
class hasseb2(hid):
    """hasseb DALI Master based on NXP LPC11xx_LPC13xx with new firmware
    """
    # Commands sent to the interface
    _cmdtmpl = struct.Struct("B" * 10)
    # Magic number always sent and received in byte 0
    _CMD_MAGIC = 0xaa

    # Command codes sent in byte 0
    _CMD_NOOP = 0x00
    _CMD_READ_VERSION = 0x02
    _CMD_CONFIG_DEVICE = 0x05
    _CMD_SEND = 0x07

    # Responses received from the interface
    # Decodes to mode, response type, frame, interval, seq
    _resptmpl = struct.Struct("B" * 10)
    _RESP_MAGIC = 0xaa
    _RESP_NOOP = 0x00
    _RESP_READ_VERSION = 0x02
    _RESP_RECV = 0x07

    @staticmethod
    def _seqnum(i):
        """Sequence number generator
        """
        while True:
            yield i
            i += 1
            if i > 0xff:
                i = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log = self._log.getChild("hasseb2")

        # Initialise the command sequence number to a random value,
        # avoiding zero
        self._cmd_seq = iter(self._seqnum(random.randint(0x01, 0xff)))

        # Outstanding command events and message queues indexed by
        # sequence number
        self._outstanding = {}

        # Semaphore controlling number of outstanding commands
        self._command_semaphore = asyncio.BoundedSemaphore(2, loop=self.loop)

        # Bus watch task, event and message queue
        self._bus_watch_task = None
        self._bus_watch_data_available = asyncio.Event(loop=self.loop)
        self._bus_watch_data = []

    def _initialise_device(self):
        # Read firmware version; pick up the reply in _handle_read
        os.write(self._f, self._cmd(self._CMD_READ_VERSION))

    async def _send_raw(self, command):
        frame = command.frame
        if len(frame) != 16:
            raise UnsupportedFrameTypeError
        await self.connected.wait()
        async with self._command_semaphore:
            seq = next(self._cmd_seq)
            self._log.debug("Sending with seq %x", seq)
            event = asyncio.Event(loop=self.loop)
            messages = []
            # If seq is in self._outstanding this means we've wrapped
            # around the whole sequence number space with an event
            # still outstanding: clearly a bug!
            assert seq not in self._outstanding
            self._outstanding[seq] = (event, messages)
            frame = frame.pack_len(2)
            data = self._cmd(
                self._CMD_SEND, seq=seq, byte3=16,
                byte4=1 if command.response else 0,
                byte6=10 if command.sendtwice else 0,
                byte7=frame[0],
                byte8=frame[1])
            try:
                os.write(self._f, data)
            except OSError:
                # The device has failed.  Disconnect, schedule a
                # reconnection, and report this command as failed.
                self._log.debug("fail on transmit, disconnecting")
                self.disconnect(reconnect=True)
                raise CommunicationError

            outstanding_transmissions = 2 if command.sendtwice else 1
            response = None
            while outstanding_transmissions or response is None:
                if len(messages) == 0:
                    await event.wait()
                    event.clear()
                message = messages.pop(0)
                if message == "fail":
                    # The device has gone away, possibly in the middle of processing
                    # our command.
                    self._log.debug("processing queued fail on receive")
                    raise CommunicationError

                # The response type is guaranteed to be _RESP_RECV
                # and the sequence number will match
                magic, resptype, rseq, reptype, dlen, d0, d1, d2, \
                    byte8, byte9 = self._resptmpl.unpack(message)
                if reptype == 0x01:
                    # "No response received" - presumably this means
                    # transmission is complete?
                    outstanding_transmissions -= 1
                    response = "no"
                elif reptype == 0x02:
                    # "Response data received" - presumably this means
                    # transmission is complete and there was a response?
                    outstanding_transmissions -= 1
                    response = dali.frame.BackwardFrame(d2)
                elif reptype == 0x03:
                    # "Invalid data" - dunno, does this mean framing error
                    # on response?
                    outstanding_transmissions -= 1
                    response = dali.frame.BackwardFrameError(255)
                else:
                    self._log.debug("Unexpected report type %x", reptype)
                    response = "no"
            del self._outstanding[seq], event, messages
            if command.response:
                # Construct response and return it
                if response == "no":
                    return command.response(None)
                return command.response(response)

    async def _bus_watch(self):
        # Why is this a task, and not just run from _handle_read()?
        # It's so that when we see a forward frame on the bus that
        # didn't originate with us, we can apply a timeout after which
        # if we don't see another related frame (either a repeated
        # config command forward frame, or a backward frame) we can
        # assume there wasn't one.

        # Command awaiting repeat or reply
        current_command = None
        devicetype = 0

        while True:
            # Wait for data
            if len(self._bus_watch_data) == 0:
                if current_command:
                    self._log.debug("Bus watch waiting with timeout")
                    await asyncio.wait_for(self._bus_watch_data_available.wait(), 0.2)
                else:
                    self._log.debug("Bus watch waiting for data, no timeout")
                    await self._bus_watch_data_available.wait()
                self._bus_watch_data_available.clear()

            # Figure out why we've woken up
            if len(self._bus_watch_data) == 0:
                self._log.debug("bus_watch timeout")
                timeout = True
            else:
                timeout = False
                message = self._bus_watch_data.pop(0)
                self._log.debug("bus_watch message %s", _hex(message[0:9]))
                origin, rtype, raw_frame, interval, seq = self._resptmpl.unpack(message)
                if origin not in (self._MODE_OBSERVE, self._MODE_RESPONSE):
                    self._log.debug("bus_watch: unexpected packet mode, ignoring")
                    continue
                if rtype == self._RESPONSE_FORWARD_FRAME:
                    frame = dali.frame.ForwardFrame(16, raw_frame)
                elif rtype == self._RESPONSE_BACKWARD_FRAME:
                    frame = dali.frame.BackwardFrame(raw_frame)
                elif rtype == self._RESPONSE_NO_FRAME:
                    frame = "no"
                elif rtype == self._RESPONSE_BUS_STATUS \
                     and message[5] == self._BUS_STATUS_FRAMING_ERROR:
                    frame = dali.frame.BackwardFrameError(255)
                else:
                    # Probably a bus status message other than framing error
                    self._log.debug("bus_watch: ignoring packet")
                    continue

            # Resolve the current_command before considering anything else.
            if current_command:
                # current_command will be a config command or a
                # command that expects a response.  It cannot be
                # EnableDeviceType()
                if current_command.sendtwice:
                    # We are waiting for a repeat of the command
                    if timeout:
                        # We didn't get it: report a failed command
                        self._log.debug("Failed sendtwice command: %s", current_command)
                        self.bus_traffic._invoke(current_command, None, True)
                        current_command = None
                        continue
                    elif isinstance(frame, dali.frame.ForwardFrame):
                        # If frame matches command, it's a valid config command
                        if current_command.frame == frame:
                            self._log.debug("Config command: %s", current_command)
                            self.bus_traffic._invoke(current_command, None, False)
                            current_command = None
                            continue
                        else:
                            self._log.debug("Failed config command (second frame didn't match): %s", current_comment)
                            self.bus_traffic._invoke(current_command, None, True)
                            current_command = None
                            # Fall through to continue processing frame
                    elif isinstance(frame, dali.frame.BackwardFrame):
                        # Error: config commands don't get backward frames.
                        self._log.debug("Failed config command %s with backward frame",
                                        current_command)
                        self.bus_traffic._invoke(current_command, None, True)
                        current_command = None
                    else:
                        self._log.debug("Unexpected response waiting for retransmit of config command")
                elif current_command.response:
                    # We are waiting for a response
                    if timeout or frame == "no":
                        # The response is "No".
                        self._log.debug("Command %s response \'No\'", current_command)
                        self.bus_traffic._invoke(
                            current_command, current_command.response(None), False)
                        current_command = None
                        continue
                    elif isinstance(frame, dali.frame.BackwardFrame):
                        # There's a response
                        self._log.debug("Command %s response %s",
                                        current_command, current_command.response(frame))
                        self.bus_traffic._invoke(
                            current_command, current_command.response(frame), False)
                        current_command = None
                        continue
                    else:
                        # The response is "No" and we have a new frame to deal with;
                        # fall through to process it
                        self._log.debug("Command %s response \'No\' (on new frame)",
                                        current_command)
                        self.bus_traffic._invoke(
                            current_command, current_command.response(None), False)
                        current_command = None

            # If we reach here, there is no current_command and there
            # may still be a frame to process.
            assert current_command == None
            if timeout:
                pass
            elif isinstance(frame, dali.frame.ForwardFrame):
                command = dali.command.from_frame(frame, devicetype=devicetype)
                devicetype = 0
                if command.sendtwice or command.response:
                    # We need more information.  Stash the command and wait.
                    current_command = command
                else:
                    # We're good.  Report it.
                    self._log.debug("Command %s, immediate", command)
                    self.bus_traffic._invoke(command, None, False)
                if isinstance(command, EnableDeviceType):
                    devicetype = command.param
                    self._log.debug("remembering device type %s", devicetype)
            elif isinstance(frame, dali.frame.BackwardFrame):
                self._log.debug("Unexpected backward frame %s", frame)

    def _handle_read(self, data):
        self._log.debug("_handle_read %s", _hex(data[0:9]))
        if data[0] != self._RESP_MAGIC:
            self._log.debug("Bad magic number received")
            return
        if data[1] == self._RESP_NOOP:
            # No-op; ignore silently
            return
        if data[1] == self._RESP_READ_VERSION:
            if not self.firmware_version:
                self.firmware_version = f"{data[3]}.{data[4]}"
                self.connected.set()
                #self._bus_watch_task = asyncio.ensure_future(
                #    self._bus_watch(), loop=self.loop)
            else:
                self._log.debug("Unsolicited init command response")
            return
        if data[1] == self._RESP_RECV:
            #self._bus_watch_data.append(data)
            #self._bus_watch_data_available.set()
            seq = data[2]
            if seq in self._outstanding:
                event, messages = self._outstanding[seq]
                messages.append(data)
                event.set()
                del event, messages
            else:
                self._log.debug("Received data with unexpected seqnum %x",
                                data[2])
            return
        else:
            self._log.debug("Unknown response mode %x", data[1])

    def _shutdown_device(self):
        # All outstanding commands need to be woken up and told they've failed
        for event, messages in self._outstanding.values():
            messages.append("fail")
            event.set()
        self._outstanding_values = {}
        # Cancel the bus watch task
        if self._bus_watch_task is not None:
            self._bus_watch_task.cancel()
            self._bus_watch_task = None
        self._bus_watch_data_available.clear()
        self._bus_watch_data = []
        # Clear these so that we won't get confused when we reconnect
        self.firmware_version = None
        self.serial = None

    @classmethod
    def _cmd(cls, cmd, seq=0, byte3=0, byte4=0, byte5=0, byte6=0, byte7=0,
             byte8=0, byte9=0):
        """Return 64 bytes for the specified command
        """
        return cls._cmdtmpl.pack(
            cls._CMD_MAGIC, cmd, seq, byte3, byte4, byte5, byte6,
            byte7, byte8, byte9)
