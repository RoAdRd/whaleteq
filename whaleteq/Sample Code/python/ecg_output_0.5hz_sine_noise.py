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

print('output ECG (0.5Hz, 1mV, Sine, RA, Noise: 50Hz/0.5mV) ...')
sys.stdout.flush()

ecg_waveform = device.get_default_ecg_waveform()
ecg_waveform.WaveformType = ECGWaveformType.Sine.value
ecg_waveform.Frequency = 0.5
ecg_waveform.NoiseAmplitude = 0.5
ecg_waveform.NoiseFrequency = ECGNoiseFrequency._50Hz.value

device.output_ecg(pointer(ecg_waveform), OutputSignalCallback(0))

time.sleep(10)

device.stop_output()
device.free()
