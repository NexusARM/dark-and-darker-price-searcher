import logging
import sys

import keyboard

from ImageProcessor import ImageProcessor
from apiUser import PriceSearcher

global number1, number2

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(message)s')

def process_image_and_search_price():
    try:
        imageProcessor = ImageProcessor(number1, number2)
        # Use the new method with retry logic
        result = imageProcessor.find_and_crop_image_with_retry()

        if result is None or len(result) < 4:
            print("Template not found in the screenshot.")
            return

        cropped_image, match_val, name, stat = result

        if name and stat:
            print("Extracted name:", name)
            print("Extracted stat:", stat)
            print("Extracted grade:", imageProcessor.grade)
            price_searcher = PriceSearcher()
            price_searcher.execution(name, stat, imageProcessor.grade)
            print("Estimated price:", price_searcher.estimated_price)
            print("Final price:", price_searcher.final_price)
            print("Estimated demand:", price_searcher.demand)
        else:
            print("Name or stat is empty, skipping click operation.")
    except Exception as e:
        logging.error("An error occurred", exc_info=True)
        print("An error occurred. Check the error.log file for more details.")

if len(sys.argv) != 3:
    print("Usage: python main.py <number1> <number2>")
    sys.exit(1)

try:
    number1 = int(sys.argv[1])
    number2 = int(sys.argv[2])
except ValueError:
    print("Both arguments must be integers.")
    sys.exit(1)

print(f"resolution: {number1} x {number2}")


keyboard.add_hotkey('shift+p', process_image_and_search_price)

print("Press Shift+P to process image and search price.")
keyboard.wait('esc')
