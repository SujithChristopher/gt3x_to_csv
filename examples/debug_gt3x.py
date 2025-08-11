import zipfile
import struct

def find_activity_records(log_data):
    records = []
    offset = 0
    
    while offset < len(log_data):
        if offset + 8 >= len(log_data):
            break
            
        separator = log_data[offset]
        if separator != 0x1E:
            offset += 1
            continue
            
        record_type = log_data[offset + 1]
        timestamp = struct.unpack('<I', log_data[offset + 2:offset + 6])[0]
        payload_size = struct.unpack('<H', log_data[offset + 6:offset + 8])[0]
        
        if offset + 8 + payload_size + 1 > len(log_data):
            break
            
        records.append((offset, record_type, timestamp, payload_size))
        offset += 8 + payload_size + 1
    
    return records

with zipfile.ZipFile('test_file.gt3x', 'r') as zip_file:
    log_data = zip_file.read('log.bin')
    records = find_activity_records(log_data)
    
    print(f'Total records found: {len(records)}')
    
    record_types = {}
    for offset, rec_type, timestamp, payload_size in records:
        if rec_type not in record_types:
            record_types[rec_type] = 0
        record_types[rec_type] += 1
    
    print('Record types found:')
    for rec_type, count in sorted(record_types.items()):
        print(f'  Type {rec_type}: {count} records')
    
    # Find first activity record (type 0)
    activity_records = [r for r in records if r[1] == 0]
    if activity_records:
        print(f'\nFirst activity record (type 0):')
        offset, rec_type, timestamp, payload_size = activity_records[0]
        print(f'Offset: {offset}, Timestamp: {timestamp}, Payload size: {payload_size}')
        
        payload = log_data[offset + 8:offset + 8 + payload_size]
        print(f'Payload preview (hex): {payload[:30].hex()}')
        print(f'Payload size: {len(payload)} bytes')
        
        # Try to parse as different formats
        print(f'Samples if 9-byte format: {payload_size // 9}')
        print(f'Samples if 6-byte format: {payload_size // 6}')
        print(f'Samples if 3-byte format: {payload_size // 3}')
    else:
        print('No activity records (type 0) found!')
    
    # Check type 26 records (might be activity data in newer format)
    type26_records = [r for r in records if r[1] == 26]
    if type26_records:
        print(f'\nFirst type 26 record:')
        offset, rec_type, timestamp, payload_size = type26_records[0]
        print(f'Offset: {offset}, Timestamp: {timestamp}, Payload size: {payload_size}')
        
        payload = log_data[offset + 8:offset + 8 + payload_size]
        print(f'Payload preview (hex): {payload[:30].hex()}')
        print(f'Payload size: {len(payload)} bytes')
        
        # Analyze payload structure
        if payload_size >= 6:
            # Try parsing as 2-byte signed integers (common format)
            import struct
            values = struct.unpack('<' + 'h' * (payload_size // 2), payload[:payload_size//2*2])
            print(f'As 2-byte signed integers: {values[:10]}...')
        
        # Check if it's consistent with 100 Hz sample rate
        samples_per_second = 100  # From info.txt
        if payload_size % (samples_per_second * 6) == 0:  # 6 bytes per sample (3 axes * 2 bytes)
            print(f'Could be {payload_size // 6} samples at 6 bytes per sample')
        elif payload_size % (samples_per_second * 2) == 0:  # 2 bytes per axis
            print(f'Could be {payload_size // 2} values at 2 bytes per value')