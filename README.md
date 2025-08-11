# GT3X to CSV Converter

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)
![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

A fast, pure Python library for parsing ActiGraph GT3X accelerometer files and converting them to CSV format. This tool provides a dependency-free alternative to ActiLife software for extracting activity data from GT3X files.

## ⚡ Key Features

- 🔧 **Zero Dependencies** - Uses only Python standard library
- 📊 **Multiple CSV Formats** - ActiLife-compatible or simple timestamp format
- 🚀 **High Performance** - Efficiently processes large GT3X files
- ✅ **Data Validation** - Includes checksum verification
- 🔍 **Multiple Sample Formats** - Supports 3, 6, and 9-byte activity samples
- 📱 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🔬 **Research Ready** - Perfect for accelerometry research workflows

## 🚀 Installation

### Option 1: Direct Download
```bash
git clone https://github.com/yourusername/gt3x-to-csv.git
cd gt3x-to-csv
```

### Option 2: Pip Install (Coming Soon)
```bash
pip install gt3x-to-csv
```

## 💻 Quick Start

### Command Line Usage
```bash
python gt3x_parser.py input.gt3x output.csv
```

### Python API
```python
from gt3x_parser import GT3XParser, GT3XToCSV

# Parse GT3X file
parser = GT3XParser('data.gt3x')
data = parser.parse()

print(f"Device: {data['info']['Serial Number']}")
print(f"Samples: {len(data['activity_samples'])}")

# Convert to CSV
converter = GT3XToCSV()

# ActiLife format (default)
converter.convert('data.gt3x', 'output_actilife.csv', actilife_format=True)

# Simple timestamp format
converter.convert('data.gt3x', 'output_simple.csv', actilife_format=False)
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

## Testing

Run the test suite with the included sample file:
```bash
cd examples
python test_parser.py
python example_usage.py
```

Test with the sample GT3X file:
```bash
cd examples
python ../gt3x_parser.py test_file.gt3x output.csv
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Performance

This Python implementation provides significant performance improvements over ActiLife:
- Processes files in seconds rather than minutes
- Memory efficient binary parsing
- Suitable for batch processing large datasets

## 📚 API Reference

### GT3XParser Class
```python
parser = GT3XParser(file_path)
data = parser.parse()  # Returns {'info': dict, 'activity_samples': list}
```

### GT3XToCSV Class
```python
converter = GT3XToCSV()
converter.convert(gt3x_path, csv_path, actilife_format=True)
```

### Data Structures
```python
@dataclass
class ActivitySample:
    x: int  # X-axis acceleration
    y: int  # Y-axis acceleration  
    z: int  # Z-axis acceleration

@dataclass
class GT3XRecord:
    separator: int
    record_type: int
    timestamp: int
    payload_size: int
    payload: bytes
    checksum: int
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