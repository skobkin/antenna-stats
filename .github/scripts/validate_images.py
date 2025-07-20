#!/usr/bin/env python3
"""
Validate image locations and formats in antenna directories.
Ensures images are only in allowed subdirectories and use correct formats.
"""

import sys
from pathlib import Path

# Import configuration
try:
    from config import (
        ANTENNAS_DIR, ALLOWED_IMAGE_EXTENSIONS, ALL_IMAGE_EXTENSIONS,
        IMAGE_NAMING_PATTERN, IMAGES_DIR_NAME,
        ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    )
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

def validate_images():
    """Check image locations, formats, and naming conventions."""
    errors = []
    
    if not ANTENNAS_DIR.exists():
        print(ERROR_TEMPLATES['no_antennas_dir'])
        return errors
    
    print(PROGRESS_TEMPLATES['images'])
    
    try:
        for file_path in ANTENNAS_DIR.rglob('*'):
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                
                if file_ext in ALL_IMAGE_EXTENSIONS:
                    if file_path.parent.parent.name == ANTENNAS_DIR.name and file_path.parent.name != IMAGES_DIR_NAME:
                        errors.append(ERROR_TEMPLATES['image_wrong_location'].format(path=file_path))
                        print(f"  ❌ {file_path}: Wrong location")
                    
                    elif file_path.parent.name == IMAGES_DIR_NAME:
                        if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
                            errors.append(ERROR_TEMPLATES['image_unsupported_format'].format(
                                path=file_path, ext=file_ext
                            ))
                            print(f"  ❌ {file_path}: Unsupported format {file_ext}")
                        else:
                            if not IMAGE_NAMING_PATTERN.match(file_path.name.lower()):
                                errors.append(ERROR_TEMPLATES['image_invalid_naming'].format(path=file_path))
                                print(f"  ❌ {file_path}: Invalid naming convention")
                            else:
                                print(PROGRESS_TEMPLATES['valid_image'].format(path=file_path))
    except OSError as e:
        error_msg = f"❌ Error traversing antennas directory: {e}"
        errors.append(error_msg)
        print(error_msg)
    
    return errors

def main():
    """Main function."""
    try:
        errors = validate_images()
        
        if errors:
            print(f"\n❌ Image validation failed!")
            print(f"Total issues: {len(errors)}")
            for error in errors:
                print(f"  {error}")
            sys.exit(1)
        else:
            print(f"\n{SUCCESS_TEMPLATES['images']}")
            sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error in image validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 