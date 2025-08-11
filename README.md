# GT3X to CSV Converter (Python)

A pure Python implementation for converting ActiGraph GT3X accelerometer files to CSV format. This tool provides a fast, dependency-free alternative to ActiLife software for extracting activity data from GT3X files.

## Features

- **Zero Dependencies**: Uses only Python standard library
- **ActiLife Compatible**: Generates CSV files that match ActiLife's output format
- **High Performance**: Efficiently processes large GT3X files
- **Multiple Formats**: Supports both ActiLife-style and simple timestamp formats
- **Modern GT3X Support**: Handles both legacy and modern GT3X file formats

## Quick Start

### Command Line Usage
```bash
python gt3x_parser.py input.gt3x output.csv
```

### Programmatic Usage
```python
from gt3x_parser import GT3XToCSV

converter = GT3XToCSV()
converter.convert('input.gt3x', 'output.csv')  # ActiLife format
converter.convert('input.gt3x', 'output.csv', actilife_format=False)  # Simple format
```

## File Structure

```
gt3x2csv/
├── gt3x_parser.py      # Main converter module
├── requirements.txt    # Dependencies (none required)
├── README.md          # This file
└── examples/          # Examples and test files
    ├── test_file.gt3x        # Sample GT3X file
    ├── actilife_file.csv     # Reference ActiLife output
    ├── example_usage.py      # Usage examples
    ├── test_parser.py        # Unit tests
    └── debug_gt3x.py         # GT3X file analyzer
```

## Output Formats

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

## License

This is a Python port inspired by the [gt3x2csv R package](https://github.com/tarensanders/gt3x2csv) by Taren Sanders.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.