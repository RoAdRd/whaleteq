from ctypes import *
from aecg100 import *
import sys
import time

device = AECG100(get_lib_path())
if device.connect(-1, 5000) == False:
    print('Error: device is not connected')
    device.free()
    sys.exit()


print('device is connected... ({} / {})'.format(
    device.get_serial_number(),
    device.get_ppg_serial_number()))
sys.stdout.flush()

time.sleep(5)
print('set DC offset to +300mV ...')
sys.stdout.flush()
device.set_dc_offset(300)

time.sleep(5)
print('set DC offset to -300mV ...')
sys.stdout.flush()
device.set_dc_offset(-300)

time.sleep(5)
print('set DC offset to 0mV ...')
sys.stdout.flush()
device.set_dc_offset(0)

device.free()
