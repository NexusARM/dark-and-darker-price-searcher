# ImageProcessor.py Documentation

## Overview
The `ImageProcessor` class is responsible for processing screenshots from the game "Dark and Darker" to identify items and extract their stats. It uses computer vision techniques and optical character recognition (OCR) to analyze game images.

## Dependencies
- OpenCV (cv2)
- NumPy
- Pytesseract (OCR engine)
- PIL (Python Imaging Library)
- Standard libraries: difflib, re, os, logging

## Class: ImageProcessor

### Initialization
```python
def __init__(self, resolution_height: int, resolution_width: int, tesseract_path: str = None, screenshot_dir: str = None, data_dir: str = None)
```

**Parameters:**
- `resolution_height`: The height of the game resolution
- `resolution_width`: The width of the game resolution
- `tesseract_path`: Path to the Tesseract OCR executable (optional)
- `screenshot_dir`: Directory to save screenshots (optional)
- `data_dir`: Directory containing item data files (optional)

### Methods

#### `_capture_screenshot(self)`
Captures a screenshot of the current screen.

**Returns:**
- A PIL Image object containing the screenshot

#### `_load_stats(self)`
Loads the list of possible item stats from the data directory.

#### `_load_items(self)`
Loads item name lists from various data files.

#### `find_image_in_screenshot(self, template_path: str)`
Finds a template image within the current screenshot.

**Parameters:**
- `template_path`: Path to the template image to find

**Returns:**
- Tuple containing match value and coordinates of the match

#### `find_and_crop_image(self, template_path: str = "border.png", offset_multiplier: int = 1)`
Finds a template in the screenshot and crops the image around it.

**Parameters:**
- `template_path`: Path to the template image (default: "border.png")
- `offset_multiplier`: Multiplier for the crop offset (default: 1)

**Returns:**
- Tuple containing the cropped image, match value, item name, and stats

#### `find_and_crop_image_with_retry(self, template_path: str = "border.png", max_retries: int = 5)`
Attempts to find and crop an image multiple times with retries.

**Parameters:**
- `template_path`: Path to the template image (default: "border.png")
- `max_retries`: Maximum number of retry attempts (default: 5)

**Returns:**
- Tuple containing the cropped image, match value, item name, and stats

#### `extract_text_from_image(self, image: Image.Image)`
Extracts text from an image using color filtering and OCR.

**Parameters:**
- `image`: PIL Image to extract text from

**Returns:**
- Extracted text as a string

#### `extract_name_and_stat(self, text: str)`
Parses the extracted text to identify item name and stats.

**Parameters:**
- `text`: Text extracted from the image

**Returns:**
- Tuple containing the item name and a list of stats

#### `_extract_stats_from_lines(self, stat_lines: List[str])`
Helper method to extract stats from text lines.

**Parameters:**
- `stat_lines`: List of text lines containing stats

**Returns:**
- List of extracted stats

#### `_extract_item_from_lines(self, item_name: str)`
Helper method to identify the correct item name.

**Parameters:**
- `item_name`: Raw item name text

**Returns:**
- Corrected item name

## Usage Example
```python
# Initialize the image processor
processor = ImageProcessor(
    resolution_height=1080,
    resolution_width=1920,
    tesseract_path="C:/Program Files/Tesseract-OCR/tesseract.exe",
    screenshot_dir="screenshots",
    data_dir="data"
)

# Capture and process an item
cropped_image, match_value, item_name, stats = processor.find_and_crop_image_with_retry()

# Print the results
print(f"Item: {item_name}")
print(f"Stats: {stats}")
```

## Notes
- The class uses color filtering to identify text of different rarities (Uncommon, Rare, Epic, Legendary)
- It saves intermediate images for debugging purposes in the screenshot directory
- It uses fuzzy matching to correct OCR errors when identifying item names