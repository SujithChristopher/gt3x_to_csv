#!/usr/bin/env python3
"""
Example usage of the GT3X to CSV converter

This script demonstrates how to use the GT3XToCSV class to convert
ActiGraph GT3X files to CSV format.
"""

from gt3x_parser import GT3XToCSV
import os


def convert_single_file(gt3x_path: str, csv_path: str, actilife_format: bool = True):
    """Convert a single GT3X file to CSV"""
    converter = GT3XToCSV()
    converter.convert(gt3x_path, csv_path, actilife_format)


def convert_directory(input_dir: str, output_dir: str):
    """Convert all GT3X files in a directory to CSV"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    converter = GT3XToCSV()
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.gt3x'):
            gt3x_path = os.path.join(input_dir, filename)
            csv_filename = filename.replace('.gt3x', '.csv').replace('.GT3X', '.csv')
            csv_path = os.path.join(output_dir, csv_filename)
            
            print(f"Processing: {filename}")
            converter.convert(gt3x_path, csv_path)


if __name__ == "__main__":
    # Example 1: Convert a single file
    # convert_single_file("sample.gt3x", "sample.csv")
    
    # Example 2: Convert all files in a directory
    # convert_directory("input_gt3x_files/", "output_csv_files/")
    
    print("Example usage:")
    print("1. Single file (ActiLife format): convert_single_file('sample.gt3x', 'sample.csv')")
    print("2. Single file (Simple format): convert_single_file('sample.gt3x', 'sample.csv', False)")
    print("3. Directory: convert_directory('input_gt3x_files/', 'output_csv_files/')")
    print("4. Command line: python gt3x_parser.py input.gt3x output.csv")
    print("\\nTest with example file: python gt3x_parser.py test_file.gt3x output.csv")