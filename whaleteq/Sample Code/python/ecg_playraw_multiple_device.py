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
            ac[lineNumber-4] = float(x) * 3
            dc[lineNumber-4] = 0

        lineNumber = lineNumber + 1

    f.close()

    play_raw_data.AC = addressof(ac)
    play_raw_data.DC = addressof(dc)
    play_raw_data.OutputSignalCallback = OutputSignalCallback(0)
    return play_raw_data

def init_device(device, raw_data, sync_object):
    device.enable_player_loop(c_bool(True))
    device.set_synchronization_signal(c_void_p(sync_object))
    device.play_raw_ecg(pointer(raw_data))

device1 = AECG100('./AECG100x64-1.dll')
if device1.connect(-1, 5000) == False:
    print('Error: device1 is not connected')
    device1.free()
    sys.exit()

device2 = AECG100('./AECG100x64-2.dll')
if device2.connect(-1, 5000) == False:
    print('Error: device2 is not connected')
    device1.free()
    device2.free()
    sys.exit()

device3 = AECG100('./AECG100x64-3.dll')
if device3.connect(-1, 5000) == False:
    print('Error: device3 is not connected')
    device1.free()
    device2.free()
    device3.free()
    sys.exit()

device4 = AECG100('./AECG100x64-4.dll')
if device4.connect(-1, 5000) == False:
    print('Error: device4 is not connected')
    device1.free()
    device2.free()
    device3.free()
    sys.exit()

print('device1 is connected... ({} / {})'.format(
    device1.get_serial_number(),
    device1.get_ppg_serial_number()))

print('device2 is connected... ({} / {})'.format(
    device2.get_serial_number(),
    device2.get_ppg_serial_number()))

print('device3 is connected... ({} / {})'.format(
    device3.get_serial_number(),
    device3.get_ppg_serial_number()))

print('device4 is connected... ({} / {})'.format(
    device4.get_serial_number(),
    device4.get_ppg_serial_number()))

sys.stdout.flush()

time.sleep(5)

raw_data = load_raw_data_file('square_1Hz_1mV.txt')
sync_object = device1.create_synchronization_signal()

init_device (device1, raw_data, sync_object)
init_device (device2, raw_data, sync_object)
init_device (device3, raw_data, sync_object)
init_device (device4, raw_data, sync_object)

pause()
print('Synchronization signal set. Starting output across all devices...')
device1.synchronization_signal_set_event(c_void_p(sync_object))

pause()
device1.stop_output()
device1.free()

device2.stop_output()
device2.free()

device3.stop_output()
device3.free()

device4.stop_output()
device4.free()