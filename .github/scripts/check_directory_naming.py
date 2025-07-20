#!/usr/bin/env python3
"""
Check directory naming convention in antennas directory.
Ensures all directories use snake_case naming (lowercase letters and underscores only).
"""

import sys
from pathlib import Path

# Import configuration
try:
    from config import (
        ANTENNAS_DIR, SNAKE_CASE_PATTERN, 
        ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    )
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

def check_directory_naming():
    """Check that all directories in antennas use snake_case naming."""
    errors = []
    
    if not ANTENNAS_DIR.exists():
        print(ERROR_TEMPLATES['no_antennas_dir'])
        return errors
    
    print(PROGRESS_TEMPLATES['directory_naming'])
    
    try:
        for item in ANTENNAS_DIR.iterdir():
            if item.is_dir():
                if not SNAKE_CASE_PATTERN.match(item.name):
                    errors.append(ERROR_TEMPLATES['directory_naming'].format(name=item.name))
                    print(f"  ❌ {item.name}: Invalid naming convention")
                else:
                    print(PROGRESS_TEMPLATES['valid_directory'].format(name=item.name))
    except OSError as e:
        error_msg = f"❌ Error accessing antennas directory: {e}"
        errors.append(error_msg)
        print(error_msg)
    
    return errors

def main():
    """Main function."""
    try:
        errors = check_directory_naming()
        
        if errors:
            print(f"\n❌ Directory naming validation failed!")
            print(f"Total issues: {len(errors)}")
            for error in errors:
                print(f"  {error}")
            sys.exit(1)
        else:
            print(f"\n{SUCCESS_TEMPLATES['directory_naming']}")
            sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error in directory naming validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 