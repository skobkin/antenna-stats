#!/usr/bin/env python3
"""
Message templates for validation scripts.
Centralizes all error, success, and progress messages for consistency.
"""

# Error message templates
ERROR_TEMPLATES = {
    'directory_naming': "❌ Directory '{name}' in antennas/ does not use snake_case naming (only lowercase letters, numbers, and underscores allowed)",
    'file_size_exceeded': "❌ File '{path}' is {size:.1f}KB, exceeds {max_size}KB limit",
    'file_access_error': "❌ Could not check size of file '{path}': {error}",
    'image_wrong_location': "❌ Image '{path}' found in antenna root directory. Images must be in 'images/' subdirectory",
    'image_unsupported_format': "❌ Image '{path}' has unsupported format '{ext}'. Only .jpg, .jpeg, .webp, .png are allowed",
    'image_invalid_naming': "❌ Image '{path}' does not use snake_case naming convention",
    'missing_details': "❌ Directory '{name}' is missing required 'details.md' file",
    'unauthorized_file': "❌ Directory '{name}' contains unauthorized file '{file}'. Only 'details.md' and 'images/' directory are allowed",
    'unauthorized_subdir': "❌ Directory '{name}' contains unauthorized subdirectory '{subdir}'. Only 'images/' directory is allowed",
    'images_not_directory': "❌ Directory '{name}' contains 'images' but it's not a directory",
    'no_antennas_dir': "ℹ️  No antennas directory found, skipping validation",
    'readme_missing': "❌ README.md file not found in root directory",
    'antenna_not_linked': "❌ Antenna directory '{name}' is not linked from README.md",
    'broken_internal_link': "❌ README.md links to non-existing path: {link}",
    'invalid_external_link': "❌ README.md contains invalid external link: {link}",
    'malformed_external_link': "❌ README.md contains malformed external link: {link}",
    'missing_required_section': "❌ Antenna '{name}' is missing required section '## {section}'",
    'missing_buy_link': "❌ Antenna '{name}' section 'Where to buy' must contain at least one link",
    'missing_measurements_subsection': "❌ Antenna '{name}' section 'Measurements' must contain at least one subsection (###)",
    'missing_swr_in_subsection': "❌ Antenna '{name}' subsection '{subsection}' must contain 'SWR'",
    'missing_impedance_in_subsection': "❌ Antenna '{name}' subsection '{subsection}' must contain 'Impedance'",
    'photos_not_in_spoilers': "❌ Antenna '{name}' section 'Photos' must contain photos inside spoilers (<details> tags)",
    'non_existing_image': "❌ Antenna '{name}' references non-existing image: {image}",
    'non_image_file': "❌ Antenna '{name}' references non-image file: {image}",
    'readme_error': "❌ Error reading README.md: {error}",
    'missing_antennas_section': "❌ README.md is missing '## Antennas' section",
    'antenna_not_link': "❌ Antenna subsection '{subsection}' must be a link to details.md",
    'antenna_not_details_link': "❌ Antenna subsection '{subsection}' must link to details.md file",
    'antenna_file_not_exists': "❌ Antenna subsection '{subsection}' links to non-existing file: {link}",
    'antenna_dir_invalid': "❌ Antenna subsection '{subsection}' links to invalid antenna directory: {dir}",
    'missing_frequency_subsection': "❌ Antenna subsection '{subsection}' must contain at least one frequency subsection",
    'no_frequency_subsection': "❌ Antenna subsection '{subsection}' must contain at least one frequency subsection (e.g., '868 MHz', '433-466 MHz')",
    'frequency_missing_swr': "❌ Frequency subsection '{frequency}' in '{subsection}' must contain 'SWR'",
    'details_read_error': "❌ Error reading details.md for antenna '{name}': {error}"
}

# Success message templates
SUCCESS_TEMPLATES = {
    'directory_naming': "✅ All directories use proper snake_case naming!",
    'file_sizes': "✅ All files are within size limits!",
    'images': "✅ All images are properly located and formatted!",
    'required_files': "✅ All antenna directories have proper structure!",
    'readme_validation': "✅ README.md validation passed!",
    'details_validation': "✅ details.md validation passed!",
    'all_checks': "✅ All antenna structure validation checks passed!"
}

# Progress message templates
PROGRESS_TEMPLATES = {
    'directory_naming': "📁 Checking directory naming conventions...",
    'file_sizes': "📏 Checking file sizes in antenna directories...",
    'images': "🖼️  Validating image locations and formats...",
    'required_files': "📄 Validating required files in antenna directories...",
    'readme_validation': "📖 Validating README.md links...",
    'readme_sections': "📋 Validating README.md antenna sections...",
    'details_validation': "📄 Validating details.md files...",
    'starting': "🔍 Starting antenna structure validation...",
    'checking_dir': "  Checking directory: {name}",
    'valid_image': "  ✅ {path}: Valid image",
    'valid_file_size': "  ✅ {path}: {size:.1f}KB",
    'valid_directory': "  ✅ {name}: Valid snake_case naming",
    'found_details': "    ✅ Found details.md",
    'found_images': "    ✅ Found images/ directory"
} 