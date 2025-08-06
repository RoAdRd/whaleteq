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

print('output PPG (70BPM, ch1=12.5mV/ch2=25mV, SyncOn) ...')
sys.stdout.flush()

ppg_waveform_1 = device.get_default_ppg_ch1_waveform()
ppg_waveform_2 = device.get_default_ppg_ch2_waveform()

ppg_waveform_1.Frequency = ppg_waveform_2.Frequency = 1.17
ppg_waveform_1.TimePeriod = ppg_waveform_2.TimePeriod = int(1000/1.17)

device.output_ppg_ex(pointer(ppg_waveform_1), pointer(
    ppg_waveform_2), OutputSignalCallback(0), OutputSignalCallback(0))

time.sleep(10)

device.stop_output()
device.free()
