import os
from ctypes import *
import struct
import platform
from enum import Enum
from functools import wraps


def pause():
    input("Press Enter to continue ...")


def get_lib_path():
    lib_base = "../../SDK"
    if platform.system() == 'Windows':
        if struct.calcsize("P") == 4:
            lib_name = "windows/AECG100x86.dll"
        else:
            lib_name = "windows/AECG100x64.dll"
    elif platform.system() == 'Linux':
        if platform.machine() == 'aarch64':
            lib_name = "linux/libaecgrpix64.so"
        elif platform.machine() == 'armv7l':
            lib_name = "linux/libaecgrpix86.so"
        elif platform.machine() == 'x86_64':
            lib_name = "linux/libaecgx64.so"
        else:
            lib_name = "linux/libaecgx86.so"
    elif platform.system() == 'Darwin':
        lib_name = "macos/libaecg.a"
    return os.path.join(lib_base, lib_name)


ConnectedCallback = CFUNCTYPE(None, c_bool)
OutputSignalCallback = CFUNCTYPE(None, c_double, c_int, c_int)
SamplingCallback = CFUNCTYPE(None, c_int, c_int)
SamplingErrorCallback = CFUNCTYPE(None, c_int)


class PPGChannel(Enum):
    Channel1 = 1
    Channel2 = 2
    Channel3 = 3


class RespirationMode (Enum):
    Off = 0x00
    BaselineModulation = 0x01
    AmplitudeModulation = 0x02
    FrequencyModulation = 0x04
    Resistance = 0x80           # only supported in ECG


class ECGWaveformType (Enum):
    Sine = 0
    Triangle = 1
    Square = 2
    RectanglePulse = 3
    TrianglePulse = 4
    Exponential = 5
    ECG = 6


class Electrode (Enum):
    RightArm = 0     # RA
    LeftArm = 0xff   # LA


class ECGImpedance (Enum):
    Off = 0       # Disable impedance
    On = 0xff     # Enable 620K impedance


class ECGPacingEnable (Enum):
    Off = 0
    On = 0xff


class ECGRespirationBaseline (Enum):
    _500 = 500      # not supported now
    _1000 = 1000
    _1500 = 1500
    _2000 = 2000


class ECGNoiseFrequency (Enum):
    Off = 0
    _50Hz = 1
    _60Hz = 2
    _100Hz = 3
    _120Hz = 4


class PPGWaveformType (Enum):
    Sine = 0
    Triangle = 1
    Square = 2
    PPG = 3


class PPGNoiseFrequency (Enum):
    Off = 0
    _50Hz = 1
    _60Hz = 2
    _1KHz = 3
    _5KHz = 4
    _100Hz = 5
    _120Hz = 6
    WhiteNoise = 7
    _0_5Hz = 8
    _1Hz = 9
    _2Hz = 10
    _3Hz = 11
    _5Hz = 12
    _10Hz = 13
    _25Hz = 14


class LEDType (Enum):
    Green = 0
    Red = 1
    IR = 2
    Max = 3


class LEDPulse (Enum):
    LEDPulseNone = 0x00
    LEDPulseGreen = 0x01
    LEDPulseRed = 0x02
    LEDPulseInfrared = 0x04


class SyncPulse (Enum):
    LEDOff = 0      # not supported now
    SyncOn = 1      # enable the synchronization between AECG100 LED and DUT LED
    SyncOff = 2     # AECG100 LED is always on


class PPGInverted (Enum):
    Off = 0
    On = 1


class PPGSampling (Enum):
    Channel1PD = 0
    Channel2PD = 1
    Channel1Switch = 2
    Channel2Switch = 3
    Max = 4


class PPGAmbientLightMode (Enum):
    Off = 0
    _50Hz = 1
    _60Hz = 2
    _1KHz = 3
    _2KHz = 4
    _3KHz = 5
    _4KHz = 6
    _5KHz = 7
    _6KHz = 8
    _7KHz = 9
    _8KHz = 10
    _9KHz = 11
    _10KHz = 12
    DirectCurrent = 13
    SunLight = 14


class HW_INFORMATION (Structure):
    _fields_ = [
        ('FWMajorVersion', c_int),
        ('FWMinorVersion', c_int),
        ('FWBuildVersion', c_int),
        ('HWVersion', c_int),
        ('PCBVersion', c_int),
        ('FPGAMajorVersion', c_int),
        ('FPGAMinorVersion', c_int)
    ]


class MODEL_INFORMATION (Structure):
    _fields_ = [
        ('ProductName', c_char * 2),
        ('GenerationNumber', c_char),
        ('ModelNumber', c_char),
        ('SerialNumber', c_int),
        ('Year', c_int),
        ('LEDType1', c_int),
        ('LEDType2', c_int),
        ('LEDType3', c_int)
    ]


class ECG_WAVEFORM (Structure):
    _fields_ = [
        ('WaveformType', c_int),
        ('Frequency', c_double),
        ('Amplitude', c_double),
        ('TWave', c_double),
        ('PWave', c_double),
        ('STSegment', c_double),
        ('DCOffsetVariable', c_int),
        ('DCOffset', c_int),
        ('TimePeriod', c_int),
        ('PRInterval', c_int),
        ('QRSDuration', c_int),
        ('TDuration', c_int),
        ('QTInterval', c_int),
        ('Impedance', c_int),
        ('Electrode', c_int),
        ('PulseWidth', c_int),
        ('NoiseAmplitude', c_double),
        ('NoiseFrequency', c_int),
        ('PacingEnabled', c_int),
        ('PacingAmplitude', c_double),
        ('PacingDuration', c_double),
        ('PacingRate', c_int),
        ('RespirationMode', c_int),
        ('RespirationAmplitude', c_int),
        ('RespirationRate', c_int),
        ('RespirationRatio', c_int),
        ('RespirationBaseline', c_int),
        ('RespirationApneaDuration', c_int),
        ('RespirationApneaCycle', c_int),
        ('Reserved', c_char * 12)
    ]


class PPG_WAVEFORM (Structure):
    _fields_ = [
        ('WaveformType', c_int),
        ('Frequency', c_double),
        ('VolDC', c_double),
        ('VolSP', c_double),
        ('VolDN', c_double),
        ('VolDP', c_double),
        ('ACOffset', c_double),
        ('TimeSP', c_int),
        ('TimeDN', c_int),
        ('TimeDP', c_int),
        ('TimePeriod', c_int),
        ('SyncPulse', c_int),
        ('Inverted', c_int),
        ('NoiseAmplitude', c_double),
        ('NoiseFrequency', c_int),
        ('RespirationMode', c_int),
        ('RespirationRate', c_int),
        ('RespirationVariation', c_int),
        ('RespirationInExhaleRatio', c_int),
        ('RespirationApneaDuration', c_int),
        ('RespirationApneaCycle', c_int),
        ('Reserved', c_char * 12)
    ]


class FREQUENCY_SCAN (Structure):
    _fields_ = [
        ('Amplitude', c_double),
        ('FrequencyStart', c_double),
        ('FrequencyFinish', c_double),
        ('Duration', c_int)
    ]


class FREQUENCY_SCAN2 (Structure):
    _fields_ = [
        ('Amplitude', c_double),
        ('DC', c_double),
        ('SyncPulse', c_int),
        ('FrequencyStart', c_double),
        ('FrequencyFinish', c_double),
        ('Duration', c_int)
    ]


class PLAY_RAW_DATA (Structure):
    _fields_ = [
        ('SampleRate', c_double),
        ('Size', c_int),
        ('SyncPulse', c_int),
        ('AC', c_void_p),
        ('DC', c_void_p),
        ('OutputSignalCallback', OutputSignalCallback)
    ]


class PPG_LED_PULSE_GROUP_SETTING (Structure):
    _fields_ = [
        ('PulseLEDTable', c_ubyte * 8),
        ('PulseGroupInterval', c_ushort)
    ]


def sdk_fn(cfn_name, args_type=None, return_type=None):
    def decorator_function(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cfn = getattr(self.sdk, cfn_name)
            if args_type:
                cfn.argtypes = args_type
            if return_type:
                cfn.restype = return_type
            return cfn(*args, **kwargs)

        return wrapper

    return decorator_function


class AECG100:
    def __init__(self, lib_file_path):        
        self.sdk = cdll.LoadLibrary(lib_file_path)        
    
    #
    # Initialization & Cleanup
    #
    @sdk_fn("WTQInit", [ConnectedCallback], c_bool)
    def init(self, cb) -> c_bool:
        pass

    @sdk_fn("WTQConnect", [c_uint, c_uint], c_bool)
    def connect(self, port_number, milliseconds_timeout) -> c_bool:
        pass

    @sdk_fn("WTQFree", [], None)
    def free(self) -> None:
        pass

    @sdk_fn("WTQGetVersion", [], c_uint32)
    def get_version(self) -> c_uint32:
        pass

    #
    # Device Configurations
    #
    def get_serial_number(self):
        self.sdk.WTQGetSerialNumber.restype = c_char_p
        return self.sdk.WTQGetSerialNumber().decode('ascii')

    def get_ppg_serial_number(self):
        self.sdk.WTQGetPPGSerialNumber.restype = c_char_p
        return self.sdk.WTQGetPPGSerialNumber().decode('ascii')

    @sdk_fn("WTQGetPPGDeviceInformation", [c_void_p], c_bool)
    def get_ppg_device_information(self) -> c_bool:
        pass

    #
    # PPG Module Sampling
    #
    @sdk_fn("WTQEnableSampling", [c_int, SamplingCallback], c_bool)
    def enable_sampling(self, mode, cb) -> c_bool:
        pass

    @sdk_fn("WTQStartSampling", [SamplingErrorCallback], c_bool)
    def start_sampling(self, cb) -> c_bool:
        pass

    @sdk_fn("WTQDisableSampling", [], None)
    def disable_sampling(self) -> None:
        pass

    #
    # PPG Module LED Configuration
    #
    @sdk_fn("WTQReadLEDPulseGroupSetting", [c_void_p], c_bool)
    def read_led_pulse_group_setting(self, pulse_group_setting) -> c_bool:
        pass

    @sdk_fn("WTQWriteLEDPulseGroupSetting", [c_void_p], c_bool)
    def write_led_pulse_group_setting(self, pulse_group_setting) -> c_bool:
        pass

    @sdk_fn("WTQSetLEDAmbientLightMode", [c_int], c_bool)
    def set_led_ambient_light_mode(self, mode) -> c_bool:
        pass

    #
    # ECG Signal Output Control
    #
    @sdk_fn("WTQDeviceSetDCOffset", [c_int], c_bool)
    def set_dc_offset(self, dc_offset):
        pass

    #
    # Output waveform in device alone mode
    #
    @sdk_fn("WTQOutputECG", [c_void_p, OutputSignalCallback], c_bool)
    def output_ecg(self, waveform, cb) -> c_bool:
        pass

    @sdk_fn("WTQOutputECGAndPPG", [c_int, c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback], c_bool)
    def output_ecg_ppg(self, pttp, ecg_waveform, ppg_waveform, cb_ecg, cb_ppg):
        pass

    @sdk_fn("WTQOutputECGAndPPGEx", [c_int, c_void_p, c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback, OutputSignalCallback], c_bool)
    def output_ecg_ppg_2(self, pttp, ecg_waveform, ppg_waveform_ch1, ppg_waveform_ch2, cb_ecg, cb_ppg_ch1, cb_ppg_ch2):
        pass

    @sdk_fn("WTQOutputPPG", [c_int, c_void_p, OutputSignalCallback], c_bool)
    def output_ppg(self, channel_number, waveform, cb) -> c_bool:
        pass

    @sdk_fn("WTQOutputPPGEx", [c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback], c_bool)
    def output_ppg_ex(self, waveform_ch1, waveform_ch2, cb_ch1, cb_ch2) -> c_bool:
        pass

    @sdk_fn("WTQOutputFrequencyScan", [c_void_p, OutputSignalCallback], c_bool)
    def output_ecg_frequency_scan(self, scan, cb) -> c_bool:
        pass

    #
    # Play Raw Data
    #
    @sdk_fn("WTQWaveformPlayerOutputECG", [c_void_p], c_bool)
    def play_raw_ecg(self, raw_data) -> c_bool:
        pass

    @sdk_fn("WTQWaveformPlayerOutputPPG", [c_int, c_void_p], c_bool)
    def play_raw_ppg(self, channel_number, raw_data) -> c_bool:
        pass

    @sdk_fn("WTQWaveformPlayerOutputPPGEx", [c_void_p, c_void_p], c_bool)
    def play_raw_ppg_ex(self, raw_data_ch1, raw_data_ch2) -> c_bool:
        pass

    @sdk_fn("WTQWaveformPlayerOutputPPG3", [c_void_p, c_void_p, c_void_p], c_bool)
    def play_raw_ppg3(self, raw_data_ch1, raw_data_ch2, raw_data_ch3) -> c_bool:
        pass

    #
    # Output waveform in play-raw mode
    #
    @sdk_fn("WTQPlayECG", [c_void_p, OutputSignalCallback], c_bool)
    def play_ecg(self, waveform, cb) -> c_bool:
        pass

    @sdk_fn("WTQPlayECGAndPPG", [c_int, c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback], c_bool)
    def play_ecg_ppg(self, pttp, ecg_waveform, ppg_waveform, cb_ecg, cb_ppg) -> c_bool:
        pass

    @sdk_fn("WTQPlayECGAndPPGEx", [c_int, c_void_p, c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback, OutputSignalCallback], c_bool)
    def play_ecg_ppg_2(self, pttp, ecg_waveform, ppg_waveform_ch1, ppg_waveform_ch2, cb_ecg, cb_ppg_ch1, cb_ppg_ch2) -> c_bool:
        pass

    @sdk_fn("WTQPlayPPG", [c_int, c_void_p, OutputSignalCallback], c_bool)
    def play_ppg(self, channel_number, waveform, cb) -> c_bool:
        pass

    @sdk_fn("WTQPlayPPGEx", [c_void_p, c_void_p, OutputSignalCallback, OutputSignalCallback], c_bool)
    def play_ppg_ex(self, waveform_ch1, waveform_ch2, cb_ch1, cb_ch2) -> c_bool:
        pass

    @sdk_fn("WTQWaveformPlayerLoop", [c_bool], None)
    def enable_player_loop(self, c_bool):
        pass

    @sdk_fn("WTQStopOutputWaveform", [], None)
    def stop_output(self):
        pass

    @sdk_fn("WTQCreateSynchronizationSignal", [], c_void_p)
    def create_synchronization_signal(self) -> c_void_p:
        pass

    @sdk_fn("WTQSetSynchronizationSignal", [c_void_p], None)
    def set_synchronization_signal(self, sync_object) -> None:
        pass

    @sdk_fn("WTQSynchronizationSignalSetEvent", [c_void_p], None)
    def synchronization_signal_set_event(self, sync_object) -> None:
        pass

    @sdk_fn("WTQSynchronizationSignalResetEvent", [c_void_p], None)
    def synchronization_signal_reset_event(self, sync_object) -> None:
        pass

    def get_default_ecg_waveform(self):
        waveform = ECG_WAVEFORM()
        waveform.WaveformType = ECGWaveformType.ECG.value
        waveform.Frequency = 1
        waveform.Amplitude = 1.0
        waveform.TWave = 0.2
        waveform.PWave = 0.2
        waveform.STSegment = 0
        waveform.DCOffsetVariable = 0
        waveform.DCOffset = 0
        waveform.TimePeriod = 1000
        waveform.PRInterval = 160
        waveform.QRSDuration = 100
        waveform.TDuration = 180
        waveform.QTInterval = 350
        waveform.Impedance = ECGImpedance.Off.value
        waveform.Electrode = Electrode.RightArm.value
        waveform.PulseWidth = 100
        waveform.NoiseAmplitude = 0
        waveform.NoiseFrequency = ECGNoiseFrequency.Off.value
        waveform.PacingEnabled = 0
        waveform.PacingAmplitude = 2
        waveform.PacingDuration = 2
        waveform.PacingRate = 60
        waveform.RespirationMode = RespirationMode.Off.value
        waveform.RespirationAmplitude = 1000
        waveform.RespirationRate = 20
        waveform.RespirationBaseline = 1000
        waveform.RespirationRatio = 1
        waveform.RespirationApneaDuration = 10
        waveform.RespirationApneaCycle = 1

        return waveform

    def get_default_ppg_ch3_waveform(self):
        waveform = PPG_WAVEFORM()
        waveform.Frequency = 1
        waveform.WaveformType = PPGWaveformType.PPG.value
        waveform.VolDC = 625
        waveform.VolSP = 12.5
        waveform.VolDN = 7.0
        waveform.VolDP = 8.0
        waveform.ACOffset = 0
        waveform.TimePeriod = 1000
        waveform.TimeSP = 150
        waveform.TimeDN = 360
        waveform.TimeDP = 460
        waveform.SyncPulse = SyncPulse.SyncOn.value
        waveform.Inverted = PPGInverted.On.value
        waveform.NoiseAmplitude = 0
        waveform.NoiseFrequency = PPGNoiseFrequency.Off.value
        waveform.RespirationMode = RespirationMode.Off.value
        waveform.RespirationRate = 20
        waveform.RespirationVariation = 1
        waveform.RespirationInExhaleRatio = 1
        waveform.RespirationApneaDuration = 10
        waveform.RespirationApneaCycle = 1
        return waveform

    def get_default_ppg_ch2_waveform(self):
        waveform = PPG_WAVEFORM()
        waveform.Frequency = 1
        waveform.WaveformType = PPGWaveformType.PPG.value
        waveform.VolDC = 625
        waveform.VolSP = 25.0
        waveform.VolDN = 14.0
        waveform.VolDP = 16.0
        waveform.ACOffset = 0
        waveform.TimePeriod = 1000
        waveform.TimeSP = 150
        waveform.TimeDN = 360
        waveform.TimeDP = 460
        waveform.SyncPulse = SyncPulse.SyncOn.value
        waveform.Inverted = PPGInverted.On.value
        waveform.NoiseAmplitude = 0
        waveform.NoiseFrequency = PPGNoiseFrequency.Off.value
        waveform.RespirationMode = RespirationMode.Off.value
        waveform.RespirationRate = 20
        waveform.RespirationVariation = 1
        waveform.RespirationInExhaleRatio = 1
        waveform.RespirationApneaDuration = 10
        waveform.RespirationApneaCycle = 1
        return waveform
