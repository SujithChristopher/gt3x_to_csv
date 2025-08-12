# GT3X to CSV Converter

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)
![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)
![Pandas](https://img.shields.io/badge/pandas-supported-orange.svg)
![Polars](https://img.shields.io/badge/polars-supported-red.svg)
![uv](https://img.shields.io/badge/uv-compatible-purple.svg)

A fast, pure Python library for parsing ActiGraph GT3X accelerometer files and converting them to CSV format. This tool provides a dependency-free alternative to ActiLife software for extracting accelerometer data from GT3X files.

## ⚡ Key Features

- 🔧 **Zero Dependencies** - Uses only Python standard library
- 📊 **Multiple CSV Formats** - ActiLife-compatible or simple timestamp format
- 🚀 **High Performance** - Efficiently processes large GT3X files
- ✅ **Data Validation** - Includes checksum verification
- 🔍 **Multiple Sample Formats** - Supports 3, 6, and 9-byte activity samples
- 📱 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🔬 **Research Ready** - Perfect for accelerometry research workflows

## 🚀 Installation

### Option 1: uv (Recommended)
```bash
git clone https://github.com/yourusername/gt3x-to-csv.git
cd gt3x-to-csv
uv sync --extra test  # Installs with pandas/polars support
```

### Option 2: Direct Download
```bash
git clone https://github.com/yourusername/gt3x-to-csv.git
cd gt3x-to-csv
pip install -e .  # Installs without optional dependencies
```

### Option 3: Pip Install (Coming Soon)
```bash
pip install gt3x-to-csv
pip install gt3x-to-csv[test]  # With pandas/polars support
```

## 💻 Quick Start

### Command Line Usage
```bash
python gt3x_parser.py input.gt3x output.csv
# Or with uv:
uv run python gt3x_parser.py input.gt3x output.csv
```

### Enhanced Python API (Recommended)
```python
from gt3x_parser import GT3XReader

# Modern context manager API with DataFrame support
with GT3XReader('data.gt3x') as reader:
    # Access structured metadata
    print(f"Device: {reader.device_info.serial_number}")
    print(f"Sample Rate: {reader.device_info.sample_rate} Hz")
    print(f"Total Samples: {reader.recording_info.total_samples}")
    
    # Get data in different formats
    df = reader.to_pandas(calibrated=True)     # Pandas DataFrame (timestamped)
    df_pl = reader.to_polars(calibrated=True)  # Polars DataFrame  
    data = reader.to_dict(calibrated=True)     # Python dictionary
    
    # Access complete metadata
    metadata = reader.metadata
```

### Legacy Python API (Still Supported)
```python
from gt3x_parser import GT3XParser, GT3XToCSV

# Original API for backward compatibility
parser = GT3XParser('data.gt3x')
data = parser.parse()

print(f"Device: {data['info']['Serial Number']}")
print(f"Samples: {len(data['activity_samples'])}")

# Convert to CSV
converter = GT3XToCSV()
converter.convert('data.gt3x', 'output.csv', actilife_format=True)
```

## 📁 Project Structure

```
gt3x-to-csv/
├── gt3x_parser.py      # Main converter module
├── requirements.txt    # Dependencies (none required)
├── README.md          # This file
├── LICENSE            # MIT license
├── setup.py           # Package configuration
└── examples/          # Examples and test files
    ├── test_file.gt3x        # Sample GT3X file
    ├── actilife_file.csv     # Reference ActiLife output
    ├── example_usage.py      # Usage examples
    ├── test_parser.py        # Unit tests
    └── debug_gt3x.py         # GT3X file analyzer
```

## 📊 Output Formats

### ActiLife Format (Default)
Mimics ActiLife software output with header information and g-force values:
```csv
------------ Data File Created By ActiGraph GT3X+ ActiLife v6.11.9 Firmware v1.7.2 date format d/MM/yyyy at 100 Hz  Filter Normal -----------
Serial Number: TAS1H30182785
Start Time 18:40:00
Start Date 17/09/2019
...
Accelerometer X,Accelerometer Y,Accelerometer Z
0.000,0.008,0.996
0.016,0.000,1.008
```

### Simple Format
Clean CSV with timestamps and raw values:
```csv
Timestamp,X,Y,Z
2019-09-17 18:40:00.000,0,2,255
2019-09-17 18:40:00.010,4,0,258
```

## GT3X File Format Support

This converter handles:
- **Legacy GT3X files** with activity records (type 0)
- **Modern GT3X files** with type 26 records  
- **Windows ticks timestamps** (common in newer files)
- **Multiple sample formats** (6-byte, 9-byte, packed formats)
- **Proper scaling** using device-specific scale factors

## 🧪 Testing

Run the test suite with uv:
```bash
uv run python examples/test_parser.py
uv run python examples/enhanced_api_demo.py  # Demo new features
```

Legacy testing:
```bash
cd examples
python test_parser.py
python example_usage.py
```

Test with the sample GT3X file:
```bash
cd examples
uv run python ../gt3x_parser.py test_file.gt3x output.csv
```

## 📋 Requirements

### Core Requirements
- Python 3.8+
- No external dependencies (uses only standard library)

### Optional Dependencies (for enhanced features)
- `pandas >= 2.0.3` - For DataFrame output with `.to_pandas()`
- `polars >= 1.8.2` - For high-performance DataFrame output with `.to_polars()`

Install with:
```bash
uv add pandas polars  # or pip install pandas polars
```

## Performance

This Python implementation provides significant performance improvements over ActiLife:
- Processes files in seconds rather than minutes
- Memory efficient binary parsing
- Suitable for batch processing large datasets

## 📚 API Reference

### Modern GT3XReader Class (Recommended)
```python
# Context manager for resource management
with GT3XReader(file_path) as reader:
    # DataFrame outputs (requires pandas/polars)
    df = reader.to_pandas(include_timestamps=True, calibrated=True)
    df_pl = reader.to_polars(include_timestamps=True, calibrated=True)
    
    # Dictionary output (always available)
    data = reader.to_dict(include_timestamps=True, calibrated=True)
    
    # Structured metadata access
    device_info = reader.device_info      # DeviceInfo dataclass
    recording_info = reader.recording_info  # RecordingInfo dataclass  
    data_quality = reader.data_quality    # DataQuality dataclass
    metadata = reader.metadata            # Complete dict
```

### Legacy Classes (Backward Compatible)
```python
# Original parser
parser = GT3XParser(file_path)
data = parser.parse()  # Returns {'info': dict, 'activity_samples': list}

# CSV converter
converter = GT3XToCSV()
converter.convert(gt3x_path, csv_path, actilife_format=True)
```

### Data Structures
```python
@dataclass
class DeviceInfo:
    serial_number: str
    firmware_version: str
    battery_voltage: str
    sample_rate: float
    acceleration_scale: float

@dataclass
class RecordingInfo:
    start_time: Optional[datetime]
    stop_time: Optional[datetime]
    duration_hours: float
    total_samples: int

@dataclass
class ActivitySample:
    x: int  # X-axis acceleration
    y: int  # Y-axis acceleration  
    z: int  # Z-axis acceleration
```

## 🔧 Troubleshooting

### Common Issues

**File not found error**
```bash
Error: Input file data.gt3x does not exist
```
Ensure the GT3X file path is correct and the file exists.

**Checksum verification failed**
```
Checksum verification failed at offset 1234
```
The GT3X file may be corrupted. This warning doesn't stop processing but indicates data integrity issues.

**Unknown activity payload format**
```
Unknown activity payload format, size: 7
```
The parser encountered an unsupported sample format. Please report this as an issue.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ActiGraph for the GT3X file format specification
- [gt3x2csv R package](https://github.com/tarensanders/gt3x2csv) by Taren Sanders for inspiration
- The accelerometry research community

## 🔗 Related Projects

- [ActiGraph ActiLife](https://actigraphcorp.com/actilife-6/) - Official ActiGraph software
- [GGIR](https://github.com/wadpac/GGIR) - R package for accelerometer data processing
- [pygt3x](https://github.com/actigraph/pygt3x) - Official ActiGraph Python library

---

⭐ **Star this repo** if you find it useful!

📫 **Issues and questions** are welcome in the [Issues](https://github.com/yourusername/gt3x-to-csv/issues) section.
