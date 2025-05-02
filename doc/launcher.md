# launcher.bat Documentation

## Overview
The `launcher.bat` file is a simple Windows batch script that serves as a convenient way to start the Dark and Darker Price Searcher application. It provides a user-friendly method to launch the application without needing to use the command line directly.

## File Content
```batch
@echo off
echo Starting Dark and Darker Price Searcher...
python main.py
pause
```

## Purpose
- Suppresses command echoing (`@echo off`)
- Displays a startup message to the user
- Executes the main Python script (`main.py`)
- Pauses execution after the application exits to keep the console window open, allowing users to see any error messages

## Usage
To use the launcher:
1. Double-click on the `launcher.bat` file in Windows Explorer
2. The batch file will execute and start the Dark and Darker Price Searcher application
3. When you exit the application, the console window will remain open until you press any key

## Requirements
- Python must be installed and available in the system PATH
- The batch file must be located in the same directory as `main.py`

## Notes
- This launcher is designed for Windows systems only
- If you need to pass command-line arguments to the application, you would need to modify this batch file or use the command line directly
- The pause command at the end is useful for debugging as it allows users to see any error messages before the window closes