from ctypes import *
from aecg100 import *

device1 = AECG100(get_lib_path())
device2 = AECG100("./AECG100x64.2.dll") # duplicate the lib file to control another WhaleTeq device

def Device1ConnectedHandler(connected):
    if connected:
        print('device1 is connected ({})'.format(device1.get_serial_number()))
    else:
        print('device1 is disconnected')

def Device2ConnectedHandler(connected):
    if connected:
        print('device2 is connected ({})'.format(device2.get_serial_number()))
    else:
        print('device2 is disconnected')

connectedCb1 = ConnectedCallback(Device1ConnectedHandler)
connectedCb2 = ConnectedCallback(Device2ConnectedHandler)

device1.init(connectedCb1)
device2.init(connectedCb2)

input("Press Enter to exit...")

device1.free()
device2.free()