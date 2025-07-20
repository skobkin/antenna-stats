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

# Error message templates
ERROR_TEMPLATES = {
    'directory_naming': "❌ Directory '{name}' in antennas/ does not use snake_case naming (only lowercase letters, numbers, and underscores allowed)",
    'file_size_exceeded': "❌ File '{path}' is {size:.1f}KB, exceeds {max_size}KB limit",
    'file_access_error': "❌ Could not check size of file '{path}': {error}",
    'image_wrong_location': f"❌ Image '{{path}}' found in antenna root directory. Images must be in '{IMAGES_DIR_NAME}/' subdirectory",
    'image_unsupported_format': f"❌ Image '{{path}}' has unsupported format '{{ext}}'. Only {', '.join(ALLOWED_IMAGE_EXTENSIONS)} are allowed",
    'image_invalid_naming': "❌ Image '{path}' does not use snake_case naming convention",
    'missing_details': f"❌ Directory '{{name}}' is missing required '{DETAILS_FILE_NAME}' file",
    'unauthorized_file': f"❌ Directory '{{name}}' contains unauthorized file '{{file}}'. Only '{DETAILS_FILE_NAME}' and '{IMAGES_DIR_NAME}/' directory are allowed",
    'unauthorized_subdir': f"❌ Directory '{{name}}' contains unauthorized subdirectory '{{subdir}}'. Only '{IMAGES_DIR_NAME}/' directory is allowed",
    'images_not_directory': f"❌ Directory '{{name}}' contains '{IMAGES_DIR_NAME}' but it's not a directory",
    'no_antennas_dir': "ℹ️  No antennas directory found, skipping validation"
}

# Success message templates
SUCCESS_TEMPLATES = {
    'directory_naming': "✅ All directories use proper snake_case naming!",
    'file_sizes': "✅ All files are within size limits!",
    'images': "✅ All images are properly located and formatted!",
    'required_files': "✅ All antenna directories have proper structure!",
    'all_checks': "✅ All antenna structure validation checks passed!"
}

# Progress message templates
PROGRESS_TEMPLATES = {
    'directory_naming': "📁 Checking directory naming conventions...",
    'file_sizes': "📏 Checking file sizes in antenna directories...",
    'images': "🖼️  Validating image locations and formats...",
    'required_files': "📄 Validating required files in antenna directories...",
    'starting': "🔍 Starting antenna structure validation...",
    'checking_dir': "  Checking directory: {name}",
    'valid_image': "  ✅ {path}: Valid image",
    'valid_file_size': "  ✅ {path}: {size:.1f}KB",
    'valid_directory': "  ✅ {name}: Valid snake_case naming",
    'found_details': f"    ✅ Found {DETAILS_FILE_NAME}",
    'found_images': f"    ✅ Found {IMAGES_DIR_NAME}/ directory"
}
