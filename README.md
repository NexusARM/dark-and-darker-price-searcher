# 🔍 **Dark and Darker Price Searcher**

A tool to quickly look up item prices from [DND Prices](https://www.dndprices.com/) while playing Dark and Darker.

## ✨ **Features**

- **Automatic Screenshot Capture**: Press a hotkey to capture the current item on screen
- **OCR Text Recognition**: Extracts item name and stats from the screenshot
- **Price Lookup**: Automatically searches for current market prices
- **Configurable Settings**: Easy to customize via configuration file
- **Improved Error Handling**: Robust error recovery and logging
- **Type Annotations**: Full Python type hints for better code quality

## 🛠 **Installation**

To use this program, follow these simple steps:

1. **Install Tesseract OCR:**
   - Download and install from: [Tesseract OCR - UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - The default installation path is `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - If you install to a different location, update the path in the config.json file

2. **Install Python and Dependencies:**
   - Download and install Python 3.8 or newer (if not already installed)
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```

## 🖍 **Program Description**

This program helps you quickly look up item prices on [DND Prices](https://www.dndprices.com/) during gameplay. It consists of three main components:

### 1️⃣ **ImageProcessor**

This component extracts text from the game screen:

- Takes a screenshot of the item description
- Identifies and crops the text box around the description
- Filters and processes the text for accurate recognition using OCR
- Matches extracted text to known item names and stats

> **Important:** Ensure the item description is fully visible in the game for the best results.

### 2️⃣ **PriceSearcher**

This component uses the data from the **ImageProcessor** to:

- Make an API call to the DND Prices service
- Process the response to extract price information
- Return estimated price, final price, and demand information

### 3️⃣ **Main Program**

The `main.py` script:

- Manages configuration settings
- Handles command-line arguments
- Registers hotkeys for capturing screenshots
- Coordinates the workflow between components
- Displays results in a user-friendly format

## 🚀 **How to Use the Program**

### Configuration

The program uses a `config.json` file for settings. A default configuration is created on first run, but you can modify it to match your setup:

```json
{
    "resolution": {
        "height": 1080,
        "width": 1920
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

### Running the Program

1. **Using the Launcher:**
   - Run `launcher.bat` to start the program
   - The program will use settings from `config.json`

2. **Using Command Line:**
   - You can also run the program directly with optional parameters:
   ```bash
   python main.py --height 1080 --width 1920 --config custom_config.json
   ```

3. **Using the Program:**
   - In the game, hover over an item to view its description
   - Press **Shift + P** to capture and process the item
   - The terminal will display the item information and price details
   - Press **ESC** to exit the program

## 📚 **Documentation**

Comprehensive documentation is available in the `doc` folder:

- **[index.md](doc/index.md)**: Main documentation entry point with overview and links
- **[main.py](doc/main.md)**: Documentation for the main program
- **[ImageProcessor.py](doc/ImageProcessor.md)**: Documentation for the image processing component
- **[apiUser.py](doc/apiUser.md)**: Documentation for the price searching component
- **[config.json](doc/config.md)**: Documentation for configuration options
- **[launcher.bat](doc/launcher.md)**: Documentation for the launcher script
- **[data_files.md](doc/data_files.md)**: Documentation for the data files

The documentation provides detailed information about each component, including:
- Purpose and functionality
- Class and method descriptions
- Parameters and return values
- Usage examples
- Notes and tips

## 🔄 **Recent Improvements**

The codebase has been significantly upgraded to improve quality and maintainability:

- **Configuration System**: Added a JSON-based configuration system
- **Command Line Arguments**: Support for overriding configuration via command line
- **Type Annotations**: Added Python type hints throughout the codebase
- **Comprehensive Documentation**: Added detailed docstrings to all functions and classes
- **Enhanced Error Handling**: Improved error recovery and detailed logging
- **Code Organization**: Refactored code into smaller, more focused methods
- **Performance Optimizations**: Improved image processing and API handling
- **User Experience**: Better formatted output with emoji indicators

## 💡 **Future Improvements**

- **Graphical User Interface**: Add a GUI for easier configuration and use
- **Multiple Item Support**: Process multiple items in sequence
- **Historical Price Tracking**: Track price changes over time
- **Item Comparison**: Compare prices between similar items
- **Offline Mode**: Cache recent price data for offline use

## 📨 **Contact**

For questions, issues, or suggestions, feel free to reach out!

**Thank you for using the program!** 🚀

If you wish to contribute to the development, you can open an issue on GitHub or contact me directly on Discord.

👤 **Username:** nexusarm
