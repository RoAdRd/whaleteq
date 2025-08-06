#pragma once

#ifndef DOXYGEN_SHOULD_SKIP_THIS
#if defined(WIN32)
#ifdef WHALETEQ_API

#else
#define WHALETEQ_API extern "C" __declspec(dllimport)
#endif
#elif defined(LINUX) || defined(OSX)
#define WHALETEQ_API extern "C"
#endif
#endif


// Defined in <limits.h>
//#define INT_MIN     (-2147483647 - 1) /* minimum (signed) int value */

/// \fn ConnectedCallback
/// \brief Called when the device is connected or disconnected
/// @param[in] connected    true if connected; otherwise, it's false
typedef void (*ConnectedCallback) (bool connected);

/// \fn OutputSignalCallback
/// \brief Called back with outputted data; if the outputting is stopped, the data sent by the last callback is the minimum value of INT
/// @param[in] ac         Unit: uV
/// @param[in] dc         Unit: uV
typedef void (*OutputSignalCallback) (double time, int ac, int dc);

/// \fn SamplingCallback
/// \brief Called back with sampling data; the PD sampling data is [0, 1023]
/// @param[in] data       PD sampling data
/// @param[in] number     the number of the sampling data with the value
typedef void (*SamplingCallback) (int data, int number);

/// DUTSignalDetectionCallback
/// \brief Called back with the DUT signal strength
/// @param[in] location    0~100. 50: best location, < 0: signal is not detected, 0: top side, 100: too bottom side
typedef void (*DUTSignalDetectionCallback) (int location);

/// \fn SamplingErrorCallback
/// \brief Called back with PD sampling error code
/// @param[in] error      Error code for PD sampling error
typedef void (*SamplingErrorCallback) (int error);

#define STATUS_OK                      0
#define STATUS_DEVICE_NOT_CONNECTED    1
#define STATUS_DEVICE_ERROR            2
#define STATUS_INVALID_PARAMETER       3
#define STATUS_INVALID_MODE_TYPE       4  // Mode-ECG, Mode-PWV, Mode-SPO2, Mode-PPG (1 LED), Mode-PPG (2 LED)

// Sampling Error Code
#define SAMPLING_STATUS_CHANNEL1_PD_PACKET_LOST      0x10    //!< the packet of channel-1 pd sampling is lost
#define SAMPLING_STATUS_CHANNEL1_SWITCH_PACKET_LOST  0x11    //!< the packet of channel-1 switch (trigger level) sampling is lost
#define SAMPLING_STATUS_CHANNEL2_PD_PACKET_LOST      0x12    //!< the packet of channel-2 pd sampling is lost
#define SAMPLING_STATUS_CHANNEL2_SWITCH_PACKET_LOST  0x13    //!< the packet of channel-2 switch (trigger level) sampling is lost


// WAP1001      channel-1: G, channel-2: NA,  channel-3: NA
// WAP2001-2004 channel-1: R, channel-2: IR,  channel-3: NA
// WAP2005-2008 channel-1: R, channel-2: IR,  channel-3: G 
// WAP2012      channel-1: R, channel-2: IR,  channel-3: NA
typedef enum {
    PPGChannel1 = 1,               //!< channel-1
    PPGChannel2 = 2,               //!< channel-2
    PPGChannel3 = 3                //!< channel-3
} PPGChannel;

typedef enum {
    StandAloneModeMain,
    StandAloneModeA,               //!< Mode-A
    StandAloneModeB,               //!< Mode-B
    StandAloneModeC                //!< Mode-C
} StandAloneMode;

typedef enum {
    ModeTypeECG = 1,               //!< ECG mode
    ModeTypePWV = 2,               //!< PWV mode (ECG+PPG)
    ModeTypeSPO2 = 3,              //!< SPO2 mode (two PPG channel)
    ModeTypePPG1 = 4,              //!< PPG Adv mode (only PPG channel-1)
    ModeTypePPG2 = 5,              //!< PPG Adv mode (two PPG channels)
    ModeTypePWV2 = 6,              //!< PWV mode (ECG + two PPG)
    ModeTypePWV3 = 7,              //!< PWV mode (ECG + three PPG)
    ModeTypeSPO23 = 8,             //!< SPO2 mode (three PPG channel)
    ModeTypePPG3 = 9,              //!< PPG Adv mode (three PPG channels)
    ModeTypeMax = 10
} ModeType;


typedef enum {
    RespirationModeOff = 0x00,
    RespirationModeBaselineModulation = 0x01,
    RespirationModeAmplitudeModulation = 0x02,
    RespirationModeFrequencyModulation = 0x04,
    RespirationModeResistance = 0x80              //!< only supported in ECG; if the Resistance is used, others will be ignored
} RespirationMode;

typedef enum {
    ECGWaveformTypeSine,           //!< Sine
    ECGWaveformTypeTriangle,       //!< Triangle
    ECGWaveformTypeSquare,         //!< Square
    ECGWaveformTypeRectanglePulse, //!< Rectangle Pulse
    ECGWaveformTypeTrianglePulse,  //!< Triangle Pulse
    ECGWaveformTypeExponential,    //!< Exponential
    ECGWaveformTypeECG,
} ECGWaveformType;

/// Device output lead
typedef enum {
    ElectrodeRightArm,             //!< RA
    ElectrodeLeftArm = 0xff        //!< LA
} Electrode;

typedef enum {
    ECGImpedanceOff,               //!< Disable impedance
    ECGImpedanceOn = 0xff          //!< Enable 620K impedance
} ECGImpedance;

typedef enum {
    ECGPacingOff,
    ECGPacingOn = 0xff
} ECGPacingEnable;

typedef enum {
    ECGRespirationBaseline500 = 500,       //!< not supported now
    ECGRespirationBaseline1000 = 1000,
    ECGRespirationBaseline1500 = 1500,
    ECGRespirationBaseline2000 = 2000
} ECGRespirationBaseline;

typedef enum {
    ECGNoiseFrequencyOff,         //!< No noise
    ECGNoiseFrequency50Hz,        //!< 50Hz noise
    ECGNoiseFrequency60Hz,        //!< 60Hz noise
    ECGNoiseFrequency100Hz,       //!< 100Hz noise
    ECGNoiseFrequency120Hz        //!< 120Hz noise
} ECGNoiseFrequency;

typedef enum {
    PPGWaveformTypeSine,          //!< Sine
    PPGWaveformTypeTriangle,      //!< Triangle
    PPGWaveformTypeSquare,        //!< Square
    PPGWaveformTypePPG            //!< PPG
} PPGWaveformType;

typedef enum {
    PPGNoiseFrequencyOff,         //!< No noise
    PPGNoiseFrequency50Hz,        //!< 50Hz noise
    PPGNoiseFrequency60Hz,        //!< 60Hz noise
    PPGNoiseFrequency1KHz,        //!< 1KHz noise
    PPGNoiseFrequency5KHz,        //!< 5KHz noise
    PPGNoiseFrequency100Hz,       //!< 100Hz noise
    PPGNoiseFrequency120Hz,       //!< 120Hz noise
    PPGNoiseFrequencyWhiteNoise,  //!< white noise
    PPGNoiseFrequeycy0_5Hz,       //!< 0.5Hz noise
    PPGNoiseFrequeycy1Hz,         //!< 1Hz noise
    PPGNoiseFrequeycy2Hz,         //!< 2Hz noise
    PPGNoiseFrequeycy3Hz,         //!< 3Hz noise
    PPGNoiseFrequeycy5Hz,         //!< 5Hz noise
    PPGNoiseFrequeycy10Hz,        //!< 10Hz noise
    PPGNoiseFrequeycy25Hz         //!< 25Hz noise
} PPGNoiseFrequency;

typedef enum {
    LEDTypeGreen,                 //!< Green
    LEDTypeRed,                   //!< Red
    LEDTypeIR,                    //!< IR
    LEDTypeNone                   //!< not existing
} LEDType;

typedef enum {
    LEDPulseNone = 0x00,
    LEDPulseGreen = 0x01,
    LEDPulseRed = 0x02,
    LEDPulseInfrared = 0x04
} LEDPulse;

typedef enum {
    SyncPulseLEDOff,              //!< not supported now
    SyncPulseSyncOn,              //!< enable the synchronization between AECG100 LED and DUT LED
    SyncPulseSyncOff              //!< AECG100 LED is always on
} SyncPulse;

typedef enum {
    PPGInvertedOff,               //!< The outputting PPG waveform is not inverted 
    PPGInvertedOn                 //!< The outputting PPG waveform is inverted
} PPGInverted;

typedef enum {
    PPGSamplingChannel1PD,
    PPGSamplingChannel2PD,
    PPGSamplingChannel1Switch,
    PPGSamplingChannel2Switch,
    PPGSamplingMax
} PPGSampling;

typedef enum {
    PPGAmbientLightOff,    
    PPGAmbientLight50Hz,
    PPGAmbientLight60Hz,
    PPGAmbientLight1KHz,
    PPGAmbientLight2KHz,
    PPGAmbientLight3KHz,
    PPGAmbientLight4KHz,
    PPGAmbientLight5KHz,
    PPGAmbientLight6KHz,
    PPGAmbientLight7KHz,
    PPGAmbientLight8KHz,
    PPGAmbientLight9KHz,
    PPGAmbientLight10KHz,
    PPGAmbientLightDirectCurrent,
    PPGAmbientLightSunLight	
} PPGAmbientLightMode;


/// \anchor structHW_INFORMATION
/// \brief Define a structure of device hw and fw information
/// \details <B>FW version:</B> x.y (ex: version 1.2)\n
///          <B>HW version:</B> x (ex: version 9)
typedef struct {
    int         FWMajorVersion;    //!< FW major version
    int         FWMinorVersion;    //!< FW minor version
    int         FWBuildVersion;    //!< FW build version
    int         HWVersion;         //!< HW version
    int			PCBVersion;        //!< PCB version
    int			FPGAMajorVersion;  //!< FPGA major version; only used in PPG module
    int			FPGAMinorVersion;  //!< FPGA minor version; only used in PPG module
} HW_INFORMATION;

/// \anchor structMODEL_INFORMATION
/// \brief Define a structure of the device model; for C code, you can get the serial number by the format: 
///        ("W%c%c%02X%02X-%02d%04d", ProductName[0], ProductName[1], GenerationNumber, ModelNumber, Year, SerialNumber)
typedef struct {
    char            ProductName[2];
    unsigned char   GenerationNumber;
    unsigned char   ModelNumber;
    int             SerialNumber;       //!< device serial number
    int             Year;               //!< 0x11 = 2017
    int             LEDType1;           //!< enum ::LEDType of channel-1 
    int             LEDType2;           //!< enum ::LEDType of channel-2
    int             LEDType3;           //!< enum ::LEDType of channel-3
} MODEL_INFORMATION;

/// \anchor structECG_WAVEFORM
/// \brief  Define a structure of ECG waveform setting
typedef struct {
    int         WaveformType;                 //!< ::ECGWaveformType
    double      Frequency;                    //!< Unit: Hz
    double      Amplitude;                    //!< Unit: mV
    double      TWave;                        //!< Unit: mV
    double      PWave;                        //!< Unit: mV
    double      STSegment;                    //!< Unit: mV
    int         DCOffsetVariable;             //!< boolean value; the possible DCOffset value depends on this
    int         DCOffset;                     //!< If DCOffsetVariable is true, the range is -500~500; otherwise, the value is 300|0|-300.
    int         TimePeriod;                   //!< Unit: ms
    int         PRInterval;                   //!< Unit: ms
    int         QRSDuration;                  //!< Unit: ms
    int         TDuration;                    //!< Unit: ms
    int         QTInterval;                   //!< Unit: ms
    int         Impedance;                    //!< ::ECGImpedance
    int         Electrode;                    //!< ::Electrode
    int         PulseWidth;                   //!< Effective only when the WaveformType is ::ECGWaveformTypeRectanglePulse| ::ECGWaveformTypeTrianglePulse| ::ECGWaveformTypeExponential
    double      NoiseAmplitude;               //!< Unit: mV; The max noise amplitude is 2.00 mV
    int         NoiseFrequency;               //!< ::ECGNoiseFrequency
    int         PacingEnabled;                //!< boolean value; 0 if disable
    double      PacingAmplitude;              //!< Unit: mV; -1000mV ~ 1000mV
    double      PacingDuration;               //!< Unit: ms; 0ms ~ 2ms; resolution: 0.1ms
    int         PacingRate;                   //!< Unit: BPM
    int         RespirationMode;              //!< Holds a combination of ::RespirationMode enum values
    int         RespirationAmplitude;         //!< Unit: milli-ohm; the supported range: 1000 ~ 5000 milli-ohm; resolution: 0.1 ohm
    int         RespirationRate;              //!< 4~200 BrPM
    int         RespirationRatio;             //!< (a) Resistance: the possible values are from 1 to 5. 1 means 1:1, 2 means 1:2. The default is 1 (1:1). <br>(b) Modulation: respiration variation. Unit: -16~16% percent
    int         RespirationBaseline;          //!< (a) Resistance: ::ECGRespirationBaseline. The default is 1000 ohm. <br>(b) Modulation: in-exhale ratio; the supported value is 1~5 (1:1 ~ 1:5)
    int         RespirationApneaDuration;     //!< Unit: sec. The value is 0~60 sec.
    int         RespirationApneaCycle;        //!< Unit: sec. The value is 1~10 minute.
    char        Reserved[12];                 //!< internal use
} ECG_WAVEFORM;

/// \anchor structPPG_WAVEFORM
/// \brief Define a structure of PPG waveform setting
typedef struct {
    int                 WaveformType;                //!< ::PPGWaveformType
    double              Frequency;                   //!< Unit: Hz
    double              VolDC;                       //!< Unit: mV
    double              VolSP;                       //!< Unit: mV
    double              VolDN;                       //!< Unit: mV
    double              VolDP;                       //!< Unit: mV
    double              ACOffset;                    //!< Unit: mV; the sum of the VolSP(AC) and ACOffset must less than or equal to 30mV
    int                 TimeSP;                      //!< Unit: ms
    int                 TimeDN;                      //!< Unit: ms
    int                 TimeDP;                      //!< Unit: ms
    int                 TimePeriod;                  //!< Unit: ms
    int                 SyncPulse;                   //!< ::SyncPulse
    int                 Inverted;                    //!< ::PPGInverted
    double              NoiseAmplitude;              //!< Unit: mV. The max noise amplitude is 2.00 mV
    int                 NoiseFrequency;              //!< ::PPGNoiseFrequency
    int                 RespirationMode;             //!< Holds a combination of ::RespirationMode enum values
    int                 RespirationRate;             //!< Unit: BrPM
    int                 RespirationVariation;        //!< Unit: -16~16% percent
    int                 RespirationInExhaleRatio;    //!< inhale:exhale ratio; the supported value is 1~5 (1:1 ~ 1:5)
    int                 RespirationApneaDuration;    //!< Unit: sec. The value is 0~60 sec.
    int                 RespirationApneaCycle;       //!< Unit: sec. The value is 1~10 minute.
    char                Reserved[12];                //!< internal use
} PPG_WAVEFORM;

typedef struct {
    double      Amplitude;        //!< Unit: mV
    double      FrequencyStart;   //!< Unit: Hz
    double      FrequencyFinish;  //!< Unit: Hz
    int         Duration;         //!< Unit: second
} FREQUENCY_SCAN;

typedef struct {
    double      Amplitude;        //!< Unit: mV
    double      DC;               //!< Unit: mV; ECG: -500mV ~ +500mV, PPG: 0mV ~ 3000mV
    int         SyncPulse;        //!< ::SyncPulse
    double      FrequencyStart;   //!< Unit: Hz
    double      FrequencyFinish;  //!< Unit: Hz
    int         Duration;         //!< Unit: second
} FREQUENCY_SCAN2;

typedef struct {
    double                SampleRate;   //!< sampling frequency
    int                   Size;         //!< the number of points for AC and DC
    int                   SyncPulse;    //!< ::SyncPulse
    double                *AC;          //!< the array of AC data; for PPG, the range is 0~30
    double                *DC;          //!< the array of DC data; for PPG, the range is 0~3000
    OutputSignalCallback  cb;
} PLAY_RAW_DATA;

typedef struct {
    unsigned char       PulseLEDTable[8];      //!< ::LEDPulse
    unsigned short      PulseGroupInterval;    //!< Unit: us; the interval between each group of pulses; if the value is 0, it's IR-first mode (PulseLEDTable[0] must be IR).
} PPG_LED_PULSE_GROUP_SETTING;

//
// Initialization & Cleanup
//

///
/// Initialization; register connection event listener
///
/// During initialization, it will try to connect a device. If a device is found,
/// the cb function will be called. After then, if a device is disconnected,
/// the cb will be called again to notify the disconnection event. 
///
/// @param[in] cb  A callback function that is used to receive the connection or disconnection event
///
WHALETEQ_API
bool
WTQInit (
    ConnectedCallback cb
);

///
/// Connect the device.
///
/// @param[in] portNumber            Device COM port number; -1 means the port number is automatically selected
/// @param[in] millisecondsTimeout   Connection timeout; the number of milliseconds to connect, or -1 to wait indefinitely
/// @return true if the device is connected; false if the time-out interval elapsed and 
///         the device is still not connected
///
WHALETEQ_API
bool
WTQConnect (
    unsigned int portNumber,
    unsigned int millisecondsTimeout
);

///
/// Disconnect the device and clean up library resource
///
WHALETEQ_API
void
WTQFree (
    void
);

//
// Device Configurations
//

///
/// Get device information (main module)
///
/// @param[out] modelInfo     A pointer to a ::MODEL_INFORMATION structure
///
WHALETEQ_API
bool
WTQGetDeviceInformation (
    MODEL_INFORMATION *modelInfo
);

///
/// Get device serial number (main module)
///
/// @return a null-terminated string of serial number text; DO NOT free the returned string
///
WHALETEQ_API
char*
WTQGetSerialNumber (
    void
);

///
/// Get device information (PPG module)
///
/// @param[out] modelInfo     A pointer to a ::MODEL_INFORMATION structure
///
WHALETEQ_API
bool
WTQGetPPGDeviceInformation (
    MODEL_INFORMATION *modelInfo
);

///
/// Get device serial number (PPG module)
///
/// @return a null-terminated string of serial number text; DO NOT free the returned string
///
WHALETEQ_API
char*
WTQGetPPGSerialNumber (
    void
);

///
/// Get device FW/HW information
///
/// @param[out] hwlInfo     A pointer to a ::HW_INFORMATION structure
///
WHALETEQ_API
bool
WTQGetHWInformation (
    HW_INFORMATION *hwInfo
);

WHALETEQ_API
bool
WTQGetPPGHWInformation (
    HW_INFORMATION *hwInfo
);

//
// PPG Module Sampling
//
///
/// Enable Sampling Mode
///
/// @param[in] mode           \ref PPGSampling
/// @param[in] cbSamplingData A callback function to receive the sampling data
/// 
WHALETEQ_API
bool
WTQEnableSampling (
    PPGSampling mode,
    SamplingCallback cbSamplingData
);

WHALETEQ_API
bool
WTQStartSampling (
    SamplingErrorCallback cbError
);

///
/// Stop sampling and reset all sampling mode; later, users need to call WTQEnableSampling again to restart the sampling mode
/// 
WHALETEQ_API
void
WTQDisableSampling (
    void
);

///
/// DUT Signal Strength Detection (only for Finger module)
///
WHALETEQ_API
bool
WTQEnableDUTSignalDetection (
    bool enable,
    DUTSignalDetectionCallback cb
);

//
// RLD Test
//

///
/// Enable RLD function
///
/// Once the RLD measurement is completed, it's required to disable RLD 
///
/// @param[in] enable  true to enable RLD; otherwises, the RLD is disabled
///
WHALETEQ_API
bool
WTQEnableRLD (
    bool enable
);

///
/// Measure RLD N1/N2 voltage
/// 
/// It's required add delay (ex: 1 second) during the calls to WTQEnableRLD and the first WTQReadRLD
///
WHALETEQ_API
bool
WTQReadRLD (
    double *N1,
    double *N2
);

//
// PPG AC/ DC Position
//

///
/// Enable AC above DC
///
/// By default, the PPG AC signal is below DC.
/// 
/// @param[in] enable  true if AC is above DC; otherwises, AC is below DC
///
WHALETEQ_API
void
WTQEnableACAboveDC (
    bool enable
);

//
// ECG Signal Output Control
//

WHALETEQ_API
bool
WTQDeviceEnableImpedance (
    int impedance         //!< ::ECGImpedance
);

WHALETEQ_API
bool
WTQDeviceSetElectrode (
    int electrode         //!< ::Electrode
);

WHALETEQ_API
bool
WTQDeviceSetDCOffset (
    int dcOffset          //!< The DCOffset mode is fixed, not variable. The valid value is 300| 0| -300.
);

WHALETEQ_API
bool
WTQDeviceEnablePacing (
    int pacing            //!< ::ECGPacingEnable
);

///
/// ECG Respiration (resistance)
///
WHALETEQ_API
bool
WTQDeviceEnableRespiration (
    int respiration       //!< ::RespirationMode; the value must be RespirationModeOff or RespirationModeResistance
);

//
// PPG Module LED Configuration
//

//
// Configurations of pulse groups; only effective for the PPG modules of single-LED or two-led simulate 3 channels (WAP2005/ WAP2006/ WAP2007/ WAP2008)
//
WHALETEQ_API
bool
WTQReadLEDPulseGroupSetting (
    PPG_LED_PULSE_GROUP_SETTING *pulseGroupSetting
);

WHALETEQ_API
bool
WTQWriteLEDPulseGroupSetting (
    PPG_LED_PULSE_GROUP_SETTING *pulseGroupSetting
);

//
// Ambient Light; only effective for PPG module WAP2012
//
WHALETEQ_API
int
WTQGetLEDAmbientLightMode (
    void
);

WHALETEQ_API
bool
WTQSetLEDAmbientLightMode (
    int mode              //!< PPGAmbientLightMode
);

//
// Output waveform in device alone mode (WTQOutput*)
//

///
/// Output ECG
///
/// @param[in] waveform     ECG waveform setting.
/// @param[in] cb           A callback function to pass waveform point data.
///
WHALETEQ_API
bool
WTQOutputECG (
    ECG_WAVEFORM *waveform,
    OutputSignalCallback cb
);

///
/// Output ECG and PPG
///
/// @param[in] timeDiffPTTPeak The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform     ECG waveform setting
/// @param[in] ppgWaveform     PPG waveform setting
/// @param[in] cbECG           A callback function to pass ECG waveform point data\n 
///                            <B>Note:</B> the point value unit is uV
/// @param[in] cbPPG           A callback function to pass PPG waveform point data\n
///                            <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQOutputECGAndPPG (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgWaveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPG
);

///
/// Output ECG and two PPG
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting
/// @param[in] ppgChannel2Waveform     PPG waveform setting
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQOutputECGAndPPGEx (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPGChannel1,
    OutputSignalCallback cbPPGChannel2
);

///
/// Output ECG and PPG three channels
///
/// For single-LED PPG module, this should be used instead of WTQOutputECGAndPPG or WTQOutputECGAndPPGEx.
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting (R)
/// @param[in] ppgChannel2Waveform     PPG waveform setting (IR)
/// @param[in] ppgChannel3Waveform     PPG waveform setting (G)
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel3           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQOutputECGAndPPG3 (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPGChannel1,
    OutputSignalCallback cbPPGChannel2,
    OutputSignalCallback cbPPGChannel3
);

///
/// Output PPG (only one channel)
///
/// @param[in] channelNo   enum ::PPGChannel. Specify which channel to output.
/// @param[in] waveform    PPG waveform setting.
/// @param[in] cb          A callback function to pass PPG waveform point data.\n
///                        <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQOutputPPG (
    PPGChannel channelNo,
    PPG_WAVEFORM *waveform,
    OutputSignalCallback cb
);

///
/// Output PPG (two channels)
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQOutputPPGEx (
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    OutputSignalCallback cbChannel1,
    OutputSignalCallback cbChannel2
);

///
/// Output PPG (three channels)
///
/// For single-LED PPG module, this should be used instead of WTQOutputPPG or WTQOutputPPGEx.
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] channel3Waveform    PPG waveform setting for channel-3.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
/// @param[in] cbChannel3          A callback function to pass PPG waveform point data for channel-3.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQOutputPPG3 (
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform,
    OutputSignalCallback cbChannel1,
    OutputSignalCallback cbChannel2,
    OutputSignalCallback cbChannel3
);

///
/// Frequency Scan; output sine waveform with varying frequency
/// 
/// @param[in]  scan        struct ::FREQUENCY_SCAN
/// @param[in]  cb          A callback function to pass waveform point data\n 
///                         <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQOutputFrequencyScan (
    FREQUENCY_SCAN *scan,
    OutputSignalCallback cb
);

///
/// Frequency Scan; output sine waveform with varying frequency
/// 
/// @param[in]  scan        struct ::FREQUENCY_SCAN2
/// @param[in]  channelNo   enum ::PPGChannel. Specify which channel to output
/// @param[in]  cb          A callback function to pass waveform point data\n 
///                         <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQOutputFrequencyScanPPG (
    PPGChannel channelNo,
    FREQUENCY_SCAN2 *scan,
    OutputSignalCallback cb
);

//
// Play Raw Data (WTQWaveformPlayerOutput*)
//

///
/// Play Raw Data to ECG channel
///
/// @param[in]  data           enum ::PLAY_RAW_DATA. ECG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECG (
    PLAY_RAW_DATA *data
);

/// 
/// Play Raw Data to ECG and PPG one channel
///
/// @param[in]  ecgData        enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  channelNo      enum ::PPGChannel. Specify which channel to output
/// @param[in]  ppgData        enum ::PLAY_RAW_DATA. PPG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPG (
    PLAY_RAW_DATA *ecgData,
    PPGChannel channelNo,
    PLAY_RAW_DATA *ppgData
);

/// 
/// Play Raw Data to ECG and PPG two channels
///
/// @param[in]  ecgData          enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPGEx (
    PLAY_RAW_DATA *ecgData,
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data
);

/// 
/// Play Raw Data to ECG and PPG three channels
///
/// For single-LED PPG module, this should be used instead of WTQWaveformPlayerOutputECGAndPPG or WTQWaveformPlayerOutputECGAndPPGEx.
///
/// @param[in]  ecgData          enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data (R)
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data (IR)
/// @param[in]  ppgChannel3Data  enum ::PLAY_RAW_DATA. PPG channel-3 raw data (G)
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPG3 (
    PLAY_RAW_DATA *ecgData,
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data,
    PLAY_RAW_DATA *ppgChannel3Data
);

///
/// Play Raw Data to PPG one channel
///
/// @param[in]  channelNo      enum ::PPGChannel. Specify which channel to output
/// @param[in]  ppgData        enum ::PLAY_RAW_DATA. PPG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPG (
    PPGChannel channelNo,
    PLAY_RAW_DATA *ppgData
);

/// 
/// Play Raw Data to PPG two channels
///
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPGEx (
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data
);

/// 
/// Play Raw Data to PPG three channels
///
/// For single-LED PPG module, this should be used instead of WTQWaveformPlayerOutputPPG or WTQWaveformPlayerOutputPPGEx.
///
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data (R)
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data (IR)
/// @param[in]  ppgChannel3Data  enum ::PLAY_RAW_DATA. PPG channel-3 raw data (G)
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPG3 (
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data,
    PLAY_RAW_DATA *ppgChannel3Data
);

//
// Output waveform in play-raw mode (WTQPlay*)
//
// WTQPlay* functions are mainly used to support modulation respiration (BaselineModulation/ AmplitudeModulation/ FrequencyModulation).
// If you don't need modulation respiration function, WTQOutput* are suggested for stability.
//

///
/// Output ECG
///
/// @param[in] waveform     ECG waveform setting.
/// @param[in] cb           A callback function to pass waveform point data.
///
WHALETEQ_API
bool
WTQPlayECG (
    ECG_WAVEFORM *waveform,
    OutputSignalCallback cb
);

///
/// Output ECG and PPG
///
/// @param[in] timeDiffPTTPeak The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform     ECG waveform setting
/// @param[in] ppgWaveform     PPG waveform setting
/// @param[in] cbECG           A callback function to pass ECG waveform point data\n 
///                            <B>Note:</B> the point value unit is uV
/// @param[in] cbPPG           A callback function to pass PPG waveform point data\n
///                            <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQPlayECGAndPPG (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgWaveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPG
);

///
/// Output ECG and two PPG
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting
/// @param[in] ppgChannel2Waveform     PPG waveform setting
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQPlayECGAndPPGEx (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPGChannel1,
    OutputSignalCallback cbPPGChannel2
);

///
/// Output ECG and PPG three channels
///
/// For single-LED PPG module, this should be used instead of WTQOutputECGAndPPG or WTQOutputECGAndPPGEx.
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting (R)
/// @param[in] ppgChannel2Waveform     PPG waveform setting (IR)
/// @param[in] ppgChannel3Waveform     PPG waveform setting (G)
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel3           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQPlayECGAndPPG3 (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform,
    OutputSignalCallback cbECG,
    OutputSignalCallback cbPPGChannel1,
    OutputSignalCallback cbPPGChannel2,
    OutputSignalCallback cbPPGChannel3
);

///
/// Output PPG (only one channel)
///
/// @param[in] channelNo   enum ::PPGChannel. Specify which channel to output.
/// @param[in] waveform    PPG waveform setting.
/// @param[in] cb          A callback function to pass PPG waveform point data.\n
///                        <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool
WTQPlayPPG (
    PPGChannel channelNo,
    PPG_WAVEFORM *waveform,
    OutputSignalCallback cb
);

///
/// Output PPG (two channels)
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQPlayPPGEx (
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    OutputSignalCallback cbChannel1,
    OutputSignalCallback cbChannel2
);

///
/// Output PPG (three channels)
///
/// For single-LED PPG module, this should be used instead of WTQOutputPPG or WTQOutputPPGEx.
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] channel3Waveform    PPG waveform setting for channel-3.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
/// @param[in] cbChannel3          A callback function to pass PPG waveform point data for channel-3.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool
WTQPlayPPG3 (
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform,
    OutputSignalCallback cbChannel1,
    OutputSignalCallback cbChannel2,
    OutputSignalCallback cbChannel3
);

WHALETEQ_API
void
WTQWaveformPlayerLoop (
    bool loop
);

///
/// Stop the device outputting waveform
///
WHALETEQ_API
void
WTQStopOutputWaveform (
    void
);

///
/// Stop playing raw data
///
WHALETEQ_API
void
WTQStopPlayRawData (
    void
);

//
// Standalone Mode Setting Control
//

///
/// Read/Write waveform from/to device
///
/// @param[in] mode             enum ::StandAloneMode. Specify which mode to read from.      
/// @returns enum ::ModeType
/// 
WHALETEQ_API
int
WTQReadStandaloneModeType (
    int mode
);

///
/// Read ECG waveform from device
///
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] waveform        ECG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadECGModeFromStandaloneMode (
    int mode,
    ECG_WAVEFORM *waveform
);

///
/// Write ECG waveform to device
///
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] waveform        ECG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWriteECGModeToStandaloneMode (
    int mode,
    ECG_WAVEFORM *waveform
);

///
/// Read ECG and PPG waveform from device
///
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform     ECG waveform setting.
/// @param[out] ppgWaveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModeFromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Write ECG and PPG waveform to device
///
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform     ECG waveform setting.
/// @param[out] ppgWaveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModeToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Read ECG and PPG waveform from device
///
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting.
/// @param[out] ppgChannel1Waveform     PPG waveform setting.
/// @param[out] ppgChannel2Waveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModeExFromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform
);

///
/// Write ECG and two PPG waveform to device
///
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting.
/// @param[out] ppgChannel1Waveform     PPG waveform setting.
/// @param[out] ppgChannel2Waveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModeExToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform
);

///
/// Read ECG and PPG waveform from device (only supported in one LED-RED mode)
///
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting
/// @param[out] ppgChannel1Waveform     PPG waveform setting
/// @param[out] ppgChannel2Waveform     PPG waveform setting
/// @param[out] ppgChannel3Waveform     PPG waveform setting
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModePPG3FromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform
);

///
/// Write ECG and two PPG waveform to device (only supported in one LED-RED mode)
///
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting
/// @param[out] ppgChannel1Waveform     PPG waveform setting
/// @param[out] ppgChannel2Waveform     PPG waveform setting
/// @param[out] ppgChannel3Waveform     PPG waveform setting
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModePPG3ToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform
);

///
/// Read SPO2 waveform from device
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1.
/// @param[out] channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQReadSPO2ModeFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Write SPO2 waveform to device
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to write to.
/// @param[in]  channel1Waveform     PPG waveform setting for channel-1.
/// @param[in]  channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQWriteSPO2ModeToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Read SPO2 waveform from device (only supported in one LED-RED mode)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQReadSPO2ModePPG3FromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Write SPO2 waveform to device (only supported in one LED-RED mode)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQWriteSPO2ModePPG3ToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Read PPG waveform from device (only one LED)
///
/// @param[in]  mode                enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] ppgWaveform         PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModeFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Write PPG waveform to device (only one LED)
///
/// @param[in]  mode                enum ::StandAloneMode. Specify which mode to write to.
/// @param[in]  ppgWaveform         PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModeToStandaloneMode (
    int mode,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Read PPG waveform from device (two LED)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1.
/// @param[out] channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModeExFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Write PPG waveform to device (two LED)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[in]  channel1Waveform     PPG waveform setting for channel-1.
/// @param[in]  channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModeExToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Read PPG waveform from device (only supported in one LED-RED mode)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModePPG3FromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Write PPG waveform to device (only supported in one LED-RED mode)
///
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModePPG3ToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Restore the LED level and Trigger level of PPG module to the factory settings
///
WHALETEQ_API
bool
WTQRestoreFactorySetting (
    void
);

///
/// Read PPG LED Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to read.
/// @param[out] level           PPG LED Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQReadPPGLedCalibrationSetting (
    PPGChannel channelNo,
    unsigned short *level
);

///
/// Write PPG LED Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to write.
/// @param[in]  level           PPG LED Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQWritePPGLedCalibrationSetting (
    PPGChannel channelNo,
    unsigned short level
);

///
/// Read PPG Trigger Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to read.
/// @param[out] level           PPG Trigger Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQReadPPGTriggerLevelCalibrationSetting (
    PPGChannel channelNo,
    unsigned short *level
);

///
/// Write PPG Trigger Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to write.
/// @param[in]  level           PPG Trigger Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQWritePPGTriggerLevelCalibrationSetting (
    PPGChannel channelNo,
    unsigned short level
);

//
// DLL Version
//
/// Get DLL file version
///
/// \return The version is 4-digits and are saved in each byte of unsigned int value.\n
///         For example, if the return value is 0x01020304, the dll version is 1.2.3.4.
WHALETEQ_API
unsigned int
WTQGetVersion (
    void
);

///
/// \brief Create synchronization signal
/// 
/// This API creates a manual-reset event to enable synchronized data output across multiple products. 
/// When the event is signaled, all products will output their signals simultaneously.
/// 
WHALETEQ_API
void *
WTQCreateSynchronizationSignal (
    void
);

///
/// \brief Set the synchronization event
/// 
/// This API sets the synchronization event for the product. 
/// Subsequent signal outputs will wait for this event to be signaled.
/// 
WHALETEQ_API
void
WTQSetSynchronizationSignal (
    void *syncObject
);

///
/// \brief Signal the synchronization event
/// 
/// This API signals the synchronization event, triggering all products to begin waveform output simultaneously.
///
WHALETEQ_API
void
WTQSynchronizationSignalSetEvent (
    void *syncObject
);

///
/// \brief Signal the synchronization event
/// 
/// Reset the synchronization event
/// 
WHALETEQ_API
void
WTQSynchronizationSignalResetEvent (
    void *syncObject
);
