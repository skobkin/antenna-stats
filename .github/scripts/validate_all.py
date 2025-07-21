#!/usr/bin/env python3
"""
Consolidated validation script for antenna directory structure.
This script coordinates all validation checks and provides clear error messages.
Imports functions from individual validation scripts to avoid code duplication.
"""

import sys
from typing import List

# Import configuration
try:
    from config import ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

# Import validation functions from individual scripts
try:
    from check_directory_naming import check_directory_naming
    from check_file_sizes import check_file_sizes
    from validate_images import validate_images
    from validate_required_files import validate_required_files
    from validate_readme import validate_readme_links
    from validate_details import validate_antenna_readme_files
except ImportError as e:
    print(f"❌ Error: Could not import validation modules: {e}")
    sys.exit(1)

def run_all_validations() -> List[str]:
    """
    Run all validation checks and return a list of all errors found.
    
    Returns:
        List[str]: List of error messages from all validation checks
    """
    all_errors = []
    
    print(PROGRESS_TEMPLATES['starting'])
    
    # Run directory naming validation
    try:
        errors = check_directory_naming()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in directory naming validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    # Run file size validation
    try:
        errors = check_file_sizes()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in file size validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    # Run image validation
    try:
        errors = validate_images()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in image validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    # Run required files validation
    try:
        errors = validate_required_files()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in required files validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    # Run README validation
    try:
        errors = validate_readme_links()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in README validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    # Run README.md validation
    try:
        errors = validate_antenna_readme_files()
        all_errors.extend(errors)
    except Exception as e:
        error_msg = f"❌ Error in README.md validation: {e}"
        all_errors.append(error_msg)
        print(error_msg)
    
    return all_errors

def main():
    """Main validation function."""
    try:
        all_errors = run_all_validations()
        
        # Report results
        if all_errors:
            print(f"\n❌ Antenna structure validation failed!")
            print(f"\nTotal issues found: {len(all_errors)}")
            print("\nIssues found:")
            for i, error in enumerate(all_errors, 1):
                print(f"  {i}. {error}")
            print(f"\n❌ Validation failed with {len(all_errors)} issue(s)")
            sys.exit(1)
        else:
            print(f"\n{SUCCESS_TEMPLATES['all_checks']}")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Unexpected error in validation process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 