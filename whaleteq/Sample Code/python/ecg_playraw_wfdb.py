from ctypes import *
from aecg100 import *
import sys
import time
import threading
import matplotlib
import matplotlib.pyplot as plt
import wfdb

# Ensure required packages are installed
"""
Install packages:
pip install wfdb matplotlib
"""

# Initialize threading lock for safe data handling between threads
the_lock = threading.Lock()

# Setup matplotlib for real-time plotting
fig = plt.figure()
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('ECG Output')
plt.ion()
plt.show(block=False)
plt.ylim(-1, 1) # Set the y-axis limits for ECG voltage

data_x = []
data_y = []
last_plt_x = 0
last_plt_y = 0

def signal_output(time, ac, dc):
    """Callback function to handle output signal from the device."""
    global data_x
    global data_y

    with the_lock:
        data_x.append(time)
        data_y.append(ac/1000.0)

def load_signals(record_name, channel_name):
    """Load signals from a specified record and channel."""
    try:
        record = wfdb.rdrecord(record_name)
        channel_index = record.sig_name.index(channel_name)
        signals = record.p_signal[:, channel_index]
        return (c_double * len(signals))(*signals), record.fs
    except FileNotFoundError:
        print(f"Error: Record file {record_name} not found.")
        sys.exit(1)
    except ValueError:
        print(f"Error: Channel {channel_name} not found in the record.")
        sys.exit(1)

# Initialize device
device = AECG100(get_lib_path())

# Connect to device
if device.connect(-1, 5000) == False:
    print('Error: device is not connected')
    device.free()
    sys.exit()

time.sleep(5)

print('device is connected... ({} / {})'.format(
    device.get_serial_number(),
    device.get_ppg_serial_number()))

# Load ECG signals from record
signal_data, sample_rate = load_signals('03900001', 'III')

# Prepare the PLAY_RAW_DATA structure
play_raw_data = PLAY_RAW_DATA()
play_raw_data.SampleRate = sample_rate
play_raw_data.Size = len(signal_data)
play_raw_data.AC = cast(signal_data, c_void_p)
play_raw_data.DC = cast((c_double * len(signal_data))(*([0] * len(signal_data))), c_void_p)
play_raw_data.OutputSignalCallback = OutputSignalCallback(signal_output)

# Play ECG data
device.enable_player_loop(c_bool(True))
device.play_raw_ecg(pointer(play_raw_data))

# Loop for up to 30 seconds
while last_plt_x < 30:    
    data = [[last_plt_x], [last_plt_y]]
    with the_lock:
        if len(data_x) == 0:
            continue

        data[0] += data_x
        data[1] += data_y
        last_plt_x = data_x[-1]
        last_plt_y = data_y[-1]
        data_x = []
        data_y = []

    plt.xlim(last_plt_x-10, last_plt_x+0.1)
    plt.plot(data[0], data[1], c='black')
    plt.draw()
    plt.pause(0.1)

    time.sleep(0.2)

device.stop_output()
device.free()
