from ctypes import *
from aecg100 import *
import sys
import time

device = AECG100(get_lib_path())


def OutputVariableOffset(offset):
    print('set variable DC offset to ' + str(offset) + 'mV ...')
    sys.stdout.flush()

    ecg_waveform = device.get_default_ecg_waveform()
    ecg_waveform.WaveformType = ECGWaveformType.Sine.value
    ecg_waveform.Amplitude = 0
    ecg_waveform.DCOffsetVariable = 1
    ecg_waveform.DCOffset = offset
    device.output_ecg(pointer(ecg_waveform), OutputSignalCallback(0))
    time.sleep(5)
    device.stop_output()


if device.connect(-1, 5000) == False:
    print('Error: device is not connected')
    device.free()
    sys.exit()

print('device is connected... ({} / {})'.format(
    device.get_serial_number(),
    device.get_ppg_serial_number()))
sys.stdout.flush()

time.sleep(5)

for offset in [200, 500, -200, -500]:
    OutputVariableOffset(offset)

device.free()
