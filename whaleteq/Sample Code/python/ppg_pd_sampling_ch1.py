from ctypes import *
from aecg100 import *
import threading
import time
import sys

pd1 = []


def Channel1PDSamplingHandler(data, number):
    global pd1
    average_count = 1000

    while number != 0:
        append = min(number, average_count - len(pd1))
        number -= append
        pd1 += [data] * append

        if len(pd1) == average_count:
            average = 0
            for x in pd1:
                average += x

            average /= average_count
            print('\rppg channel-1 pd sampling...' +
                  str(average) + '      ', end='')
            pd1 = []


def SamplingErrorHandler(error):
    print('sampling error... ' + str(error))


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
print('start sampling...')
sys.stdout.flush()

samplingCb = SamplingCallback(Channel1PDSamplingHandler)
samplingErrorCb = SamplingErrorCallback(SamplingErrorHandler)

device.enable_sampling(
    PPGSampling.Channel1PD.value, samplingCb)
device.start_sampling(samplingErrorCb)

time.sleep(10)

device.disable_sampling()
device.free()
