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

print('output PWTT (ECG/PPG-Ch1, PTTp: 550ms) ...')
sys.stdout.flush()

ecg_waveform = device.get_default_ecg_waveform()
ppg_waveform = device.get_default_ppg_ch1_waveform()
device.output_ecg_ppg(c_int(550), pointer(ecg_waveform), pointer(
    ppg_waveform), OutputSignalCallback(0), OutputSignalCallback(0))

time.sleep(10)

device.stop_output()
device.free()
