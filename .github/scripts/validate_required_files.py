#!/usr/bin/env python3
"""
Validate required files in antenna directories.
Ensures each antenna directory contains required files and no unauthorized files.
"""

import sys
from pathlib import Path

# Import configuration
try:
    from config import (
        ANTENNAS_DIR, REQUIRED_FILES, ALLOWED_DIRECTORIES,
        DETAILS_FILE_NAME, IMAGES_DIR_NAME,
        ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    )
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

def validate_required_files():
    """Check that each antenna directory contains required files and no unauthorized files."""
    errors = []
    
    if not ANTENNAS_DIR.exists():
        print(ERROR_TEMPLATES['no_antennas_dir'])
        return errors
    
    print(PROGRESS_TEMPLATES['required_files'])
    
    try:
        for item in ANTENNAS_DIR.iterdir():
            if item.is_dir():
                print(PROGRESS_TEMPLATES['checking_dir'].format(name=item.name))
                
                details_file = item / DETAILS_FILE_NAME
                if not details_file.exists():
                    errors.append(ERROR_TEMPLATES['missing_details'].format(name=item.name))
                    print(f"    ❌ Missing {DETAILS_FILE_NAME}")
                else:
                    print(PROGRESS_TEMPLATES['found_details'])
                
                for subitem in item.iterdir():
                    if subitem.name not in REQUIRED_FILES + ALLOWED_DIRECTORIES:
                        if subitem.is_file():
                            errors.append(ERROR_TEMPLATES['unauthorized_file'].format(
                                name=item.name, file=subitem.name
                            ))
                            print(f"    ❌ Unauthorized file: {subitem.name}")
                        elif subitem.is_dir():
                            errors.append(ERROR_TEMPLATES['unauthorized_subdir'].format(
                                name=item.name, subdir=subitem.name
                            ))
                            print(f"    ❌ Unauthorized subdirectory: {subitem.name}")
                    elif subitem.name == IMAGES_DIR_NAME:
                        if subitem.is_dir():
                            print(PROGRESS_TEMPLATES['found_images'])
                        else:
                            errors.append(ERROR_TEMPLATES['images_not_directory'].format(name=item.name))
                            print(f"    ❌ '{IMAGES_DIR_NAME}' is not a directory")
    except OSError as e:
        error_msg = f"❌ Error accessing antennas directory: {e}"
        errors.append(error_msg)
        print(error_msg)
    
    return errors

def main():
    """Main function."""
    try:
        errors = validate_required_files()
        
        if errors:
            print(f"\n❌ Required files validation failed!")
            print(f"Total issues: {len(errors)}")
            for error in errors:
                print(f"  {error}")
            sys.exit(1)
        else:
            print(f"\n{SUCCESS_TEMPLATES['required_files']}")
            sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error in required files validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 