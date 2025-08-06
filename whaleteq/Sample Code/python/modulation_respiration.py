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

print('output ECG+PPG (baseline respiration) ...')
sys.stdout.flush()

ecg_waveform = device.get_default_ecg_waveform()
ppg_waveform = device.get_default_ppg_ch1_waveform()

ecg_waveform.RespirationMode = ppg_waveform.RespirationMode = RespirationMode.BaselineModulation.value | RespirationMode.FrequencyModulation.value
ecg_waveform.RespirationRate = ppg_waveform.RespirationRate = 20  # BPM
ecg_waveform.RespirationRatio = ppg_waveform.RespirationVariation = 10  # variation; 10%
ecg_waveform.RespirationBaseline = ppg_waveform.RespirationInExhaleRatio = 2

device.play_ecg_ppg(c_int(550), pointer(ecg_waveform), pointer(
    ppg_waveform), OutputSignalCallback(0), OutputSignalCallback(0))

time.sleep(10)

device.stop_output()
device.free()
