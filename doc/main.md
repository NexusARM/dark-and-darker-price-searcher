# main.py Documentation

## Overview
The `main.py` file is the main entry point for the Dark and Darker Price Searcher application. It integrates the `ImageProcessor` and `PriceSearcher` classes to capture screenshots of items in the game, extract their information, and search for price data.

## Dependencies
- ImageProcessor (local module)
- apiUser (local module)
- keyboard
- Standard libraries: logging, sys, os, json, argparse
- Typing annotations

## Constants
- `DEFAULT_CONFIG_FILE`: Default configuration file path ('config.json')
- `DEFAULT_CONFIG`: Default configuration dictionary containing:
  - Resolution settings
  - Tesseract OCR path
  - Screenshot directory
  - Data directory
  - API settings

## Functions

### `load_config(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]`
Loads configuration from a JSON file or creates a default configuration if the file doesn't exist.

**Parameters:**
- `config_file`: Path to the configuration file (default: 'config.json')

**Returns:**
- Dictionary containing configuration values

### `process_image_and_search_price(config: Dict[str, Any]) -> None`
Processes a screenshot to extract item information and search for price data.

**Parameters:**
- `config`: Application configuration dictionary

**Process:**
1. Captures a screenshot
2. Processes the image to extract item information
3. Searches for price information using the API
4. Displays the results

### `parse_arguments()`
Parses command line arguments.

**Returns:**
- Parsed arguments

**Arguments:**
- `--config`: Path to configuration file
- `--height`: Screen height (overrides config file)
- `--width`: Screen width (overrides config file)

### `main()`
Main entry point of the application.

**Process:**
1. Parses command line arguments
2. Loads configuration
3. Overrides configuration with command line arguments if provided
4. Ensures required directories exist
5. Displays startup information
6. Registers hotkeys
7. Waits for user input

## Hotkeys
- `Shift+P`: Capture screenshot and search price
- `ESC`: Exit application

## Usage
The application can be run directly from the command line:

```
python main.py [--config CONFIG_FILE] [--height HEIGHT] [--width WIDTH]
```

### Examples

**Run with default settings:**
```
python main.py
```

**Run with custom configuration file:**
```
python main.py --config my_config.json
```

**Run with custom resolution:**
```
python main.py --height 1080 --width 1920
```

## Configuration
The application uses a JSON configuration file with the following structure:

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

If the configuration file doesn't exist, a default one will be created.

## Notes
- The application uses the keyboard library to register hotkeys
- It creates necessary directories if they don't exist
- Error handling is implemented to catch and log exceptions
- The application displays user-friendly messages with emoji icons