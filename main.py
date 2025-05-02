import argparse
import json
import logging
import os
from typing import Dict, Any

import keyboard

from ImageProcessor import ImageProcessor
from apiUser import PriceSearcher

# Constants
DEFAULT_CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    "resolution": {
        "height": 1440,
        "width": 2560
    },
    "tesseract_path": r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    "screenshot_dir": "screenshots",
    "data_dir": "data",
    "api": {
        "info_file": "data/info.txt",
        "last_days": "4",
        "amount": "3"
    }
}

def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    """
    Load configuration from a JSON file or create default if not exists.

    Args:
        config_file: Path to the configuration file

    Returns:
        Dictionary containing configuration values
    """
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config
        else:
            # Create default config file
            with open(config_file, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
                return DEFAULT_CONFIG
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return DEFAULT_CONFIG


def process_image_and_search_price(config: Dict[str, Any]) -> None:
    """
    Process a screenshot to extract item information and search for price.

    This function:
    1. Captures a screenshot
    2. Processes the image to extract item information
    3. Searches for price information using the API
    4. Displays the results

    Args:
        config: Application configuration dictionary
    """
    try:
        # Create ImageProcessor with configuration
        image_processor = ImageProcessor(
            resolution_height=config["resolution"]["height"],
            resolution_width=config["resolution"]["width"],
            tesseract_path=config.get("tesseract_path"),
            screenshot_dir=config.get("screenshot_dir"),
            data_dir=config.get("data_dir")
        )

        # Use the method with retry logic to find and process the item
        result = image_processor.find_and_crop_image_with_retry()

        if result is None or len(result) < 4:
            logging.warning("Template not found in the screenshot.")
            print("❌ Item not found in the screenshot.")
            return

        cropped_image, match_val, name, stat = result

        if name and stat:
            # Display extracted information
            print(f"📋 Item Information:")
            print(f"  • Name: {name}")
            print(f"  • Rarity: {image_processor.grade}")
            print(f"  • Stats: {', '.join([f'{s[0]}: {s[1]}' for s in stat])}")

            # Create PriceSearcher with configuration
            price_searcher = PriceSearcher(
                info_file_path=config["api"]["info_file"],
                last_days=config["api"]["last_days"],
                amount=config["api"]["amount"]
            )

            # Search for price information
            price_searcher.execution(name, stat, image_processor.grade)

            # Display price information
            print(f"\n💰 Price Information:")
            print(f"  • Estimated price: {price_searcher.estimated_price or 'Unknown'}")
            print(f"  • Final price: {price_searcher.final_price or 'Unknown'}")
            print(f"  • Estimated demand: {price_searcher.demand or 'Unknown'}")
        else:
            logging.warning("Name or stat is empty, skipping price search.")
            print("❌ Could not extract item information from the screenshot.")
    except Exception as e:
        logging.error("An error occurred during processing", exc_info=True)
        print("❌ An error occurred. Check the error.log file for more details.")

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Dark and Darker Price Searcher')
    parser.add_argument('--config', type=str, default=DEFAULT_CONFIG_FILE,
                        help=f'Path to configuration file (default: {DEFAULT_CONFIG_FILE})')
    parser.add_argument('--height', type=int, 
                        help='Screen height (overrides config file)')
    parser.add_argument('--width', type=int, 
                        help='Screen width (overrides config file)')

    return parser.parse_args()


def main():
    """
    Main entry point of the application.
    """
    # Parse command line arguments
    args = parse_arguments()

    # Load configuration
    config = load_config(args.config)

    # Override configuration with command line arguments if provided
    if args.height:
        config["resolution"]["height"] = args.height
    if args.width:
        config["resolution"]["width"] = args.width

    # Ensure required directories exist
    os.makedirs(config.get("screenshot_dir", "screenshots"), exist_ok=True)
    os.makedirs("debug", exist_ok=True)

    # Display startup information
    print(f"🔍 Dark and Darker Price Searcher")
    print(f"Resolution: {config['resolution']['width']} x {config['resolution']['height']}")
    print(f"Configuration: {args.config}")

    # Register hotkey
    keyboard.add_hotkey('shift+p', lambda: process_image_and_search_price(config))

    # Display instructions
    print("\n⌨️  Press Shift+P to capture screenshot and search price.")
    print("⌨️  Press ESC to exit.")

    # Wait for ESC key to exit
    keyboard.wait('esc')
    print("Exiting application.")


if __name__ == "__main__":
    main()

# This is handled in the load_config function
