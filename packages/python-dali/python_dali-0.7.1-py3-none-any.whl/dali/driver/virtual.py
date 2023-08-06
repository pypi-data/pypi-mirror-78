# async virtual device driver

# Useful for testing!

import asyncio
import os
import logging
import random
import glob
from dali.exceptions import UnsupportedFrameTypeError, CommunicationError
import dali.frame

# dali.command and dali.gear are required for the bus traffic callback
import dali.command
import dali.gear
from dali.gear.general import EnableDeviceType

def _hex(b):
    return ''.join("%02X" % x for x in b)

# This is a copy of the callback class in hid.py - should we have a
# "utils" module instead?
class _callback:
    """Helper class for callback registration
    """
    def __init__(self, parent):
        self._parent = parent
        self._callbacks = {}

    class _callback_handle:
        """Callback handle

        Call unregister() to remove this callback.
        """
        def __init__(self, callback):
            self._callback = callback

        def unregister(self):
            del self._callback._callbacks[self]

    def register(self, func):
        wrapper = self._callback_handle(self)
        self._callbacks[wrapper] = func
        return wrapper

    def _invoke(self, *args):
        for func in self._callbacks.values():
            self._parent.loop.call_soon(func, self._parent, *args)

class bus:
    """A virtual DALI bus
    """
    def __init__(self, name, loop=None):
        self._log = logging.getLogger().getChild("virtual").getChild(name)
        self._name = name
        self.loop = loop or asyncio.get_event_loop()

        self.exceptions_on_send = True
        self.transaction_lock = asyncio.Lock(loop=self.loop)
        self.connection_status_callback = _callback(self)
        self.bus_traffic = _callback(self)
        self.connected = asyncio.Event(loop=self.loop)
        self.firmware_version = None
        self.serial = None
        self.devices = []

    def connect(self):
        self.connected.set()
        self.connection_status_callback._invoke("connected")
        return True

    def disconnect(self):
        self.connected.clear()
        self.connection_status_callback._invoke("disconnected")

    async def send(self, command, in_transaction=False, exceptions=None):
        if exceptions is None:
            exceptions = self.exceptions_on_send

        if not in_transaction:
            await self.transaction_lock.acquire()
        response = None
        for d in self.devices:
            new_response = d.process_command(command)
            if response is None:
                response = new_response
            elif new_response is not None:
                response = dali.frame.BackwardFrameError(255)
        if not in_transaction:
            self.transaction_lock.release()
        return response
