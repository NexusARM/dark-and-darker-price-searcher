# config.json Documentation

## Overview
The `config.json` file is a configuration file for the Dark and Darker Price Searcher application. It contains various settings that control the behavior of the application, including screen resolution, file paths, and API parameters.

## File Structure
The configuration file is in JSON format and contains the following structure:

```json
{
    "resolution": {
        "height": 1440,
        "width": 2560
    },
    "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    "screenshot_dir": "screenshots",
    "data_dir": "data",
    "api": {
        "info_file": "data/info.txt",
        "last_days": "4",
        "amount": "3"
    }
}
```

## Configuration Parameters

### Resolution Settings
- `resolution.height`: The height of the game resolution in pixels (default: 1440)
- `resolution.width`: The width of the game resolution in pixels (default: 2560)

### File Paths
- `tesseract_path`: Path to the Tesseract OCR executable, required for text recognition
- `screenshot_dir`: Directory where screenshots will be saved (default: "screenshots")
- `data_dir`: Directory containing item data files (default: "data")

### API Settings
- `api.info_file`: Path to the information file used by the API (default: "data/info.txt")
- `api.last_days`: Number of days to look back for price data (default: "4")
- `api.amount`: Number of results to retrieve from the API (default: "3")

## Usage
The configuration file is loaded by the application at startup. If the file doesn't exist, a default configuration will be created automatically.

You can modify the configuration file to match your system settings and preferences:

1. Adjust the resolution to match your game's resolution
2. Update the Tesseract OCR path if it's installed in a different location
3. Change the API settings to retrieve more or less price data

## Command Line Override
Some configuration parameters can be overridden via command line arguments when starting the application:

```
python main.py --height 1080 --width 1920
```

This will override the resolution settings in the configuration file.

## Notes
- All paths should use Windows-style backslashes (`\\`) or escaped backslashes (`\\\\`)
- The configuration file is automatically created with default values if it doesn't exist
- Changes to the configuration file take effect the next time the application is started