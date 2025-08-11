# Examples and Test Files

This directory contains example files and usage demonstrations for the GT3X to CSV converter.

## Files

### Sample Data
- **`test_file.gt3x`** - Sample GT3X file from ActiGraph device (199KB)
- **`actilife_file.csv`** - Reference CSV output from ActiLife software (4MB)

### Example Scripts
- **`example_usage.py`** - Demonstrates various usage patterns
- **`test_parser.py`** - Unit tests with mock GT3X data
- **`debug_gt3x.py`** - Tool for analyzing GT3X file structure

## Running Examples

### Basic Conversion
```bash
python ../gt3x_parser.py test_file.gt3x my_output.csv
```

### Test All Functionality
```bash
python test_parser.py
python example_usage.py
```

### Analyze GT3X Structure
```bash
python debug_gt3x.py
```

## Expected Output

The sample GT3X file contains:
- **Serial Number:** TAS1H30182785
- **Sample Rate:** 100 Hz
- **Duration:** ~5.5 minutes
- **Total Samples:** 33,000
- **Data Format:** Type 26 records (modern format)

When converted, it should produce a CSV file with 33,000 rows of accelerometer data matching the reference `actilife_file.csv`.