from ctypes import *
from aecg100 import *
import sys
import time

"""
The pulse setting is effective only for the following modules:
 - PPG-1R-660 (WAP2005)
 - PPG-1T-660 (WAP2006)
 - PPG-2RS-880 (WAP2007)
"""

device = AECG100(get_lib_path())
if device.connect(-1, 5000) == False:
    print('Error: device is not connected')
    device.free()
    sys.exit()

print('device is connected... ({} / {})'.format(
    device.get_serial_number(),
    device.get_ppg_serial_number()))
sys.stdout.flush()

pulseSetting = PPG_LED_PULSE_GROUP_SETTING()
pulseSetting.PulseGroupInterval = 4500
pulseSetting.PulseLEDTable[0] = LEDPulse.LEDPulseRed.value
pulseSetting.PulseLEDTable[1] = LEDPulse.LEDPulseInfrared.value
pulseSetting.PulseLEDTable[2] = LEDPulse.LEDPulseGreen.value

print('configure pulse sequence...')
if device.write_led_pulse_group_setting(pointer(pulseSetting)) == False:
    print('Error: write pulse group setting failed')

print('configure done')
device.free()
