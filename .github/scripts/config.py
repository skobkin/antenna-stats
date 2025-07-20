#!/usr/bin/env python3
"""
Configuration file for antenna validation rules and settings.
Centralizes all validation parameters for easy maintenance.
"""

import re
from pathlib import Path

# Directory structure configuration
ANTENNAS_DIR = Path("antennas")
MAX_FILE_SIZE_KB = 300
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_KB * 1024

# Required files and directories
REQUIRED_FILES = ['details.md']
ALLOWED_DIRECTORIES = ['images']

# File names (for dynamic references)
DETAILS_FILE_NAME = REQUIRED_FILES[0]
IMAGES_DIR_NAME = ALLOWED_DIRECTORIES[0]

# Naming conventions
SNAKE_CASE_PATTERN = re.compile(r'^[a-z0-9_]+$')

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.webp', '.png'}
ALL_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.webp', '.png', '.gif', '.bmp', '.tiff', '.svg'}

# Dynamic image naming pattern based on allowed extensions
allowed_extensions_str = '|'.join(ext[1:] for ext in ALLOWED_IMAGE_EXTENSIONS)
IMAGE_NAMING_PATTERN = re.compile(f'^[a-z0-9_]+\\.({allowed_extensions_str})$')

# Import message templates
try:
    from messages import ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
except ImportError:
    print("❌ Error: Could not import message templates")
    exit(1)
