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

playRaw = PLAY_RAW_DATA()
playRaw.SampleRate = 1000
playRaw.Size = 1000
playRaw.SyncPulse = SyncPulse.SyncOff.value

SampleArray = c_double * playRaw.Size
ac = SampleArray()
dc = SampleArray()
for i in range(50):
    ac[i] = 30
    ac[i+250] = 30
    ac[i+500] = 30
    ac[i+750] = 30

playRaw.AC = addressof(ac)
playRaw.DC = addressof(dc)
playRaw.OutputSignalCallback = OutputSignalCallback(0)

device.enable_player_loop(c_bool(True))
if device.play_raw_ppg3(pointer(playRaw), pointer(playRaw), pointer(playRaw)) == False:
    print('Error: output data failed')
    device.free()
    sys.exit()

time.sleep(10)

device.stop_output()
device.free()
