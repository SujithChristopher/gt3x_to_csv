#!/usr/bin/env python3
"""
Test script for GT3X parser

This script tests the GT3X parser functionality without requiring actual GT3X files.
It creates mock data to verify the parsing logic works correctly.
"""

import struct
import zipfile
import tempfile
import os
from gt3x_parser import GT3XParser, GT3XToCSV


def create_mock_gt3x_file(filepath: str):
    """Create a mock GT3X file for testing"""
    
    # Create mock info.txt content
    info_content = """Serial Number: ABC123
Start Date: 1/1/2024
Start Time: 10:00:00
Stop Date: 1/1/2024  
Stop Time: 10:05:00
Sample Rate: 30
"""
    
    # Create mock log.bin with a simple activity record
    log_data = bytearray()
    
    # Create a simple ACTIVITY record (type 0)
    separator = 0x1E
    record_type = 0  # ACTIVITY
    timestamp = 1704110400  # Unix timestamp for 2024-01-01 10:00:00
    
    # Create mock activity payload (3 samples, 3 bytes each)
    payload = bytearray()
    # Sample 1: x=100, y=200, z=300 (simplified 12-bit packing)
    payload.extend([0x64, 0xC8, 0x2C])  # Mock 3-byte activity sample
    payload.extend([0x65, 0xC9, 0x2D])  # Mock 3-byte activity sample  
    payload.extend([0x66, 0xCA, 0x2E])  # Mock 3-byte activity sample
    
    payload_size = len(payload)
    
    # Build record header
    header = struct.pack('<BBIH', separator, record_type, timestamp, payload_size)
    
    # Calculate checksum (1's complement XOR)
    checksum = 0
    for byte in header + payload:
        checksum ^= byte
    checksum = (~checksum) & 0xFF
    
    # Combine header, payload, and checksum
    log_data.extend(header)
    log_data.extend(payload)
    log_data.append(checksum)
    
    # Create the GT3X zip file
    with zipfile.ZipFile(filepath, 'w') as zipf:
        zipf.writestr('info.txt', info_content)
        zipf.writestr('log.bin', bytes(log_data))


def test_parser():
    """Test the GT3X parser with mock data"""
    print("Testing GT3X parser...")
    
    # Create temporary mock GT3X file
    with tempfile.NamedTemporaryFile(suffix='.gt3x', delete=False) as tmp:
        mock_gt3x_path = tmp.name
    
    try:
        create_mock_gt3x_file(mock_gt3x_path)
        
        # Test parser
        parser = GT3XParser(mock_gt3x_path)
        data = parser.parse()
        
        print(f"Parsed info: {data['info']}")
        print(f"Number of activity samples: {len(data['activity_samples'])}")
        
        if data['activity_samples']:
            print("First few samples:")
            for i, sample in enumerate(data['activity_samples'][:5]):
                print(f"  Sample {i}: x={sample.x}, y={sample.y}, z={sample.z}")
        
        # Test CSV conversion
        csv_path = mock_gt3x_path.replace('.gt3x', '.csv')
        converter = GT3XToCSV()
        converter.convert(mock_gt3x_path, csv_path)
        
        # Read and display first few lines of CSV
        if os.path.exists(csv_path):
            print(f"\nCSV file created: {csv_path}")
            with open(csv_path, 'r') as f:
                lines = f.readlines()[:6]  # Header + first 5 data lines
                for line in lines:
                    print(f"  {line.strip()}")
            
            os.remove(csv_path)
        
        print("\nTest completed successfully!")
        
    finally:
        # Clean up
        if os.path.exists(mock_gt3x_path):
            os.remove(mock_gt3x_path)


def test_info_parsing():
    """Test info.txt parsing"""
    print("Testing info.txt parsing...")
    
    info_content = """Serial Number: TEST123
Start Date: 1/15/2024
Start Time: 14:30:00
Stop Date: 1/15/2024
Stop Time: 16:30:00
Sample Rate: 100
Subject Name: Test Subject
"""
    
    parser = GT3XParser("")  # Empty path for this test
    info = parser._parse_info_txt(info_content)
    
    print("Parsed info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    assert info['Serial Number'] == 'TEST123'
    assert info['Sample Rate'] == '100'
    print("Info parsing test passed!")


if __name__ == "__main__":
    test_info_parsing()
    test_parser()