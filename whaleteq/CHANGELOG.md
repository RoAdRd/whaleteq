# WhaleTeq AECG100 SDK Changelog

**Test Environment:**
* Linux Kernel Version (Ubuntu): 6.8.0.49-generic
* Raspberry Pi Version: Raspberry Pi 4 Model B (4GB RAM)
* Raspberry Pi Linux Kernel Version: 5.10.103-v7l+ (32-bit), 6.1.21-v8+ (64-bit)
* macOS Version: macOS Sonoma 14.4.1

**IMPORTANT:**
1. the calling convention is _cdecl
2. If the PPG module WAP2005/ WAP2006 is connected, the Switch sampling function will be disabled 
3. PPG module WAP2012: to output ppg signals, it's suggested to use WTQ*PPGEx
4. only supported FW version 1.14.44.19 and later
5. the ECG play sample rate is limited to 20K in MacOS
6. (Linux/ Raspberry Pi/ macOS) if the devices can not be connected
   1. switch to root user
   2. make sure /var/lock directory is created
   3. remove all the files - /var/lock/whaleteq* and try again

## Version 1.0.5.1 - 2025-05-27
1. CHG: moved PPG AC below DC
2. NEW: added support new PPG module WAP2112
3. FIX: prevent potential hang on Linux

## Version 1.0.4.1 - 2024-12-18
1. CHG: the respiration algorithm can be multi selected
2. CHG: added support apnea in ECG and PPG respiration algorithm
3. NEW: added play data synchronization functionality

**IMPORTANT:**  
1. The *enum RespirationMode* is redefined; struct ECG_WAVEFORM.RespirationMode and struct PPG_WAVEFORM.RespirationMode hold a combination of ::RespirationMode enum values
2. The *struct PPG_WAVEFORM* is updated; added apnea settings

## Version 1.0.3.9 - 2024-11-20
1. FIX: failed to normally play data in MacOS; adjust the ECG play sample rate to 20K

## Version 1.0.3.7 - 2024-10-30
1. FIX: DC is incorrectly adjusted (PPG module WAP2012)
2. FIX: play data may be interrupted in some Linux environments

## Version 1.0.3.4 - 2024-09-10
1. FIX: failed to play data in MacOS

## Version 1.0.3.3 - 2024-08-22
1. FIX: incorrect ECG signal if PWTT respiration is enabled
2. NEW: added PPG noise frequency 0.5/ 1/ 2/ 3/ 5/ 10/ 25 Hz (only supported FW version 1.14.44.19 and later)
3. NEW: added Mac library
4. FIX: AC/ DC values are incorrect for PPG module WAP2012 (WTQWaveformPlayerOutputPPG*)

## Version 1.0.2.18 - 2023-02-08
1. FIX: AC/DC is not adjusted in WTQPlayECGAndPPGEx() (PPG module WAP2012)

## Version 1.0.2.16 - 2022-12-23
1. CHG: adjust DC levels to make PI more accurate (PPG module WAP2012)

## Version 1.0.2.15 - 2022-06-06
1. FIX: the measured PTTp becomes incorrect if BPM > 125
2. FIX: the time constant is incorrect for ECG Exponential waveform

## Version 1.0.2.14 - 2021-04-25
1. CHG: structure PPG_WAVEFORM is updated: 
   - Remove AmbientLight
2. NEW: added WTQSetLEDAmbientLightMode() to configure the ambient light mode for PPG module WAP2012
3. CHG: remove enum PPGSampling::FullPD
4. CHG: set the baseline of ECG waveforms (Rectangle Pulse/ Triangle Pulse/ Exponential) to zero voltage

## Version 1.0.2.13 - 2021-03-08
1. NEW: added support new PPG module WAP2008

## Version 1.0.2.12 - 2021-03-03
1. NEW: added Linux and Raspberry Pi library
2. FIX: exception occurred in Raspberry Pi x86 if WTQWaveformPlayerOutputPPG3() is called

## Version 1.0.2.11 - 2021-12-03
1. CHG: structure PPG_WAVEFORM is updated: 
   - Add AmbientLight
2. CHG: structure HW_INFORMATION is updated; add FW build version
3. CHG: removed structure PPG_LED_PULSE
4. CHG: structure PPG_LED_PULSE_GROUP_SETTING is redefined

## Version 1.0.2.10 - 2021-08-16
1. FIX: fail to call WTQWriteLEDPulseGroupSetting() immediately following the device is connected

## Version 1.0.2.8 - 2021-07-06
1. FIX: in PWTT mode, incorrectly output PPG Ch2 AC

## Version 1.0.2.7 - 2021-06-24
1. FIX: incorrect ECG exposential waveform; the pulse width is not necessary
2. CHG: update ECG_WAVEFORM and PPG_WAVEFORM structure
3. CHG: update enum PPGSampling
4. NEW: added support new PPG module WAP2007

**IMPORTANT:**
1. structure PPG_WAVEFORM is redefined; 
     - rename 'RespirationEnabled' to 'RespirationMode'; the value is enum RespirationMode
     - update 'RespirationVariation' type from 'double' to 'int'

2. structure ECG_WAVEFORM is redefined:
     - rename 'RespirationEnabled' to 'RespirationMode'; the value is enum RespirationMode

3. enum PPGSampling is redefined:
     - add PPGSamplingFullPD

## Version 1.0.2.2 - 2021-02-19
1. FIX: when play raw ECG data, if the respiration is enabled, the ampltude of the output signal is incorrect
2. CHG: when the device is connected, reset the output lead to RA
3. CHG: when the device is connected, reset the input impedance to off
4. CHG: when the device is connected, reset the respiration to off
5. CHG: when play raw ECG data, if all the DC data are zeros, pacing relay switch is kept disabled
6. NEW: added support new PPG module WAP2012/ WAP2014

## Version 1.0.2.1 - 2020-11-04
1. CHG: remove structure PPG_LED_PULSE_SETTING
2. CHG: remove WTQReadLEDPulseSetting(), WTQWriteLEDPulseSetting(); which are replaced with ReadLEDPulseGroupSetting() and WriteLEDPulseGroupSetting()

**IMPORTANT:**
1. structure PPG_LED_PULSE_SETTING is removed; WTQReadLEDPulseSetting() and WTQWriteLEDPulseSetting() are replaced with ReadLEDPulseGroupSetting() and WriteLEDPulseGroupSetting()

## Version 1.0.1.6 - 2020-07-20
1. remove ECG respiration Basic Level 500 ohm
2. fix: the zero voltage of ECG variable DC is not precisely configured

**IMPORTANT:**
1. structure PPG_WAVEFORM is redefined; 
     - update 'RespirationAmplitude' to 'RespirationVariation'
     - add RespirationInExhaleRatio field

## Version 1.0.1.5 - 2020-04-08
1. fix after the waveform outputting is stopped, there are unexpected short signals are generated
2. fix the play raw delay issue

## Version 1.0.1.4 - 2020-03-27
1. support new PPG module (only R LED); if the new R PPG module is connected, the Switch sampling function will be disabled
2. ECG noise: support 100Hz/ 120Hz
3. PPG noise: 100Hz/ 120Hz/ White Noise 
4. fix continuous WTQOutputECG calls results in no waveform generated
5. fix OutputSignalCallback function prototype is incorrect

## Version 1.0.1.3 - 2020-03-16
1. fix PTTp time is incorrectly output
2. update sample code
3. fix PTTp/PTTf is not correctly configured when saving waveforms to Mode A/B/C

## Version 1.0.1.1 - 2019-12-06
1. add 'PacingRate' data member in struct ECG_WAVEFORM; added support async pacing rate
2. added support ECG respiration; also support ECGRespirationBaseline::ECGRespirationBaseline500  
3. rename 'RespirationApnea' to 'RespirationApneaDuration' in struct ECG_WAVEFORM
4. add 'RespirationApneaCycle' in struct ECG_WAVEFORM; added support to config apnea cycle length
5. add *.lib files to \SDK
6. fix memory leak 
7. added support to PPG frequency scan; WTQOutputFrequencyScanPPG ()
8. added support PPG square waveform
9. add api: bool WTQConnect (unsigned int portNumber, unsigned int millisecondsTimeout)
10. fix play raw data failed in long-run test

**IMPORTANT:**
1. enum PPGWaveformType is redefined; PPGWaveformTypeSquare is inserted  
2. structure PPG_WAVEFORM is redefined; 
     - add ACOffset field; 
     - update RespirationRate type from 'double' to 'int' 
     - update 'RespirationSize' to 'RespirationAmplitude'
3. structure ECG_WAVEFORM is redefined

## Version 1.0.0.7 - 2018-08-07
1. initial