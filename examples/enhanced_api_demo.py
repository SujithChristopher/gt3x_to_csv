#!/usr/bin/env python3
"""
Enhanced API Demo for GT3X Parser

This script demonstrates the new GT3XReader API with DataFrame support
and structured metadata handling.
"""

import sys
import os
sys.path.append('..')
from gt3x_parser import GT3XReader, GT3XParser, GT3XToCSV


def demo_enhanced_api():
    """Demonstrate the new enhanced API"""
    print("=== Enhanced GT3X Parser API Demo ===\n")
    
    # Create a mock GT3X file for testing
    from test_parser import create_mock_gt3x_file
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix='.gt3x', delete=False) as tmp:
        mock_gt3x_path = tmp.name
    
    try:
        create_mock_gt3x_file(mock_gt3x_path)
        
        # NEW API - Enhanced GT3XReader with context manager
        print("1. Using enhanced GT3XReader API:")
        with GT3XReader(mock_gt3x_path) as reader:
            # Access structured metadata
            print(f"   Device Serial: {reader.device_info.serial_number}")
            print(f"   Sample Rate: {reader.device_info.sample_rate} Hz")
            print(f"   Total Samples: {reader.recording_info.total_samples}")
            print(f"   Duration: {reader.recording_info.duration_hours:.2f} hours")
            
            # Get complete metadata as dictionary
            metadata = reader.metadata
            print(f"   Metadata keys: {list(metadata.keys())}")
            
            # Convert to different formats
            data_dict = reader.to_dict(calibrated=True)
            print(f"   Dictionary format - Keys: {list(data_dict.keys())}")
            print(f"   First sample: x={data_dict['x'][0]:.3f}, y={data_dict['y'][0]:.3f}, z={data_dict['z'][0]:.3f}")
            
            # Try pandas if available
            try:
                df = reader.to_pandas(calibrated=True)
                print(f"   Pandas DataFrame shape: {df.shape}")
                print(f"   DataFrame columns: {list(df.columns)}")
                print("   First few rows:")
                print(df.head(3))
            except ImportError:
                print("   Pandas not available - install with: pip install pandas")
            
            # Try polars if available  
            try:
                df_pl = reader.to_polars(calibrated=True)
                print(f"   Polars DataFrame shape: {df_pl.shape}")
                print(f"   Polars columns: {df_pl.columns}")
            except ImportError:
                print("   Polars not available - install with: pip install polars")
        
        print("\n" + "="*50 + "\n")
        
        # LEGACY API - Still works for backward compatibility
        print("2. Legacy API (still supported):")
        parser = GT3XParser(mock_gt3x_path)
        data = parser.parse()
        print(f"   Legacy format - Info keys: {list(data['info'].keys())}")
        print(f"   Activity samples count: {len(data['activity_samples'])}")
        print(f"   First sample: x={data['activity_samples'][0].x}, y={data['activity_samples'][0].y}, z={data['activity_samples'][0].z}")
        
        # Legacy CSV conversion
        csv_path = mock_gt3x_path.replace('.gt3x', '_legacy.csv')
        converter = GT3XToCSV()
        converter.convert(mock_gt3x_path, csv_path, actilife_format=True)
        print(f"   CSV created: {csv_path}")
        
        print("\n3. Comparison:")
        print("   Enhanced API Benefits:")
        print("   - Structured metadata with proper types")
        print("   - Multiple output formats (pandas, polars, dict)")
        print("   - Context manager for resource management")
        print("   - Calibrated vs raw data options")
        print("   - Better error handling")
        print("   - Type hints and documentation")
        
    finally:
        # Clean up
        if os.path.exists(mock_gt3x_path):
            os.remove(mock_gt3x_path)
        csv_path = mock_gt3x_path.replace('.gt3x', '_legacy.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)


def demo_dataframe_features():
    """Demonstrate DataFrame-specific features"""
    print("\n=== DataFrame Features Demo ===\n")
    
    from test_parser import create_mock_gt3x_file
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix='.gt3x', delete=False) as tmp:
        mock_gt3x_path = tmp.name
    
    try:
        create_mock_gt3x_file(mock_gt3x_path)
        
        with GT3XReader(mock_gt3x_path) as reader:
            print("DataFrame Options:")
            
            # Different combinations
            formats = [
                ("Raw values with timestamps", False, True),
                ("Calibrated values with timestamps", True, True), 
                ("Raw values without timestamps", False, False),
                ("Calibrated values without timestamps", True, False)
            ]
            
            for desc, calibrated, timestamps in formats:
                data = reader.to_dict(include_timestamps=timestamps, calibrated=calibrated)
                print(f"   {desc}:")
                print(f"     Keys: {list(data.keys())}")
                if data['x']:  # If we have data
                    print(f"     First X value: {data['x'][0]}")
                
    finally:
        if os.path.exists(mock_gt3x_path):
            os.remove(mock_gt3x_path)


if __name__ == "__main__":
    demo_enhanced_api()
    demo_dataframe_features()