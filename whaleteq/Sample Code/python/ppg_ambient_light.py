from ctypes import *
from aecg100 import *
import sys
import time

"""
The pulse setting is effective only for the following modules:
 - PPG-2TF-660 (WAP2012)
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

device.set_led_ambient_light_mode(PPGAmbientLightMode.SunLight.value)

print('configure to SunLight mode done')
device.free()
