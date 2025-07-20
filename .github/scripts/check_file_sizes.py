#!/usr/bin/env python3
"""
Check file sizes in antenna directories.
Ensures no files exceed the configured size limit.
"""

import sys
from pathlib import Path

# Import configuration
try:
    from config import (
        ANTENNAS_DIR, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_KB,
        ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    )
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

def check_file_sizes():
    """Check that no files in antennas subdirectories exceed the size limit."""
    errors = []
    
    if not ANTENNAS_DIR.exists():
        print(ERROR_TEMPLATES['no_antennas_dir'])
        return errors
    
    print(PROGRESS_TEMPLATES['file_sizes'])
    
    try:
        for file_path in ANTENNAS_DIR.rglob('*'):
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    if file_size > MAX_FILE_SIZE_BYTES:
                        errors.append(ERROR_TEMPLATES['file_size_exceeded'].format(
                            path=file_path, size=file_size/1024, max_size=MAX_FILE_SIZE_KB
                        ))
                        print(f"  ❌ {file_path}: {file_size/1024:.1f}KB (exceeds limit)")
                    else:
                        print(PROGRESS_TEMPLATES['valid_file_size'].format(
                            path=file_path, size=file_size/1024
                        ))
                except OSError as e:
                    error_msg = ERROR_TEMPLATES['file_access_error'].format(path=file_path, error=str(e))
                    errors.append(error_msg)
                    print(f"  ❌ {file_path}: Access error")
    except OSError as e:
        error_msg = f"❌ Error traversing antennas directory: {e}"
        errors.append(error_msg)
        print(error_msg)
    
    return errors

def main():
    """Main function."""
    try:
        errors = check_file_sizes()
        
        if errors:
            print(f"\n❌ File size validation failed!")
            print(f"Total issues: {len(errors)}")
            for error in errors:
                print(f"  {error}")
            sys.exit(1)
        else:
            print(f"\n{SUCCESS_TEMPLATES['file_sizes']}")
            sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error in file size validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 