from ctypes import *
from aecg100 import *
import sys
import time


ac = None
dc = None
def load_raw_data_file(file_name):
    global ac, dc
    
    play_raw_data = PLAY_RAW_DATA()
    lineNumber = 0
    f = open(file_name)
    for x in f:
        if lineNumber == 0:
            play_raw_data.SampleRate = int(x)
        elif lineNumber == 1:
            play_raw_data.Size = int(x)
            ac = (c_double * play_raw_data.Size)()
            dc = (c_double * play_raw_data.Size)()
        elif lineNumber >= 4:
            ac[lineNumber-4] = float(x)
            dc[lineNumber-4] = 0

        lineNumber = lineNumber + 1

    f.close()

    play_raw_data.AC = addressof(ac)
    play_raw_data.DC = addressof(dc)
    play_raw_data.OutputSignalCallback = OutputSignalCallback(0)
    return play_raw_data


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

print('ecg play raw (1Hz, 5mV)...')
sys.stdout.flush()

raw_data = load_raw_data_file('ecg-1hz-5mv.txt')
device.enable_player_loop(c_bool(True))
device.play_raw_ecg(pointer(raw_data))

time.sleep(10)

device.stop_output()
device.free()
