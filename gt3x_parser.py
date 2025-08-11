import zipfile
import struct
import datetime
import csv
import os
from typing import Optional, List, Dict, Any, BinaryIO
from dataclasses import dataclass


@dataclass
class GT3XRecord:
    separator: int
    record_type: int
    timestamp: int
    payload_size: int
    payload: bytes
    checksum: int


@dataclass
class ActivitySample:
    x: int
    y: int
    z: int


class GT3XParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.info = {}
        self.activity_samples = []
        
    def parse(self) -> Dict[str, Any]:
        """Parse GT3X file and extract activity data"""
        with zipfile.ZipFile(self.file_path, 'r') as zip_file:
            # Parse info.txt for metadata
            if 'info.txt' in zip_file.namelist():
                info_content = zip_file.read('info.txt').decode('utf-8')
                self.info = self._parse_info_txt(info_content)
            
            # Parse log.bin for activity data
            if 'log.bin' in zip_file.namelist():
                log_data = zip_file.read('log.bin')
                self.activity_samples = self._parse_log_bin(log_data)
        
        return {
            'info': self.info,
            'activity_samples': self.activity_samples
        }
    
    def _parse_info_txt(self, content: str) -> Dict[str, str]:
        """Parse info.txt file for device metadata"""
        info = {}
        for line in content.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        return info
    
    def _parse_log_bin(self, data: bytes) -> List[ActivitySample]:
        """Parse log.bin binary data for activity samples"""
        samples = []
        offset = 0
        
        while offset < len(data):
            try:
                record = self._read_record(data, offset)
                if record is None:
                    break
                
                # Process ACTIVITY records (type 0 or type 26)
                if record.record_type == 0 or record.record_type == 26:
                    activity_samples = self._parse_activity_payload(record.payload)
                    samples.extend(activity_samples)
                
                offset += 8 + record.payload_size + 1  # header + payload + checksum
                
            except Exception as e:
                print(f"Error parsing record at offset {offset}: {e}")
                break
        
        return samples
    
    def _read_record(self, data: bytes, offset: int) -> Optional[GT3XRecord]:
        """Read a single record from binary data"""
        if offset + 8 >= len(data):
            return None
        
        # Read header (8 bytes)
        separator = data[offset]
        record_type = data[offset + 1]
        timestamp = struct.unpack('<I', data[offset + 2:offset + 6])[0]
        payload_size = struct.unpack('<H', data[offset + 6:offset + 8])[0]
        
        if offset + 8 + payload_size + 1 > len(data):
            return None
        
        # Read payload
        payload = data[offset + 8:offset + 8 + payload_size]
        
        # Read checksum
        checksum = data[offset + 8 + payload_size]
        
        # Verify checksum
        if not self._verify_checksum(data[offset:offset + 8], payload, checksum):
            print(f"Checksum verification failed at offset {offset}")
        
        return GT3XRecord(separator, record_type, timestamp, payload_size, payload, checksum)
    
    def _verify_checksum(self, header: bytes, payload: bytes, checksum: int) -> bool:
        """Verify record checksum using 1's complement XOR"""
        calculated = 0
        for byte in header + payload:
            calculated ^= byte
        calculated = (~calculated) & 0xFF
        return calculated == checksum
    
    def _parse_activity_payload(self, payload: bytes) -> List[ActivitySample]:
        """Parse activity samples from payload"""
        samples = []
        
        # GT3X activity samples can be in different formats
        # Try different sample formats based on payload size
        if len(payload) % 9 == 0:
            # 9 bytes per sample (3 * 3-byte values)
            samples = self._parse_9_byte_samples(payload)
        elif len(payload) % 6 == 0:
            # 6 bytes per sample (3 * 2-byte values)
            samples = self._parse_6_byte_samples(payload)
        elif len(payload) % 3 == 0:
            # 3 bytes per sample (packed 12-bit values)
            samples = self._parse_3_byte_samples(payload)
        else:
            print(f"Unknown activity payload format, size: {len(payload)}")
        
        return samples
    
    def _parse_9_byte_samples(self, payload: bytes) -> List[ActivitySample]:
        """Parse 9-byte per sample format (3 * 3-byte signed integers)"""
        samples = []
        for i in range(0, len(payload), 9):
            if i + 9 <= len(payload):
                # Each axis is 3 bytes, little-endian signed
                x = struct.unpack('<i', payload[i:i+3] + b'\x00')[0]
                if x >= 0x800000: x -= 0x1000000  # Convert to signed 24-bit
                
                y = struct.unpack('<i', payload[i+3:i+6] + b'\x00')[0]
                if y >= 0x800000: y -= 0x1000000
                
                z = struct.unpack('<i', payload[i+6:i+9] + b'\x00')[0]
                if z >= 0x800000: z -= 0x1000000
                
                samples.append(ActivitySample(x, y, z))
        return samples
    
    def _parse_6_byte_samples(self, payload: bytes) -> List[ActivitySample]:
        """Parse 6-byte per sample format (3 * 2-byte signed integers)"""
        samples = []
        for i in range(0, len(payload), 6):
            if i + 6 <= len(payload):
                x, y, z = struct.unpack('<3h', payload[i:i+6])
                samples.append(ActivitySample(x, y, z))
        return samples
    
    def _parse_3_byte_samples(self, payload: bytes) -> List[ActivitySample]:
        """Parse 3-byte per sample format (packed format)"""
        samples = []
        # This format needs more investigation based on actual GT3X specification
        # For now, try to parse as best as possible
        for i in range(0, len(payload), 3):
            if i + 3 <= len(payload):
                # Simple unpacking - may need adjustment
                byte1, byte2, byte3 = payload[i:i+3]
                samples.append(ActivitySample(byte1, byte2, byte3))
        return samples
    
    def _to_signed_12bit(self, value: int) -> int:
        """Convert 12-bit unsigned to signed value"""
        if value >= 2048:
            return value - 4096
        return value


class GT3XToCSV:
    def __init__(self):
        pass
    
    def convert(self, gt3x_path: str, csv_path: str, actilife_format: bool = True) -> None:
        """Convert GT3X file to CSV format"""
        print(f"Converting {gt3x_path} to {csv_path}...")
        
        parser = GT3XParser(gt3x_path)
        data = parser.parse()
        
        # Get conversion parameters
        start_time = self._parse_start_time(data['info'])
        sample_rate = self._get_sample_rate(data['info'])
        scale_factor = self._get_scale_factor(data['info'])
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            if actilife_format:
                # Write ActiLife-style header
                self._write_actilife_header(writer, data['info'])
                writer.writerow(['Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
            else:
                # Simple header
                writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
            
            # Write activity samples
            for i, sample in enumerate(data['activity_samples']):
                if actilife_format:
                    # Convert to g-force values
                    x_g = sample.x / scale_factor
                    y_g = sample.y / scale_factor
                    z_g = sample.z / scale_factor
                    writer.writerow([f'{x_g:.3f}', f'{y_g:.3f}', f'{z_g:.3f}'])
                else:
                    timestamp = start_time + datetime.timedelta(seconds=i / sample_rate)
                    writer.writerow([
                        timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                        sample.x,
                        sample.y,
                        sample.z
                    ])
        
        print(f"Conversion complete. {len(data['activity_samples'])} samples written.")
    
    def _parse_start_time(self, info: Dict[str, str]) -> datetime.datetime:
        """Parse start time from info dictionary"""
        start_date = info.get('Start Date', '')
        start_time = info.get('Start Time', '')
        
        # Handle Windows ticks format (common in GT3X files)
        if start_date.isdigit():
            try:
                # Convert Windows ticks to datetime
                # Windows ticks = 100-nanosecond intervals since 1/1/0001 12:00am
                ticks = int(start_date)
                epoch_ticks = 621355968000000000  # Ticks between 1/1/0001 and 1/1/1970
                unix_timestamp = (ticks - epoch_ticks) / 10000000.0
                return datetime.datetime.utcfromtimestamp(unix_timestamp)
            except (ValueError, OSError):
                print(f"Could not parse Windows ticks: {start_date}")
        
        # Handle standard date/time format
        elif start_date and start_time:
            datetime_str = f"{start_date} {start_time}"
            try:
                return datetime.datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S')
            except ValueError:
                try:
                    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f"Could not parse start time: {datetime_str}")
        
        return datetime.datetime.now()
    
    def _get_sample_rate(self, info: Dict[str, str]) -> float:
        """Get sample rate from info dictionary"""
        sample_rate = info.get('Sample Rate', '30')
        try:
            return float(sample_rate)
        except ValueError:
            print(f"Could not parse sample rate: {sample_rate}, defaulting to 30 Hz")
            return 30.0
    
    def _get_scale_factor(self, info: Dict[str, str]) -> float:
        """Get acceleration scale factor from info dictionary"""
        scale = info.get('Acceleration Scale', '256.0')
        try:
            return float(scale)
        except ValueError:
            print(f"Could not parse acceleration scale: {scale}, defaulting to 256.0")
            return 256.0
    
    def _write_actilife_header(self, writer, info: Dict[str, str]):
        """Write ActiLife-style header to CSV"""
        # Parse start time for header
        start_time = self._parse_start_time(info)
        sample_rate = int(self._get_sample_rate(info))
        
        writer.writerow([f'------------ Data File Created By ActiGraph GT3X+ ActiLife v6.11.9 Firmware v{info.get("Firmware", "1.7.2")} date format d/MM/yyyy at {sample_rate} Hz  Filter Normal -----------'])
        writer.writerow([f'Serial Number: {info.get("Serial Number", "")}'])
        writer.writerow([f'Start Time {start_time.strftime("%H:%M:%S")}'])
        writer.writerow([f'Start Date {start_time.strftime("%d/%m/%Y")}'])
        writer.writerow(['Epoch Period (hh:mm:ss) 00:00:00'])
        writer.writerow([f'Download Time {start_time.strftime("%H:%M:%S")}'])  # Simplified
        writer.writerow([f'Download Date {start_time.strftime("%d/%m/%Y")}'])  # Simplified
        writer.writerow(['Current Memory Address: 0'])
        writer.writerow([f'Current Battery Voltage: {info.get("Battery Voltage", "4.18")}     Mode = 12'])
        writer.writerow(['--------------------------------------------------'])


def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python gt3x_parser.py <input.gt3x> <output.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    converter = GT3XToCSV()
    converter.convert(input_file, output_file)


if __name__ == "__main__":
    main()