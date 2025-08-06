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

print('output ECG frequency scan (0.5Hz-150Hz, 30sec) ...')
sys.stdout.flush()

scan = FREQUENCY_SCAN()
scan.Amplitude = 1
scan.FrequencyStart = 0.5
scan.FrequencyFinish = 150
scan.Duration = 30

device.output_ecg_frequency_scan(pointer(scan), OutputSignalCallback(0))

time.sleep(31)

device.stop_output()
device.free()
