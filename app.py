#!/usr/bin/env python3
"""
Ultrahuman Ring Testing GUI Application
Flask backend API for testing rings with Whaleteq device
"""

import asyncio
import threading
import time
import sys
import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from ctypes import pointer
import logging

# Add the whaleteq sample code path to import aecg100
sys.path.append(os.path.join(os.path.dirname(__file__), 'whaleteq', 'Sample Code', 'python'))

from aecg100 import AECG100, get_lib_path, PPGChannel, OutputSignalCallback
from ultrahuman_ring_cdt import UltrahumanRingCDT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultrahuman_ring_test_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class RingTestController:
    def __init__(self):
        self.whaleteq_device = None
        self.ring_cdt = None
        self.is_testing = False
        self.test_results = {}
        self.current_test_stage = None
        self.retry_count = 0
        self.max_retries = 3
        
    def connect_whaleteq_device(self):
        """Connect to Whaleteq device"""
        try:
            self.whaleteq_device = AECG100(get_lib_path())
            if self.whaleteq_device.connect(-1, 5000):
                logger.info(f'Whaleteq device connected: {self.whaleteq_device.get_serial_number()} / {self.whaleteq_device.get_ppg_serial_number()}')
                return True
            else:
                logger.error('Failed to connect to Whaleteq device')
                return False
        except Exception as e:
            logger.error(f'Error connecting to Whaleteq device: {e}')
            return False
    
    def disconnect_whaleteq_device(self):
        """Disconnect from Whaleteq device"""
        if self.whaleteq_device:
            try:
                self.whaleteq_device.stop_output()
                self.whaleteq_device.free()
                self.whaleteq_device = None
                logger.info('Whaleteq device disconnected')
            except Exception as e:
                logger.error(f'Error disconnecting Whaleteq device: {e}')
    
    async def connect_ring(self, ring_name):
        """Connect to Ultrahuman ring"""
        try:
            self.ring_cdt = UltrahumanRingCDT(ring_name)
            success = await self.ring_cdt.scan_and_connect()
            if success:
                # Enable notifications and send commands
                await self.ring_cdt.client.start_notify(
                    self.ring_cdt.CDT_READ_CHAR_UUID, 
                    self.ring_cdt.notification_handler
                )
                
                # Send pre-command sequence
                pre_command = b'\x02\x33\x28\x65\x68'
                await self.ring_cdt.client.write_gatt_char(
                    self.ring_cdt.CLI_WRITE_CHAR_UUID, 
                    pre_command
                )
                await asyncio.sleep(2)
                
                # Send CDT start command
                cdt_command = b'\x62\x01'
                await self.ring_cdt.client.write_gatt_char(
                    self.ring_cdt.CLI_WRITE_CHAR_UUID, 
                    cdt_command
                )
                
                logger.info(f'Ring {ring_name} connected and CDT mode enabled')
                return True
            return False
        except Exception as e:
            logger.error(f'Error connecting to ring: {e}')
            return False
    
    def generate_waveform(self, bpm):
        """Generate PPG waveform for given BPM"""
        frequency = bpm / 60.0  # Convert BPM to frequency
        waveform = self.whaleteq_device.get_default_ppg_ch3_waveform()
        waveform.Frequency = frequency
        return waveform
    
    def start_waveform_output(self, bpm):
        """Start outputting waveform at specified BPM"""
        try:
            waveform = self.generate_waveform(bpm)
            success = self.whaleteq_device.output_ppg(
                PPGChannel.Channel3.value, 
                pointer(waveform), 
                OutputSignalCallback(0)
            )
            if success:
                logger.info(f'Started waveform output at {bpm} BPM')
            return success
        except Exception as e:
            logger.error(f'Error starting waveform output: {e}')
            return False
    
    def stop_waveform_output(self):
        """Stop waveform output"""
        try:
            self.whaleteq_device.stop_output()
            logger.info('Stopped waveform output')
        except Exception as e:
            logger.error(f'Error stopping waveform output: {e}')
    
    async def disconnect_ring(self):
        """Disconnect from ring"""
        if self.ring_cdt and self.ring_cdt.client and self.ring_cdt.client.is_connected:
            try:
                await self.ring_cdt.client.disconnect()
                logger.info('Ring disconnected')
            except Exception as e:
                logger.error(f'Error disconnecting ring: {e}')
    
    async def write_pass_command(self):
        """Write pass command (64) to ring"""
        if self.ring_cdt and self.ring_cdt.client and self.ring_cdt.client.is_connected:
            try:
                pass_command = bytes([64])
                await self.ring_cdt.client.write_gatt_char(
                    self.ring_cdt.CLI_WRITE_CHAR_UUID, 
                    pass_command
                )
                logger.info('Pass command (64) written to ring')
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f'Error writing pass command: {e}')

# Global controller instance
controller = RingTestController()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect_whaleteq')
def handle_connect_whaleteq():
    """Handle Whaleteq device connection"""
    emit('status_update', {'message': 'Connecting to Whaleteq device...', 'type': 'info'})
    
    success = controller.connect_whaleteq_device()
    if success:
        emit('whaleteq_connected', {'success': True, 'message': 'Whaleteq device connected successfully'})
    else:
        emit('whaleteq_connected', {'success': False, 'message': 'Failed to connect to Whaleteq device'})

@socketio.on('connect_ring')
def handle_connect_ring(data):
    """Handle ring connection"""
    ring_name = data.get('ring_name', '').strip()
    if not ring_name:
        emit('ring_connected', {'success': False, 'message': 'Please enter a ring name'})
        return
    
    emit('status_update', {'message': f'Scanning for ring: {ring_name}...', 'type': 'info'})
    
    # Run async ring connection in a separate thread
    def connect_ring_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(controller.connect_ring(ring_name))
            if success:
                socketio.emit('ring_connected', {'success': True, 'message': f'Ring {ring_name} connected successfully'})
            else:
                socketio.emit('ring_connected', {'success': False, 'message': f'Failed to connect to ring {ring_name}'})
        except Exception as e:
            socketio.emit('ring_connected', {'success': False, 'message': f'Error: {str(e)}'})
        finally:
            loop.close()
    
    threading.Thread(target=connect_ring_thread, daemon=True).start()

@socketio.on('start_test')
def handle_start_test():
    """Handle test start"""
    if not controller.whaleteq_device:
        emit('test_error', {'message': 'Whaleteq device not connected'})
        return
    
    if not controller.ring_cdt or not controller.ring_cdt.client or not controller.ring_cdt.client.is_connected:
        emit('test_error', {'message': 'Ring not connected'})
        return
    
    if controller.is_testing:
        emit('test_error', {'message': 'Test already in progress'})
        return
    
    # Start test in separate thread
    def test_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(run_test_sequence())
        except Exception as e:
            logger.error(f'Test error: {e}')
            socketio.emit('test_error', {'message': f'Test failed: {str(e)}'})
        finally:
            loop.close()
    
    threading.Thread(target=test_thread, daemon=True).start()

async def run_test_sequence():
    """Run the complete test sequence"""
    controller.is_testing = True
    controller.test_results = {}
    controller.retry_count = 0
    
    test_stages = [
        {'bpm': 60, 'tolerance': 2, 'name': '60 BPM'},
        {'bpm': 120, 'tolerance': 5, 'name': '120 BPM'},
        {'bpm': 180, 'tolerance': 5, 'name': '180 BPM'}
    ]
    
    try:
        for stage in test_stages:
            success = await run_test_stage(stage)
            if not success:
                if controller.retry_count < controller.max_retries:
                    controller.retry_count += 1
                    socketio.emit('test_retry', {
                        'stage': stage['name'], 
                        'retry': controller.retry_count,
                        'max_retries': controller.max_retries
                    })
                    # Retry the same stage
                    success = await run_test_stage(stage)
                
                if not success:
                    socketio.emit('test_failed', {
                        'message': f'Test failed at {stage["name"]} after {controller.max_retries} retries',
                        'results': controller.test_results
                    })
                    return
            
            controller.retry_count = 0  # Reset retry count for next stage
        
        # All tests passed
        socketio.emit('test_progress', {'message': 'All tests passed! Writing pass command...', 'type': 'success'})
        await controller.write_pass_command()
        await controller.disconnect_ring()
        controller.stop_waveform_output()
        
        socketio.emit('test_completed', {
            'message': 'Ring testing completed successfully - PASSED',
            'results': controller.test_results
        })
        
    except Exception as e:
        logger.error(f'Test sequence error: {e}')
        socketio.emit('test_error', {'message': f'Test sequence failed: {str(e)}'})
    finally:
        controller.is_testing = False

async def run_test_stage(stage):
    """Run a single test stage"""
    bpm = stage['bpm']
    tolerance = stage['tolerance']
    stage_name = stage['name']
    
    socketio.emit('test_progress', {
        'message': f'Starting {stage_name} test...', 
        'type': 'info',
        'stage': stage_name
    })
    
    # Start waveform output
    if not controller.start_waveform_output(bpm):
        return False
    
    # Wait for 30 seconds while collecting data
    for i in range(30):
        await asyncio.sleep(1)
        socketio.emit('test_progress', {
            'message': f'{stage_name} test in progress... {30-i}s remaining',
            'type': 'info',
            'countdown': 30-i,
            'stage': stage_name
        })
    
    # Stop waveform and get latest HR reading
    controller.stop_waveform_output()
    
    if not controller.ring_cdt.latest_data or 'bpm' not in controller.ring_cdt.latest_data:
        socketio.emit('test_progress', {
            'message': f'{stage_name} test failed - No HR data received',
            'type': 'error'
        })
        return False
    
    measured_bpm = controller.ring_cdt.latest_data['bpm']
    difference = abs(measured_bpm - bpm)
    passed = difference <= tolerance
    
    controller.test_results[stage_name] = {
        'target_bpm': bpm,
        'measured_bpm': measured_bpm,
        'difference': difference,
        'tolerance': tolerance,
        'passed': passed
    }
    
    if passed:
        socketio.emit('test_progress', {
            'message': f'{stage_name} test PASSED - Target: {bpm}, Measured: {measured_bpm}, Diff: {difference}',
            'type': 'success',
            'result': controller.test_results[stage_name]
        })
        return True
    else:
        socketio.emit('test_progress', {
            'message': f'{stage_name} test FAILED - Target: {bpm}, Measured: {measured_bpm}, Diff: {difference} (tolerance: ±{tolerance})',
            'type': 'error',
            'result': controller.test_results[stage_name]
        })
        return False

@socketio.on('disconnect_all')
def handle_disconnect_all():
    """Handle disconnection of all devices"""
    def disconnect_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(controller.disconnect_ring())
            controller.disconnect_whaleteq_device()
            socketio.emit('devices_disconnected', {'message': 'All devices disconnected'})
        except Exception as e:
            socketio.emit('status_update', {'message': f'Error during disconnection: {str(e)}', 'type': 'error'})
        finally:
            loop.close()
    
    threading.Thread(target=disconnect_thread, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)