#!/usr/bin/env python3
"""
README.md validation script.
Checks that all antenna directories are linked from README.md and that all links are valid.
"""

import re
import sys
from pathlib import Path
from typing import List, Set, Tuple
from urllib.parse import urlparse

# Import configuration
try:
    from config import ANTENNAS_DIR, ERROR_TEMPLATES, SUCCESS_TEMPLATES, PROGRESS_TEMPLATES
except ImportError:
    print("❌ Error: Could not import configuration file")
    sys.exit(1)

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

def get_antenna_directories() -> Set[str]:
    """
    Get all antenna directory names.
    
    Returns:
        Set of antenna directory names
    """
    antenna_dirs = set()
    
    if not ANTENNAS_DIR.exists():
        return antenna_dirs
    
    for item in ANTENNAS_DIR.iterdir():
        if item.is_dir():
            antenna_dirs.add(item.name)
    
    return antenna_dirs

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
        errors.append("❌ README.md file not found in root directory")
        return errors
    
    # Get all antenna directories
    antenna_dirs = get_antenna_directories()
    if not antenna_dirs:
        print("ℹ️  No antenna directories found, skipping README validation")
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
        errors.append(f"❌ Antenna directory '{antenna}' is not linked from README.md")
    
    # Check for broken internal links
    for link in internal_links:
        if link.startswith('antennas/'):
            # Check if the linked file/directory exists
            link_path = Path(link)
            if not link_path.exists():
                errors.append(f"❌ README.md links to non-existing path: {link}")
    
    # Check for broken external links (basic validation)
    for link in external_links:
        try:
            parsed = urlparse(link)
            if not parsed.scheme or not parsed.netloc:
                errors.append(f"❌ README.md contains invalid external link: {link}")
        except Exception:
            errors.append(f"❌ README.md contains malformed external link: {link}")
    
    return errors

def main():
    """Main validation function."""
    try:
        errors = validate_readme_links()
        
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