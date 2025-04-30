from PIL import ImageGrab, Image, ImageEnhance
import numpy as np
import cv2
import pytesseract
import re
import difflib

class ImageProcessor:
    def __init__(self, resolution_height, resolution_width):
        self.grade = "Common"
        self.screenshot = ImageGrab.grab(bbox=(0, 0, resolution_width, resolution_height)).convert("RGB")
        enhancer = ImageEnhance.Sharpness(self.screenshot)
        self.screenshot = enhancer.enhance(1)
        self.screenshot.save("screenshots/screenshot.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def find_image_in_screenshot(self, template_path):
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        template_w, template_h = template.shape[::-1]
        screenshot_cv = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2GRAY)
        best_match_val, best_match_loc, best_match_scale = 0, None, 1

        for scale in np.linspace(1.5, 0.5, 30):
            resized_template = cv2.resize(template, (int(template_w * scale), int(template_h * scale)))
            if resized_template.shape[0] > screenshot_cv.shape[0] or resized_template.shape[1] > screenshot_cv.shape[1]:
                continue
            result = cv2.matchTemplate(screenshot_cv, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > best_match_val:
                best_match_val, best_match_loc, best_match_scale = max_val, max_loc, scale

        if best_match_loc:
            top_left = best_match_loc
            bottom_right = (top_left[0] + int(template_w * best_match_scale), top_left[1] + int(template_h * best_match_scale))
            return top_left, bottom_right, best_match_val

        return None, None, 0

    def find_and_crop_image(self, template_path="border.png"):
        top_left, bottom_right, match_val = self.find_image_in_screenshot(template_path)
        if top_left and bottom_right:
            height = bottom_right[1] - top_left[1]
            new_right_x = bottom_right[0] + int(height * 1.1)
            cropped_image = self.screenshot.crop((top_left[0], top_left[1] - 200, new_right_x, bottom_right[1]))
            return cropped_image, match_val
        return None, 0

    def extract_text_from_image(self, image):
        np_image = np.array(image.convert("RGB"))
        target_colors = [(99, 201, 0), (0, 136, 255), (193, 73, 255), (255, 128, 0)]
        mask = np.zeros((np_image.shape[0], np_image.shape[1]), dtype=np.uint8)

        for color in target_colors:
            lower_bound = np.array([max(0, c - 75) for c in color])
            upper_bound = np.array([min(255, c + 75) for c in color])
            color_mask = cv2.inRange(np_image, lower_bound, upper_bound)
            mask = cv2.bitwise_or(mask, color_mask)

        masked_image = cv2.bitwise_and(np_image, np_image, mask=mask)
        pil_masked_image = Image.fromarray(masked_image)
        pil_masked_image.save("screenshots/masked_image.png")
        text = pytesseract.image_to_string(pil_masked_image)
        words_to_remove = ["Uncommon", "Rare", "Epic", "Legendary", "Unique"]
        for word in words_to_remove:
            if word in text:
                text = text.replace(word, "")
                self.grade = word
        return text

    def extract_name_and_stat(self, text):
        match = re.match(r"([a-zA-Z\s]+)[+-]?\d*", text)
        name = match.group(1).strip() if match else text
        filtered_text = [line.strip() for line in " ".join(re.findall(r"[a-zA-Z\s]+", text)).split("\n") if line.strip()]
        filtered_modifier = [line.strip() for line in " ".join(re.findall(r"[0-9\s]+", text)).split("\n") if line.strip()]
        filtered_modifier = [re.sub(r'(?<=\d) (?=\d)', '.', s) for s in filtered_modifier]
        print(filtered_modifier)
        combined_stats = [(filtered_text[0], 0)] + list(zip(filtered_text[1:], filtered_modifier + ['0'] * (len(filtered_text) - 1 - len(filtered_modifier))))
        list_of_stat = ['All Attributes', 'Armor Penetration', 'Magical Power', 'Additional Physical Damage', 'Armor Rating', 'Magical Damage Reduction', 'True Magical Damage', 'Max Health Bonus', 'Physical Damage Reduction', 'Additional Magical Damage', 'Projectile Damage Reduction', 'Regular Interaction Speed', 'Magic Penetration', 'Physical Power', 'True Physical Damage', 'Magic Resistance', 'Additional Memory Capacity', 'Max Health', 'Debuff Duration Bonus', 'Magical Interaction Speed', 'Buff Duration Bonus', 'Spell Casting Speed', 'Memory Capacity Bonus', 'Luck', 'Action Speed', 'Will', 'Strength', 'Physical Damage Bonus', 'Dexterity', 'Magical Damage Bonus', 'Resourcefulness', 'Knowledge', 'Vigor', 'Magical Healing', 'Additional Weapon Damage', 'Physical Healing', 'Agility', 'Move Speed Bonus', 'Additional Move Speed']
        stat = [(stat_name if stat_name in list_of_stat else difflib.get_close_matches(stat_name, list_of_stat, n=1, cutoff=0.0)[0], value) for stat_name, value in combined_stats if stat_name != name]
        return name, stat
