# Contributing

You can contribute to this repository by opening a Pull Request with your measurements.

## Guidelines

- Make measurements depending on how antenna frequency characteristics are stated
  - If antenna is stated to be a wideband, make measure the beginning, the middle and the end of the band (use 3 markers in NanoVNA)
  - If antenna is stated to be tuned to a specific frequency (i.e. 868 MHz), measure it on that specific frequency, but set up your measuring device to measure with some headroom on both sides (for example from 800 MHz to 1000 MHz for 868 MHz antenna)
- Add basic information on antenna to the `README.md`. All other details should go into a separate directory in the `antennas`
  - The directory should be named using `snake_case` in English
  - All images should go into a separate sub-directory: `antennas/<antenna_name>/images`
    - Screenshots from NanoVNA and devices like that should be in PNG format while
    - Antenna photos should be in JPEG or WebP (compressed) formats, their resolutions should be no more than 1280x720
  - All detailed text data goes into a `antennas/<antenna_name>/details.md` file.
    - Check for existing `details.md` examples to see how to format it.
    - If there is a datasheet for the antenna, leave a link to it.

## Hints on taking antenna measurements with [NanoVNA](https://nanovna.com)

**Before measuring:**
- Calibrate your NanoVNA using a calibration kit (SOL: Short, Open, Load)
- Ensure calibration covers your frequency range of interest
- Use quality coaxial cables and minimize cable length
- Allow the NanoVNA to warm up for 5-10 minutes before calibration

**During measurement:**
- Keep the antenna away from metal objects, walls, and your body (at least 3 wavelengths)
- Measure in an open area or anechoic environment when possible
- Ensure good connection between antenna and NanoVNA (tight, clean connectors)
- Take measurements at multiple orientations

**What to avoid:**
- Don't touch the antenna or feed line during measurement
- Avoid measuring near other antennas or RF sources
- Don't use damaged or dirty connectors
- Avoid excessive cable coiling or sharp bends
- Don't rush - take multiple measurements for consistency
- Avoid measuring in windy conditions for wire antennas

**Documentation:**
- Leave at least one link where antenna could be bought
- Leave full vendor name and antenna model if available
- Include stated frequency range, measurement setup, optionally add environment description
- Provide clear photo(s) of the antenna and measurement setup
- Provide measurement screenshots from NanoVNA and text representation of the data on them
  - Screenshots should be saved in PNG with compression to avoid large size
- Record SWR, return loss, and impedance data
- Note any limitations or unusual conditions during measurement

## Step by step contribution guide for beginners

[TBW]
