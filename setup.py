#!/usr/bin/env python3
"""
Setup script for GT3X to CSV Converter
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py if it exists, otherwise use default
version = "1.0.0"

setup(
    name="gt3x-to-csv",
    version=version,
    author="Your Name",
    author_email="your.email@example.com",
    description="A fast, pure Python library for parsing ActiGraph GT3X accelerometer files and converting them to CSV format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gt3x-to-csv",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gt3x-to-csv/issues",
        "Source": "https://github.com/yourusername/gt3x-to-csv",
        "Documentation": "https://github.com/yourusername/gt3x-to-csv/blob/main/README.md",
    },
    packages=find_packages(),
    py_modules=["gt3x_parser"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    entry_points={
        "console_scripts": [
            "gt3x-to-csv=gt3x_parser:main",
        ],
    },
    keywords="actigraphy, accelerometer, gt3x, actilife, csv, research, health",
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.rst"],
    },
    zip_safe=False,
)