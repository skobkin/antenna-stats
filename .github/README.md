# GitHub Actions - Antenna Structure Validation

This directory contains GitHub Actions workflows and validation scripts to ensure the antenna directory structure follows the established rules.

## Workflow: `files-structure-check.yml`

This workflow runs on pull requests and pushes to main branches when changes are made to the `antennas/` directory.

### Validation Rules

The workflow enforces the following rules for antenna directories:

1. **Directory Naming Convention**: All directories in `antennas/` must use snake_case naming (lowercase letters, numbers, and underscores only)
   - ✅ Valid: `gizont_nbiot_lora_soft_antenna_m2`
   - ❌ Invalid: `Gizont-NBIoT-LoRa`, `antenna_1`, `MyAntenna`

2. **File Size Limits**: No files in antenna subdirectories should exceed 300KB
   - ✅ Valid: Files under 300KB
   - ❌ Invalid: Files over 300KB

3. **Image Location and Format**: 
   - Images must be placed only in `antennas/*/images/` subdirectories
   - Only JPEG (.jpg, .jpeg), WEBP (.webp), and PNG (.png) formats are allowed
   - Images must use snake_case naming convention
   - ✅ Valid: `antennas/my_antenna/images/front_view.jpg`
   - ❌ Invalid: `antennas/my_antenna/photo.gif`, `antennas/my_antenna/images/Photo1.JPG`

4. **Required Structure**: Each antenna directory must contain:
   - `details.md` file (required)
   - `images/` subdirectory (optional, but if present must contain only images)
   - No other files or subdirectories allowed
   - ✅ Valid structure:
     ```
     antennas/my_antenna/
     ├── details.md
     └── images/
         ├── front_view.jpg
         └── side_view.webp
     ```

### Local Testing

You can test the validation locally by running:

```bash
# Test all validations (recommended)
python .github/scripts/validate_all.py

# Test individual components
python .github/scripts/check_directory_naming.py
python .github/scripts/check_file_sizes.py
python .github/scripts/validate_images.py
python .github/scripts/validate_required_files.py
```

### Configuration

All validation rules are centralized in `.github/scripts/config.py`. 