#!/usr/bin/env python3
"""
Ultrahuman Ring CDT Data Parser - v6 (CRC Check Removed)
Connects to Ultrahuman Ring via BLE, sends the required command sequence, 
searches for a valid record header (sync marker), and parses the data
without CRC validation to handle firmware inconsistencies.
"""

import asyncio
import struct
import logging
from typing import Optional
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# UUIDs for Ultrahuman Ring
CLI_WRITE_CHAR_UUID = "86F65001-F706-58A0-95B2-1FB9261E4DC7"
CDT_READ_CHAR_UUID = "86F66001-F706-58A0-95B2-1FB9261E4DC7"

# Constants for a SINGLE data record
PPG_REC_T_SIZE = 29
SINGLE_RECORD_LENGTH = 3 + PPG_REC_T_SIZE + 2  # Header (3) + Payload (29) + Footer (2) = 34

# The "Sync Marker" is the known header of a valid data record:
# Command ID (0x62) + Payload Length (29, as little-endian 0x1D00)
SYNC_MARKER = b'\x62\x1d\x00'

# Correct format string for the 29-byte ppg_rec_t struct
PPG_REC_T_FORMAT = "<BBHLLLLLLB"

class UltrahumanRingCDT:
    def __init__(self, device_name: str):
        self.device_name = device_name
        self.client: Optional[BleakClient] = None
        self.latest_data = {}
        self.data_buffer = bytearray()

    async def scan_and_connect(self) -> bool:
        logger.info(f"Scanning for device with name: '{self.device_name}'")
        device = await BleakScanner.find_device_by_name(self.device_name, timeout=20.0)
        
        if not device:
            logger.error(f"Device '{self.device_name}' not found.")
            return False
            
        logger.info(f"Found device: {device.name} ({device.address})")
        self.client = BleakClient(device)
        
        try:
            await self.client.connect(timeout=30.0)
            logger.info(f"Successfully connected to {device.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

    def notification_handler(self, sender: BleakGATTCharacteristic, data: bytearray):
        """
        Handles incoming BLE data by adding it to a buffer and processing it.
        """
        self.data_buffer.extend(data)
        logger.debug(f"Received {len(data)} bytes, buffer is now {len(self.data_buffer)} bytes.")
        self.process_buffer()

    def process_buffer(self):
        """
        Processes the internal data buffer by searching for valid records.
        """
        while True:
            marker_index = self.data_buffer.find(SYNC_MARKER)

            if marker_index == -1:
                logger.debug("No sync marker found in buffer. Waiting for more data.")
                break

            if marker_index > 0:
                logger.warning(f"Discarding {marker_index} bytes of unrecognized data before sync marker.")
                self.data_buffer = self.data_buffer[marker_index:]

            if len(self.data_buffer) < SINGLE_RECORD_LENGTH:
                logger.debug("Found a marker but the full record is not yet in buffer. Waiting for more data.")
                break
            
            record_data = self.data_buffer[:SINGLE_RECORD_LENGTH]
            self.data_buffer = self.data_buffer[SINGLE_RECORD_LENGTH:]

            self.parse_one_record(record_data)

    def parse_one_record(self, record_data: bytes):
        """
        Parses a single 34-byte record.
        CRC check has been REMOVED as requested.
        """
        logger.debug(f"Parsing record: {record_data.hex().upper()}")
        
        # Extract payload. It is the 29 bytes between the 3-byte header and 2-byte footer.
        payload = record_data[len(SYNC_MARKER):-2]
        
        # --- CRC VALIDATION REMOVED ---
        
        self.parse_ppg_rec_t(payload)

    def parse_ppg_rec_t(self, payload: bytes):
        """
        Parses the 29-byte ppg_rec_t struct from the payload.
        """
        try:
            unpacked_data = struct.unpack(PPG_REC_T_FORMAT, payload)
            
            self.latest_data = {
                'bpm': unpacked_data[0], 'spo2': unpacked_data[1], 'spo2_r': unpacked_data[2],
                'red_ac': unpacked_data[3], 'ir_ac': unpacked_data[4], 'red_dc': unpacked_data[5],
                'ir_dc': unpacked_data[6], 'red_pi': unpacked_data[7], 'ir_pi': unpacked_data[8],
                'spo2_quality': unpacked_data[9]
            }

            logger.info(
                f"✅ PARSED - HR: {self.latest_data['bpm']} BPM, SpO2: {self.latest_data['spo2']}% "
                f"(Quality: {self.latest_data['spo2_quality']})"
            )
            logger.debug(f"Full parsed data: {self.latest_data}")

        except struct.error as e:
            logger.error(f"FATAL: Could not unpack ppg_rec_t struct. Error: {e}")

    async def run(self):
        try:
            if not await self.scan_and_connect():
                return

            logger.info(f"Enabling notifications on {CDT_READ_CHAR_UUID}...")
            await self.client.start_notify(CDT_READ_CHAR_UUID, self.notification_handler)
            logger.info("✅ Notifications enabled.")
            
            logger.info("Sending pre-command sequence...")
            pre_command = b'\x02\x33\x28\x65\x68'
            await self.client.write_gatt_char(CLI_WRITE_CHAR_UUID, pre_command)
            logger.info("Pre-command sent. Waiting for 2 seconds...")
            await asyncio.sleep(2)
            
            logger.info("Sending CDT start command...")
            cdt_command = b'\x62\x01'
            await self.client.write_gatt_char(CLI_WRITE_CHAR_UUID, cdt_command)
            logger.info("✅ CDT start command sent successfully.")
            
            logger.info("🎧 Listening for CDT data... Press Ctrl+C to stop.")
            while self.client.is_connected:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"An error occurred in the main loop: {e}")
        finally:
            if self.client and self.client.is_connected:
                await self.client.disconnect()
            logger.info("Program finished.")

async def main():
    ring = UltrahumanRingCDT(device_name="UH_C71AAFFD5A88")
    await ring.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")