# Ultrahuman Ring Testing System

A comprehensive GUI application for testing Ultrahuman rings using the Whaleteq device. This system automates BPM testing at different frequencies (60, 120, 180 BPM) and validates the ring's heart rate measurement accuracy.

## Features

- **Device Management**: Connect and manage Whaleteq device and Ultrahuman rings
- **Automated Testing**: Sequential BPM testing with configurable tolerances
- **Real-time Monitoring**: Live progress tracking and data visualization
- **Retry Mechanism**: Automatic retry on test failures (up to 3 attempts)
- **Web Interface**: Modern, responsive web-based GUI
- **Real-time Communication**: WebSocket-based real-time updates

## System Requirements

- Python 3.7+
- macOS/Linux/Windows
- Whaleteq AECG100 device
- Ultrahuman Ring with BLE capability
- Bluetooth adapter

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Whaleteq SDK is properly configured**:
   - The `whaleteq/SDK/` directory should contain the appropriate libraries for your platform
   - For macOS: `libaecg.a`
   - For Windows: `AECG100x64.dll` or `AECG100x86.dll`
   - For Linux: `libaecgx64.so` or similar

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5001
   ```

3. **Connect Devices**:
   - Click "Connect Whaleteq Device" to establish connection with the Whaleteq device
   - Enter the ring name (e.g., "UH_C71AAFFD5A88") and click "Connect Ring"

4. **Run Tests**:
   - Once both devices are connected, click "Start BPM Test Sequence"
   - The system will automatically run through the test sequence:
     - 60 BPM test (±2 BPM tolerance) - 30 seconds
     - 120 BPM test (±5 BPM tolerance) - 30 seconds  
     - 180 BPM test (±5 BPM tolerance) - 30 seconds

5. **View Results**:
   - Test progress and results are displayed in real-time
   - Final result will show "PASSED" or "REJECTED"
   - Detailed logs are available in the System Log section

## Test Sequence Details

### Test Stages
1. **60 BPM Test**: Target 60 BPM with ±2 BPM tolerance
2. **120 BPM Test**: Target 120 BPM with ±5 BPM tolerance
3. **180 BPM Test**: Target 180 BPM with ±5 BPM tolerance

### Test Process
1. Connect to Whaleteq device and ring
2. Enable CDT mode on the ring
3. For each test stage:
   - Generate PPG waveform at target BPM
   - Output waveform for 30 seconds
   - Collect heart rate data from ring
   - Validate measured BPM against target with tolerance
   - Retry up to 3 times if test fails
4. If all tests pass:
   - Write pass command (64) to ring
   - Wait 1.5 seconds
   - Disconnect from ring
   - Stop waveform output

### Retry Logic
- Each test stage can be retried up to 3 times
- If a stage fails after 3 retries, the entire test sequence fails
- Retry counter resets for each new stage

## File Structure

```
├── app.py                          # Flask backend application
├── templates/
│   └── index.html                  # Web interface
├── ultrahuman_ring_cdt.py         # Ring BLE communication
├── whaleteq/
│   ├── Sample Code/python/
│   │   ├── aecg100.py             # Whaleteq device interface
│   │   └── ppg_output_60_ppg_ch1.py # PPG waveform example
│   └── SDK/                       # Whaleteq SDK libraries
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## API Endpoints (WebSocket)

- `connect_whaleteq`: Connect to Whaleteq device
- `connect_ring`: Connect to Ultrahuman ring
- `start_test`: Start the BPM test sequence
- `disconnect_all`: Disconnect all devices

## Troubleshooting

### Common Issues

1. **Whaleteq Device Not Found**:
   - Ensure the device is powered on and connected via USB
   - Check that the correct SDK library is available for your platform
   - Verify USB permissions (Linux/macOS)

2. **Ring Connection Failed**:
   - Ensure Bluetooth is enabled
   - Check that the ring name is correct
   - Make sure the ring is not connected to other devices
   - Try restarting Bluetooth service

3. **Test Failures**:
   - Check ring placement and contact with skin
   - Ensure stable Bluetooth connection
   - Verify Whaleteq device is outputting correctly
   - Check for interference from other devices

4. **Permission Issues (Linux/macOS)**:
   ```bash
   # Add user to dialout group (Linux)
   sudo usermod -a -G dialout $USER
   
   # Grant Bluetooth permissions (macOS)
   # System Preferences > Security & Privacy > Privacy > Bluetooth
   ```

## Development

### Adding New Test Stages
To add new BPM test stages, modify the `test_stages` list in `app.py`:

```python
test_stages = [
    {'bpm': 60, 'tolerance': 2, 'name': '60 BPM'},
    {'bpm': 120, 'tolerance': 5, 'name': '120 BPM'},
    {'bpm': 180, 'tolerance': 5, 'name': '180 BPM'},
    {'bpm': 240, 'tolerance': 10, 'name': '240 BPM'},  # New stage
]
```

### Customizing Tolerances
Modify the tolerance values in the test stages configuration to adjust acceptable BPM ranges.

### Extending Ring Communication
The `UltrahumanRingCDT` class can be extended to support additional ring commands or data parsing.

## License

This project is for internal use and testing purposes.

## Support

For technical support or questions, please refer to the Whaleteq device documentation and Ultrahuman Ring specifications.