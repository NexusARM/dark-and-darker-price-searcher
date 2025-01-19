from ImageProcessor import ImageProcessor
from apiUser import PriceSearcher
import keyboard
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(message)s')

def process_image_and_search_price():
    try:
        imageProcessor = ImageProcessor(1440, 2560)
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

keyboard.add_hotkey('shift+p', process_image_and_search_price)

print("Press Shift+P to process image and search price.")
keyboard.wait('esc')