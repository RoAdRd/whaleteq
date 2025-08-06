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

print('ppg play raw...')
sys.stdout.flush()

raw_data = PLAY_RAW_DATA()
f = open('ppg_raw_data.txt', 'r')
lineNumber = 0
for x in f:
    if lineNumber == 0:
        raw_data.SampleRate = int(x)
    elif lineNumber == 1:
        raw_data.Size = int(x)
        ac = (c_double * raw_data.Size)()
        dc = (c_double * raw_data.Size)()
    elif lineNumber >= 4:
        ac[lineNumber-4] = float(x)
        dc[lineNumber-4] = 625
    lineNumber = lineNumber + 1
f.close()

normAc = (c_double * raw_data.Size)()
OldRange = (max(ac) - min(ac))
NewRange = 12.5
for i in range(len(ac)):
    normAc[i] = (((ac[i] - min(ac)) * NewRange) / OldRange)

raw_data.AC = addressof(normAc)
raw_data.DC = addressof(dc)
raw_data.SyncPulse = SyncPulse.SyncOn.value
raw_data.OutputSignalCallback = OutputSignalCallback(0)

device.enable_player_loop(c_bool(True))
device.play_raw_ppg(PPGChannel.Channel1.value, pointer(raw_data))

time.sleep(10)

device.stop_output()
device.free()
