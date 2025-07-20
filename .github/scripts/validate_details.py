#!/usr/bin/env python3
"""
details.md validation script.
Checks that all details.md files have required sections and valid image references.
"""

import re
import sys
from pathlib import Path
from typing import List, Set, Dict, Any
from urllib.parse import urlparse

# Import configuration
try:
    from config import ANTENNAS_DIR, ALLOWED_IMAGE_EXTENSIONS, ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

def extract_sections_from_markdown(content: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract sections and their content from markdown content.
    
    Args:
        content: Markdown content as string
        
    Returns:
        Dictionary with section names as keys and section info as values
    """
    sections = {}
    
    # Split content into lines
    lines = content.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        # Check for h2 headers (##)
        if line.startswith('## '):
            # Save previous section if exists
            if current_section:
                sections[current_section] = {
                    'content': '\n'.join(current_content).strip(),
                    'lines': current_content.copy()
                }
            
            # Start new section
            current_section = line[3:].strip()  # Remove '## '
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = {
            'content': '\n'.join(current_content).strip(),
            'lines': current_content.copy()
        }
    
    return sections

def extract_image_links(content: str) -> List[str]:
    """
    Extract image links from markdown content.
    
    Args:
        content: Markdown content as string
        
    Returns:
        List of image URLs/paths
    """
    image_links = []
    
    # Find markdown image links: ![alt](url)
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, content)
    
    for alt_text, url in matches:
        image_links.append(url)
    
    return image_links

def validate_required_sections(sections: Dict[str, Dict[str, Any]], antenna_name: str) -> List[str]:
    """
    Validate that required sections exist and have proper content.
    
    Args:
        sections: Dictionary of sections from markdown
        antenna_name: Name of the antenna directory
        
    Returns:
        List of error messages
    """
    errors = []
    
    required_sections = ['Where to buy', 'Measurements', 'Photos']
    
    # Check that all required sections exist
    for section in required_sections:
        if section not in sections:
            errors.append(f"❌ Antenna '{antenna_name}' is missing required section '## {section}'")
            continue
        
        section_content = sections[section]['content']
        
        # Validate "Where to buy" section
        if section == 'Where to buy':
            # Check for at least one link
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, section_content)
            if not links:
                errors.append(f"❌ Antenna '{antenna_name}' section 'Where to buy' must contain at least one link")
        
        # Validate "Measurements" section
        elif section == 'Measurements':
            # Check for at least one subsection (h3)
            subsection_pattern = r'^### '
            subsections = re.findall(subsection_pattern, section_content, re.MULTILINE)
            if not subsections:
                errors.append(f"❌ Antenna '{antenna_name}' section 'Measurements' must contain at least one subsection (###)")
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
                            if 'SWR' not in content_text:
                                errors.append(f"❌ Antenna '{antenna_name}' subsection '{current_subsection}' must contain 'SWR'")
                            if 'Impedance' not in content_text:
                                errors.append(f"❌ Antenna '{antenna_name}' subsection '{current_subsection}' must contain 'Impedance'")
                        
                        # Start new subsection
                        current_subsection = line[4:].strip()
                        subsection_content = []
                    elif current_subsection:
                        subsection_content.append(line)
                
                # Validate last subsection
                if current_subsection and subsection_content:
                    content_text = '\n'.join(subsection_content)
                    if 'SWR' not in content_text:
                        errors.append(f"❌ Antenna '{antenna_name}' subsection '{current_subsection}' must contain 'SWR'")
                    if 'Impedance' not in content_text:
                        errors.append(f"❌ Antenna '{antenna_name}' subsection '{current_subsection}' must contain 'Impedance'")
        
        # Validate "Photos" section
        elif section == 'Photos':
            # Check that photos are inside spoilers (details tags)
            if '<details>' not in section_content or '</details>' not in section_content:
                errors.append(f"❌ Antenna '{antenna_name}' section 'Photos' must contain photos inside spoilers (<details> tags)")
    
    return errors

def validate_image_references(image_links: List[str], antenna_dir: Path, antenna_name: str) -> List[str]:
    """
    Validate that all image references point to existing files (except external URLs).
    
    Args:
        image_links: List of image URLs/paths
        antenna_dir: Path to antenna directory
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
            errors.append(f"❌ Antenna '{antenna_name}' references non-existing image: {image_link}")
            continue
        
        # Check if it's an image file
        if image_path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            errors.append(f"❌ Antenna '{antenna_name}' references non-image file: {image_link}")
    
    return errors

def validate_details_files() -> List[str]:
    """
    Validate all details.md files in antenna directories.
    
    Returns:
        List of error messages
    """
    errors = []
    
    print(PROGRESS_TEMPLATES.get('details_validation', "📄 Validating details.md files..."))
    
    if not ANTENNAS_DIR.exists():
        print("ℹ️  No antennas directory found, skipping details validation")
        return errors
    
    for antenna_dir in ANTENNAS_DIR.iterdir():
        if not antenna_dir.is_dir():
            continue
        
        antenna_name = antenna_dir.name
        details_file = antenna_dir / "details.md"
        
        if not details_file.exists():
            errors.append(f"❌ Antenna '{antenna_name}' is missing details.md file")
            continue
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"❌ Error reading details.md for antenna '{antenna_name}': {e}")
            continue
        
        # Extract sections
        sections = extract_sections_from_markdown(content)
        
        # Validate required sections
        section_errors = validate_required_sections(sections, antenna_name)
        errors.extend(section_errors)
        
        # Extract and validate image references
        image_links = extract_image_links(content)
        image_errors = validate_image_references(image_links, antenna_dir, antenna_name)
        errors.extend(image_errors)
    
    return errors

def main():
    """Main validation function."""
    try:
        errors = validate_details_files()
        
        if errors:
            print(f"\n❌ details.md validation failed!")
            print(f"\nIssues found:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
            return errors
        else:
            print(f"\n{SUCCESS_TEMPLATES.get('details_validation', '✅ details.md validation passed!')}")
            return []
            
    except Exception as e:
        error_msg = f"❌ Unexpected error in details validation: {e}"
        print(error_msg)
        return [error_msg]

if __name__ == "__main__":
    main() 