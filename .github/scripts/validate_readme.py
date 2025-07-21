#!/usr/bin/env python3
"""
README.md validation script.
Checks that all antenna directories are linked from README.md and that all links are valid.
Also validates antenna sections structure and frequency subsections.
"""

import re
import sys
from pathlib import Path
from typing import List, Set, Tuple
from urllib.parse import urlparse

# Import configuration and utilities
try:
    from config import ANTENNAS_DIR
    from messages import ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
    from utils import (
        extract_sections_from_markdown, 
        check_parameter_in_section, 
        is_frequency_subsection,
        extract_links_from_readme,
        get_antenna_directories,
        extract_link_title
    )
except ImportError as e:
    print(f"❌ Error: Could not import required modules: {e}")
    sys.exit(1)



def validate_antenna_sections(readme_path: Path) -> List[str]:
    """
    Validate antenna sections in README.md.
    
    Args:
        readme_path: Path to README.md file
        
    Returns:
        List of error messages
    """
    errors = []
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(ERROR_TEMPLATES['readme_error'].format(error=e))
        return errors
    
    # Extract sections
    sections = extract_sections_from_markdown(content)
    
    # Check if "Antennas" section exists
    if 'Antennas' not in sections:
        errors.append(ERROR_TEMPLATES['missing_antennas_section'])
        return errors
    
    antennas_section = sections['Antennas']
    lines = antennas_section['lines']
    
    # Find all antenna subsections (h3 headers)
    antenna_subsections = []
    current_subsection = None
    current_content = []
    
    for line in lines:
        if line.startswith('### '):
            # Save previous subsection if exists
            if current_subsection:
                antenna_subsections.append({
                    'name': current_subsection,
                    'content': '\n'.join(current_content).strip(),
                    'lines': current_content.copy()
                })
            
            # Start new subsection
            current_subsection = line[4:].strip()  # Remove '### '
            current_content = []
        elif current_subsection:
            current_content.append(line)
    
    # Save last subsection
    if current_subsection:
        antenna_subsections.append({
            'name': current_subsection,
            'content': '\n'.join(current_content).strip(),
            'lines': current_content.copy()
        })
    
    # Validate each antenna subsection
    for subsection in antenna_subsections:
        subsection_name = subsection['name']
        subsection_content = subsection['content']
        
        # Check if it's a link to README.md
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, subsection_name)
        
        if not links:
            errors.append(ERROR_TEMPLATES['antenna_not_link'].format(subsection=subsection_name))
            continue
        
        # Check that the link points to a README.md file
        link_text, link_url = links[0]
        if not link_url.endswith('README.md'):
            errors.append(ERROR_TEMPLATES['antenna_not_details_link'].format(subsection=extract_link_title(subsection_name)))
            continue
        
        # Check that the README.md file exists
        readme_path = Path(link_url)
        if not readme_path.exists():
            errors.append(ERROR_TEMPLATES['antenna_file_not_exists'].format(subsection=extract_link_title(subsection_name), link=link_url))
            continue
        
        # Check that the antenna directory exists
        antenna_dir = readme_path.parent
        if not antenna_dir.exists() or not antenna_dir.is_dir():
            errors.append(ERROR_TEMPLATES['antenna_dir_invalid'].format(subsection=extract_link_title(subsection_name), dir=antenna_dir))
            continue
        
        # Check for frequency subsections
        frequency_subsections = []
        current_freq_subsection = None
        current_freq_content = []
        
        for line in subsection['lines']:
            if line.startswith('#### '):
                # Save previous frequency subsection if exists
                if current_freq_subsection:
                    frequency_subsections.append({
                        'name': current_freq_subsection,
                        'content': '\n'.join(current_freq_content).strip()
                    })
                
                # Start new frequency subsection
                current_freq_subsection = line[5:].strip()  # Remove '#### '
                current_freq_content = []
            elif current_freq_subsection:
                current_freq_content.append(line)
        
        # Save last frequency subsection
        if current_freq_subsection:
            frequency_subsections.append({
                'name': current_freq_subsection,
                'content': '\n'.join(current_freq_content).strip()
            })
        
        # Check that there's at least one frequency subsection
        if not frequency_subsections:
            errors.append(ERROR_TEMPLATES['missing_frequency_subsection'].format(subsection=extract_link_title(subsection_name)))
            continue
        
        # Check that at least one subsection has frequency in its name
        has_frequency_subsection = False
        for freq_subsection in frequency_subsections:
            if is_frequency_subsection(freq_subsection['name']):
                has_frequency_subsection = True
                # Check that frequency subsections contain SWR
                if not check_parameter_in_section(freq_subsection['content'], 'SWR'):
                    errors.append(ERROR_TEMPLATES['frequency_missing_swr'].format(frequency=freq_subsection['name'], subsection=extract_link_title(subsection_name)))
        
        if not has_frequency_subsection:
            errors.append(ERROR_TEMPLATES['no_frequency_subsection'].format(subsection=extract_link_title(subsection_name)))
    
    return errors

def validate_readme_links() -> List[str]:
    """
    Validate README.md links and antenna directory coverage.
    
    Returns:
        List of error messages
    """
    errors = []
    
    print(PROGRESS_TEMPLATES.get('readme_validation', "📖 Validating README.md links..."))
    
    readme_path = Path("README.md")
    if not readme_path.exists():
        errors.append(ERROR_TEMPLATES['readme_missing'])
        return errors
    
    # Get all antenna directories
    antenna_dirs = get_antenna_directories(ANTENNAS_DIR)
    if not antenna_dirs:
        print(ERROR_TEMPLATES['no_antennas_dir'])
        return errors
    
    # Extract links from README
    internal_links, external_links = extract_links_from_readme(readme_path)
    
    # Check that all antenna directories are linked
    linked_antennas = set()
    for link in internal_links:
        # Extract directory name from link
        if link.startswith('antennas/'):
            parts = link.split('/')
            if len(parts) >= 2:
                antenna_name = parts[1]
                linked_antennas.add(antenna_name)
    
    # Find unlinked antenna directories
    unlinked_antennas = antenna_dirs - linked_antennas
    for antenna in unlinked_antennas:
        errors.append(ERROR_TEMPLATES['antenna_not_linked'].format(name=antenna))
    
    # Check for broken internal links
    for link in internal_links:
        if link.startswith('antennas/'):
            # Check if the linked file/directory exists
            link_path = Path(link)
            if not link_path.exists():
                errors.append(ERROR_TEMPLATES['broken_internal_link'].format(link=link))
    
    # Check for broken external links (basic validation)
    for link in external_links:
        try:
            parsed = urlparse(link)
            if not parsed.scheme or not parsed.netloc:
                errors.append(ERROR_TEMPLATES['invalid_external_link'].format(link=link))
        except Exception:
            errors.append(ERROR_TEMPLATES['malformed_external_link'].format(link=link))
    
    return errors

def main():
    """Main validation function."""
    try:
        errors = []
        
        # Validate basic links
        link_errors = validate_readme_links()
        errors.extend(link_errors)
        
        # Validate antenna sections structure
        readme_path = Path("README.md")
        if readme_path.exists():
            print(PROGRESS_TEMPLATES.get('readme_sections', "📋 Validating README.md antenna sections..."))
            section_errors = validate_antenna_sections(readme_path)
            errors.extend(section_errors)
        
        if errors:
            print(f"\n❌ README.md validation failed!")
            print(f"\nIssues found:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
            return errors
        else:
            print(f"\n{SUCCESS_TEMPLATES.get('readme_validation', '✅ README.md validation passed!')}")
            return []
            
    except Exception as e:
        error_msg = f"❌ Unexpected error in README validation: {e}"
        print(error_msg)
        return [error_msg]

if __name__ == "__main__":
    main() 