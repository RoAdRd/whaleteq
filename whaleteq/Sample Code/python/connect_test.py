from ctypes import *
from aecg100 import *
import sys
import time

device = AECG100(get_lib_path())

def DeviceConnectedHandler(connected):
    if connected:
        print('device is connected ({})'.format(device.get_serial_number()))
    else:        
        print('device is disconnected')


connectedCb = ConnectedCallback(DeviceConnectedHandler)
if not device.init(connectedCb):
    print('Error: init failed')
    sys.exit()


pause()
device.free()
