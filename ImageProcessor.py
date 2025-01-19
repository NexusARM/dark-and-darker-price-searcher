from PIL import ImageGrab, Image
import numpy as np
import cv2
import pytesseract
import re

class ImageProcessor:
    def __init__(self, resolution_height, resolution_width):
        self.screenshot = ImageGrab.grab(bbox=(0, 0, resolution_width, resolution_height))
        self.screenshot = self.screenshot.convert("RGB")
        self.screenshot.save("screenshots/screenshot.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def find_image_in_screenshot(self, template_path):
        # Load the template image
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        template_w, template_h = template.shape[::-1]

        # Convert the screenshot to a format suitable for OpenCV
        screenshot_cv = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2GRAY)

        # Initialize variables to store the best match
        best_match_val = 0
        best_match_loc = None
        best_match_scale = 1
        # Try different scales of the template from bigger to smaller
        for scale in np.linspace(1.5, 0.5, 20):
            resized_template = cv2.resize(template, (int(template_w * scale), int(template_h * scale)))
            if resized_template.shape[0] > screenshot_cv.shape[0] or resized_template.shape[1] > screenshot_cv.shape[1]:
                continue

            # Perform template matching
            result = cv2.matchTemplate(screenshot_cv, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Update the best match if found a better one
            if max_val > best_match_val:
                best_match_val = max_val
                best_match_loc = max_loc
                best_match_scale = scale

        # Calculate the bounding box of the best match
        if best_match_loc:
            top_left = best_match_loc
            top_right = (top_left[0] + int(template_w * best_match_scale), top_left[1])
            bottom_left = (top_left[0], top_left[1] + int(template_h * best_match_scale))
            bottom_right = (top_left[0] + int(template_w * best_match_scale), top_left[1] + int(template_h * best_match_scale))
            return top_left, top_right, bottom_left, bottom_right, best_match_val

        return None, None, None, None, 0

    def find_and_crop_image(self, template_path="border.png"):
        top_left, top_right, bottom_left, bottom_right, match_val = self.find_image_in_screenshot(template_path)
        if top_left and bottom_right:
            height = bottom_right[1] - top_left[1]
            new_right_x = bottom_right[0] + int(height * 1)
            cropped_image = self.screenshot.crop((top_left[0], top_left[1], new_right_x, bottom_right[1]))
            cropped_image.save("screenshots/cropped_image.png")
            return cropped_image, match_val
        return None, 0

    def extract_text_from_image(self, image):
        # Convert the image to RGB
        image_rgb = image.convert("RGB")
        np_image = np.array(image_rgb)

        # Define the target colors
        target_colors = [(0, 161, 255), (208, 103, 255), (255, 154, 0), (128, 214, 0)]

        # Create a mask for the target colors
        mask = np.zeros((np_image.shape[0], np_image.shape[1]), dtype=np.uint8)
        for color in target_colors:
            lower_bound = np.array([max(0, c - 40) for c in color])
            upper_bound = np.array([min(255, c + 40) for c in color])
            color_mask = cv2.inRange(np_image, lower_bound, upper_bound)
            mask = cv2.bitwise_or(mask, color_mask)

        # Apply the mask to the image
        masked_image = cv2.bitwise_and(np_image, np_image, mask=mask)

        # Convert the masked image back to PIL format
        masked_image_pil = Image.fromarray(masked_image)

        # Use Tesseract to extract text from the masked image
        text = pytesseract.image_to_string(masked_image_pil)
        # Remove specific words from the extracted text
        words_to_remove = ["Uncommon", "Rare", "Epic", "Legendary"]
        for word in words_to_remove:
            text = text.replace(word, "")
        return text

    def extract_name_and_stat(self, text):
        match = re.match(r"([a-zA-Z\s]+)[+-]?\d*", text)
        name = match.group(1).strip() if match else text
        filtered_text = [line.strip() for line in " ".join(re.findall(r"[a-zA-Z\s]+", text)).split("\n") if line.strip()]
        stat = []
        for line in filtered_text:
            if "Additional" in line and "Armor" in line:
                stat.append("Armor Rating")
            elif line != name:
                stat.append(line)
        return name, stat
