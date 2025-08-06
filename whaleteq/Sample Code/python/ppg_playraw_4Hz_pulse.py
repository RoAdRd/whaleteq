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

print('ppg play raw (4Hz, rectangle pulse, 50ms)...')
sys.stdout.flush()

raw_data = PLAY_RAW_DATA()
raw_data.SampleRate = 1000
raw_data.Size = 1000
raw_data.SyncPulse = SyncPulse.SyncOff.value

SampleArray = c_double * raw_data.Size
ac = SampleArray()
dc = SampleArray()
for i in range(50):
    ac[i] = 30
    ac[i+250] = 30
    ac[i+500] = 30
    ac[i+750] = 30

raw_data.AC = addressof(ac)
raw_data.DC = addressof(dc)
raw_data.OutputSignalCallback = OutputSignalCallback(0)

device.enable_player_loop(c_bool(True))
device.play_raw_ppg(PPGChannel.Channel1.value, pointer(raw_data))

time.sleep(10)

device.stop_output()
device.free()
