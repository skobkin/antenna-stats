#!/usr/bin/env python3
"""
Utility functions for validation scripts.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple

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

def check_parameter_in_section(section_text: str, parameter: str) -> bool:
    """
    Check if a parameter is present in a section text.
    
    Args:
        section_text: Text content of the section
        parameter: Parameter to search for (e.g., 'SWR', 'Impedance')
        
    Returns:
        True if parameter is found, False otherwise
    """
    return parameter in section_text

def is_frequency_subsection(subsection_name: str) -> bool:
    """
    Check if a subsection name contains frequency information.
    
    Args:
        subsection_name: Name of the subsection
        
    Returns:
        True if it contains frequency information, False otherwise
    """
    # Look for patterns like: 868 MHz, 100 KHz, 433-466 MHz, 433 MHz, 466 MHz, 433, 466 MHz
    # This regex looks for numbers followed by optional units (MHz, KHz, GHz, Hz)
    frequency_pattern = r'\d+(?:\.\d+)?\s*(?:MHz|KHz|GHz|Hz)'
    return bool(re.search(frequency_pattern, subsection_name, re.IGNORECASE))

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

def extract_links_from_readme(readme_path: Path) -> Tuple[List[str], List[str]]:
    """
    Extract all links from README.md file.
    
    Args:
        readme_path: Path to README.md file
        
    Returns:
        Tuple of (internal_links, external_links)
    """
    internal_links = []
    external_links = []
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return internal_links, external_links
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return internal_links, external_links
    
    # Find all markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, content)
    
    for text, url in matches:
        # Check if it's an internal link (relative path)
        if url.startswith('./') or url.startswith('../') or (not url.startswith('http') and not url.startswith('#')):
            internal_links.append(url)
        elif url.startswith('http'):
            external_links.append(url)
    
    return internal_links, external_links

def get_antenna_directories(antennas_dir: Path) -> Set[str]:
    """
    Get all antenna directory names.
    
    Args:
        antennas_dir: Path to antennas directory
        
    Returns:
        Set of antenna directory names
    """
    antenna_dirs = set()
    
    if not antennas_dir.exists():
        return antenna_dirs
    
    for item in antennas_dir.iterdir():
        if item.is_dir():
            antenna_dirs.add(item.name)
    
    return antenna_dirs

def extract_link_title(link_text: str) -> str:
    """
    Extract the title part from a markdown link.
    
    Args:
        link_text: Full markdown link text like "[Title](url)"
        
    Returns:
        Just the title part without brackets
    """
    # Extract title from [title](url) format
    match = re.match(r'\[([^\]]+)\]\([^)]+\)', link_text)
    if match:
        return match.group(1)
    return link_text 