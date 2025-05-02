# Dark and Darker Price Searcher Documentation

## Overview
The Dark and Darker Price Searcher is a tool designed to help players of the game "Dark and Darker" quickly check the market value of items. It works by capturing screenshots of items in the game, extracting their information using OCR (Optical Character Recognition), and then searching for price data using an external API.

## Features
- Screenshot capture of in-game items
- OCR text extraction to identify item names and stats
- Price searching using an external API
- User-friendly interface with hotkey support
- Configurable settings for different screen resolutions

## Files Documentation

### Core Files
- [main.py](main.md) - Main entry point of the application
- [ImageProcessor.py](ImageProcessor.md) - Handles image processing and OCR
- [apiUser.py](apiUser.md) - Handles API requests for price data

### Configuration Files
- [config.json](config.md) - Configuration settings for the application

### Utility Files
- [launcher.bat](launcher.md) - Windows batch script to launch the application

### Data Files
- [Data Files](data_files.md) - Documentation for the data files used by the application

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Tesseract OCR installed
- Required Python packages (see requirements.txt)

### Installation
1. Clone or download the repository
2. Install required packages: `pip install -r requirements.txt`
3. Ensure Tesseract OCR is installed and update the path in config.json if necessary
4. Run the application using launcher.bat or `python main.py`

### Usage
1. Start the application using launcher.bat or `python main.py`
2. In the game, hover over an item to view its details
3. Press Shift+P to capture a screenshot and search for price information
4. View the results in the console window
5. Press ESC to exit the application

## Configuration
The application can be configured by editing the [config.json](config.md) file or by using command line arguments. See the [config.json documentation](config.md) for more details.

## Directory Structure
- `data/` - Contains item data files
- `screenshots/` - Directory for saving screenshots
- `debug/` - Directory for debug information
- `doc/` - Documentation files

## Troubleshooting
- If the application fails to recognize items, try adjusting your game's resolution to match the settings in config.json
- Ensure Tesseract OCR is correctly installed and the path in config.json is correct
- Check the error.log file for detailed error information

## Contributing
Contributions to improve the application are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License
This project is licensed under the terms of the license included in the repository.
