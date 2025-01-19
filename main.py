from ImageProcessor import ImageProcessor
from apiUser import PriceSearcher
import keyboard
import logging
import sys

global number1, number2

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(message)s')

def process_image_and_search_price():
    try:
        imageProcessor = ImageProcessor(number1, number2)
        cropped_image, match_val = imageProcessor.find_and_crop_image()
        if cropped_image:
            text = imageProcessor.extract_text_from_image(cropped_image)
            name, stat = imageProcessor.extract_name_and_stat(text)
            if name and stat:
                print("Extracted name:", name)
                print("Extracted stat:", stat)
                price_searcher = PriceSearcher()
                price_searcher.execution(name, stat)
                print("Estimated price:", price_searcher.estimated_price)
                print("Final price:", price_searcher.final_price)
            else:
                print("Name or stat is empty, skipping click operation.")
        else:
            print("Template not found in the screenshot.")
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
