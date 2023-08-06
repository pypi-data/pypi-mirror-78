
# IEC 62386-102 table 4 - nominal fade times in seconds; 0->"use fast fade time"
_table_102_4_fade_times = [
    0, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0, 5.7,
    8.0, 11.3, 16.0, 22.6, 32.0, 45.3, 64.0, 90.5,
]

# IEC 62386-207 table 1 - fast fade times in seconds, range 0..27
def _table_207_1_fade_time(no):
    return no * 0.025

# IEC 62386-102 table 6 - extended fade time base values (no unit)
def _table_102_6_base_value(bits):
    return bits + 1

# IEC 62386-102 table 7 - extended fade time multiplier in seconds
_table_102_7_multiplier = [
    0, 0.1, 1, 10, 60,
    # values 5..7 are reserved
]

def SetFadeTime(addr, fadetime,
                use_fast_fade_time=False,
                use_extended_fade_time=True):
    """Set the fade time as close as possible to the specified fade time.

    If the device supports Fast Fade Time as defined in IEC-62386 part
    207 (LED modules) then set use_fast_fade_time to True.

    If the device does not support Extended Fade Time as defined in
    IEC-62386 part 102 then set use_extended_fade_time to False.

    Returns the actual nominal fade time selected.
    """
    for idx, standard_fade_time in enumerate(_table_102_4_fade_times):
        
