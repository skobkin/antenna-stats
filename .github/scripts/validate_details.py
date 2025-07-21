#!/usr/bin/env python3
"""
README.md validation script.
Checks that all README.md files have required sections and valid image references.
"""

import re
import sys
from pathlib import Path
from typing import List, Set
from urllib.parse import urlparse

# Import configuration and utilities
try:
    from config import ANTENNAS_DIR, ALLOWED_IMAGE_EXTENSIONS
    from messages import ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    from utils import extract_sections_from_markdown, check_parameter_in_section, extract_image_links
except ImportError as e:
    print(f"❌ Error: Could not import required modules: {e}")
    sys.exit(1)



def validate_required_sections(sections: dict, antenna_name: str) -> List[str]:
    """
    Validate that required sections exist and have proper content.
    
    Args:
        sections: Dictionary of sections from markdown
        antenna_name: Name of the antenna directory
        
    Returns:
        List of error messages
    """
    errors = []
    
    required_sections = ['Where to buy', 'Measurements']
    
    # Check that all required sections exist
    for section in required_sections:
        if section not in sections:
            errors.append(ERROR_TEMPLATES['missing_required_section'].format(name=antenna_name, section=section))
            continue
        
        section_content = sections[section]['content']
        
        # Validate "Where to buy" section
        if section == 'Where to buy':
            # Check for at least one link
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, section_content)
            if not links:
                errors.append(ERROR_TEMPLATES['missing_buy_link'].format(name=antenna_name))
        
        # Validate "Measurements" section
        elif section == 'Measurements':
            # Check for at least one subsection (h3)
            subsection_pattern = r'^### '
            subsections = re.findall(subsection_pattern, section_content, re.MULTILINE)
            if not subsections:
                errors.append(ERROR_TEMPLATES['missing_measurements_subsection'].format(name=antenna_name))
            else:
                # Check each subsection for SWR and Impedance
                lines = sections[section]['lines']
                current_subsection = None
                subsection_content = []
                
                for line in lines:
                    if line.startswith('### '):
                        # Validate previous subsection
                        if current_subsection and subsection_content:
                            content_text = '\n'.join(subsection_content)
                            if not check_parameter_in_section(content_text, 'SWR'):
                                errors.append(ERROR_TEMPLATES['missing_swr_in_subsection'].format(name=antenna_name, subsection=current_subsection))
                            if not check_parameter_in_section(content_text, 'Impedance'):
                                errors.append(ERROR_TEMPLATES['missing_impedance_in_subsection'].format(name=antenna_name, subsection=current_subsection))
                        
                        # Start new subsection
                        current_subsection = line[4:].strip()
                        subsection_content = []
                    elif current_subsection:
                        subsection_content.append(line)
                
                # Validate last subsection
                if current_subsection and subsection_content:
                    content_text = '\n'.join(subsection_content)
                    if not check_parameter_in_section(content_text, 'SWR'):
                        errors.append(ERROR_TEMPLATES['missing_swr_in_subsection'].format(name=antenna_name, subsection=current_subsection))
                    if not check_parameter_in_section(content_text, 'Impedance'):
                        errors.append(ERROR_TEMPLATES['missing_impedance_in_subsection'].format(name=antenna_name, subsection=current_subsection))
    
    return errors

def validate_image_references(image_links: List[str], antenna_dir: Path, antenna_name: str) -> List[str]:
    """
    Validate that all image references point to existing files.
    
    Args:
        image_links: List of image links found in the markdown
        antenna_dir: Path to the antenna directory
        antenna_name: Name of the antenna directory
        
    Returns:
        List of error messages
    """
    errors = []
    
    for image_link in image_links:
        # Skip external URLs
        if image_link.startswith('http'):
            continue
        
        # Handle relative paths
        if image_link.startswith('./'):
            image_link = image_link[2:]
        elif not image_link.startswith('/'):
            # Relative to antenna directory
            image_path = antenna_dir / image_link
        else:
            # Absolute path
            image_path = Path(image_link)
        
        # Check if file exists
        if not image_path.exists():
            errors.append(ERROR_TEMPLATES['non_existing_image'].format(name=antenna_name, image=image_link))
            continue
        
        # Check if it's an image file
        if image_path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            errors.append(ERROR_TEMPLATES['non_image_file'].format(name=antenna_name, image=image_link))
    
    return errors

def validate_photo_at_top(content: str, antenna_name: str) -> List[str]:
    """
    Validate that the antenna photo is displayed at the top of the file.
    
    Args:
        content: The markdown content
        antenna_name: Name of the antenna directory
        
    Returns:
        List of error messages
    """
    errors = []
    
    # Split content into lines
    lines = content.split('\n')
    photo_found = False
    
    # Find the first h2 section (##) to define the top section
    first_h2_index = -1
    for i, line in enumerate(lines):
        if line.startswith('## '):
            first_h2_index = i
            break
    
    # If no h2 sections found, check the entire content
    if first_h2_index == -1:
        first_h2_index = len(lines)
    
    # Look for any image in the top section (before first h2)
    for i, line in enumerate(lines[:first_h2_index]):
        # Check for markdown image syntax: ![alt text](image_path)
        if '![' in line and '](' in line and ')' in line:
            # Basic validation that it looks like an image link
            if line.strip().endswith(')') and 'images/' in line:
                photo_found = True
                break
    
    if not photo_found:
        errors.append(f"❌ {antenna_name}: Antenna photo should be displayed at the top of the file after the header")
    
    return errors

def validate_antenna_readme_files() -> List[str]:
    """
    Validate all README.md files in antenna directories.
    
    Returns:
        List of error messages
    """
    errors = []
    
    print(PROGRESS_TEMPLATES.get('details_validation', "📄 Validating README.md files..."))
    
    if not ANTENNAS_DIR.exists():
        print("ℹ️  No antennas directory found, skipping README validation")
        return errors
    
    for antenna_dir in ANTENNAS_DIR.iterdir():
        if not antenna_dir.is_dir():
            continue
        
        antenna_name = antenna_dir.name
        readme_file = antenna_dir / "README.md"
        
        if not readme_file.exists():
            errors.append(ERROR_TEMPLATES['missing_details'].format(name=antenna_name))
            continue
        
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(ERROR_TEMPLATES['details_read_error'].format(name=antenna_name, error=e))
            continue
        
        # Extract sections
        sections = extract_sections_from_markdown(content)
        
        # Validate required sections
        section_errors = validate_required_sections(sections, antenna_name)
        errors.extend(section_errors)
        
        # Validate photo placement
        photo_errors = validate_photo_at_top(content, antenna_name)
        errors.extend(photo_errors)
        
        # Extract and validate image references
        image_links = extract_image_links(content)
        image_errors = validate_image_references(image_links, antenna_dir, antenna_name)
        errors.extend(image_errors)
    
    return errors

def main():
    """Main validation function."""
    try:
        errors = validate_antenna_readme_files()
        
        if errors:
            print(f"\n❌ README.md validation failed!")
            print(f"\nIssues found:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
            return errors
        else:
            print(f"\n{SUCCESS_TEMPLATES.get('details_validation', '✅ README.md validation passed!')}")
            return []
            
    except Exception as e:
        error_msg = f"❌ Unexpected error in README validation: {e}"
        print(error_msg)
        return [error_msg]

if __name__ == "__main__":
    main() 