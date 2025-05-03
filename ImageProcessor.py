import difflib
import logging
import os
import re
from typing import List, Tuple, Optional, Sequence

import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab, Image, ImageEnhance


class ImageProcessor:
    """
    A class for processing screenshots to extract item information from Dark and Darker game.

    This class handles screenshot capture, image processing, text extraction, and item/stat recognition.
    """

    # Default paths that can be overridden
    DEFAULT_TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    DEFAULT_SCREENSHOT_DIR = "screenshots"
    DEFAULT_DATA_DIR = "data"

    def __init__(self, resolution_height: int, resolution_width: int, 
                 tesseract_path: str = None, 
                 screenshot_dir: str = None,
                 data_dir: str = None):
        """
        Initialize the ImageProcessor with screen resolution and optional configuration.

        Args:
            resolution_height: Height of the screen resolution
            resolution_width: Width of the screen resolution
            tesseract_path: Path to Tesseract OCR executable (optional)
            screenshot_dir: Directory to save screenshots (optional)
            data_dir: Directory containing data files (optional)
        """
        self.grade = "Common"
        self.resolution_height = resolution_height
        self.resolution_width = resolution_width
        self.tesseract_path = tesseract_path or self.DEFAULT_TESSERACT_PATH
        self.screenshot_dir = screenshot_dir or self.DEFAULT_SCREENSHOT_DIR
        self.data_dir = data_dir or self.DEFAULT_DATA_DIR

        # Ensure screenshot directory exists
        os.makedirs(self.screenshot_dir, exist_ok=True)

        # Capture and enhance screenshot
        self.screenshot = self._capture_screenshot()

        # Configure Tesseract
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        # Load stat and item data
        self.list_of_stat = self._load_stats()
        self.list_of_item = self._load_items()

    def _capture_screenshot(self) -> Image.Image:
        """Capture and enhance a screenshot of the specified resolution."""
        try:
            screenshot = ImageGrab.grab(bbox=(0, 0, self.resolution_width, self.resolution_height)).convert("RGB")
            enhancer = ImageEnhance.Sharpness(screenshot)
            enhanced_screenshot = enhancer.enhance(1)
            screenshot_path = os.path.join(self.screenshot_dir, "screenshot.png")
            enhanced_screenshot.save(screenshot_path)
            return enhanced_screenshot
        except Exception as e:
            logging.error(f"Failed to capture screenshot: {e}")
            raise

    def _load_stats(self) -> List[str]:
        """Load the list of possible item stats from file."""
        try:
            stats_path = os.path.join(self.data_dir, 'randomStat')
            with open(stats_path, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            logging.error(f"Error loading stats: {e}")
            return []

    def _load_items(self) -> List[str]:
        """Load the list of possible item names from multiple files."""
        items = []
        try:
            file_paths = [
                os.path.join(self.data_dir, 'itemsName.txt'),
                os.path.join(self.data_dir, 'specialItemName.txt'),
                os.path.join(self.data_dir, 'pendantAndRingName.txt')
            ]

            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    items.extend(line.strip() for line in f)
            return items
        except Exception as e:
            logging.error(f"Error reading item files: {e}")
            return items

    def find_image_in_screenshot(self, template_path: str) -> tuple[None, None, int] | tuple[
        Sequence[int], tuple[int, int], float | int]:
        """
        Find a template image within the screenshot using template matching.

        Args:
            template_path: Path to the template image file

        Returns:
            Tuple containing:
                - top_left coordinates (or None if not found)
                - bottom_right coordinates (or None if not found)
                - match confidence value (0-1)
        """
        try:
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                logging.error(f"Failed to load template image from {template_path}")
                return None, None, 0

            template_w, template_h = template.shape[::-1]
            screenshot_cv = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2GRAY)
            best_match_val, best_match_loc, best_match_scale = 0, None, 1

            # Try different scales to find the best match
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
                bottom_right = (top_left[0] + int(template_w * best_match_scale),
                                top_left[1] + int(template_h * best_match_scale))
                return top_left, bottom_right, best_match_val

            return None, None, 0

        except Exception as e:
            logging.error(f"Error in find_image_in_screenshot: {e}")
            return None, None, 0

    def find_and_crop_image(self, template_path: str = "border.png", offset_multiplier: int = 1) -> Tuple[Optional[Image.Image], float]:
        """
        Find a template in the screenshot and crop the region of interest.

        Args:
            template_path: Path to the template image file
            offset_multiplier: Multiplier to adjust the top offset for cropping

        Returns:
            Tuple containing:
                - Cropped image (or None if template not found)
                - Match confidence value (0-1)
        """
        try:
            top_left, bottom_right, match_val = self.find_image_in_screenshot(template_path)
            if top_left and bottom_right:
                height = bottom_right[1] - top_left[1]
                new_right_x = bottom_right[0] + int(height * 1.5)
                # Apply the offset multiplier to adjust the top coordinate
                top_offset = 200 + 60 * offset_multiplier

                # Ensure crop coordinates are within image bounds
                crop_left = max(0, top_left[0])
                crop_top = max(0, top_left[1] - top_offset)
                crop_right = min(self.resolution_width, new_right_x)
                crop_bottom = min(self.resolution_height, bottom_right[1])

                cropped_image = self.screenshot.crop((crop_left, crop_top, crop_right, crop_bottom))
                return cropped_image, match_val
            return None, 0
        except Exception as e:
            logging.error(f"Error in find_and_crop_image: {e}")
            return None, 0

    def find_and_crop_image_with_retry(self, template_path: str = "border.png", max_retries: int = 5) -> Tuple[Optional[Image.Image], float, str, List[Tuple[str, str]]]:
        """
        Find and crop an image with multiple attempts, adjusting the offset each time.

        This method tries to find the template in the screenshot multiple times with
        different offset multipliers until it successfully identifies an item.

        Args:
            template_path: Path to the template image file
            max_retries: Maximum number of retry attempts

        Returns:
            Tuple containing:
                - Cropped image (or None if failed)
                - Match confidence value (0-1)
                - Item name (or "Unknown Item" if not identified)
                - List of item stats as (stat_name, value) tuples
        """
        name = "Unknown Item"
        stats = []
        cropped_image = None
        match_val = 0

        try:
            for attempt in range(1, max_retries + 1):
                cropped_image, match_val = self.find_and_crop_image(template_path, offset_multiplier=attempt)

                if not cropped_image:
                    continue

                # Save the cropped image for debugging
                debug_path = os.path.join(self.screenshot_dir, "cropped_image.png")
                cropped_image.save(debug_path)

                text = self.extract_text_from_image(cropped_image)
                name, stats = self.extract_name_and_stat(text)

                if name != "Unknown Item":
                    return cropped_image, match_val, name, stats

            # If we get here, we've exhausted all retries
            if cropped_image:
                return cropped_image, match_val, name, stats
            return None, 0, name, stats

        except Exception as e:
            logging.error(f"Error in find_and_crop_image_with_retry: {e}")
            return None, 0, "Unknown Item", []

    def extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extract text from an image using color filtering and OCR.

        This method filters the image to keep only text of specific colors
        (corresponding to different item rarities in the game), then uses
        Tesseract OCR to extract the text.

        Args:
            image: PIL Image to extract text from

        Returns:
            Extracted text as a string
        """
        try:
            # Game text colors for different rarities
            target_colors = [
                (99, 201, 0),    # Green (Uncommon)
                (0, 136, 255),   # Blue (Rare)
                (193, 73, 255),  # Purple (Epic)
                (255, 128, 0)    # Orange (Legendary)
            ]

            np_image = np.array(image.convert("RGB"))
            mask = np.zeros((np_image.shape[0], np_image.shape[1]), dtype=np.uint8)

            # Create a mask that keeps only pixels close to the target colors
            for color in target_colors:
                lower_bound = np.array([max(0, c - 50) for c in color])
                upper_bound = np.array([min(255, c + 50) for c in color])
                color_mask = cv2.inRange(np_image, lower_bound, upper_bound)
                mask = cv2.bitwise_or(mask, color_mask)

            # Apply the mask to the image
            masked_image = cv2.bitwise_and(np_image, np_image, mask=mask)
            pil_masked_image = Image.fromarray(masked_image)

            # Save for debugging
            debug_path = os.path.join(self.screenshot_dir, "masked_image.png")
            pil_masked_image.save(debug_path)

            # Extract text using OCR
            text = pytesseract.image_to_string(pil_masked_image)

            # Detect item rarity and remove it from the text
            words_to_remove = ["Uncommon", "Rare", "Epic", "Legendary", "Unique"]
            for word in words_to_remove:
                if word in text:
                    text = text.replace(word, "")
                    self.grade = word
                    break

            return text

        except Exception as e:
            logging.error(f"Error in extract_text_from_image: {e}")
            return ""

    def extract_name_and_stat(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Extract item name and stats from OCR text.

        Args:
            text: Text extracted from the image

        Returns:
            Tuple containing:
                - Item name (or "Unknown Item" if not identified)
                - List of item stats as (stat_name, value) tuples
        """
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            # If the first line starts with + or -, we're looking at stats without an item name
            if lines and (lines[0].startswith('+') or lines[0].startswith('-')):
                stat_lines = lines
                stats = self._extract_stats_from_lines(stat_lines)
                name = "Unknown Item"
            else:
                # First line is the item name, remaining lines are stats
                name = lines[0] if lines else ""
                # Match the extracted name to known items
                name = self._extract_item_from_lines(name)
                stat_lines = lines[1:] if len(lines) > 1 else []
                stats = self._extract_stats_from_lines(stat_lines)

            # Log the extracted stats for debugging
            logging.info(f"Extracted stats: {[stat[1] for stat in stats]}")

            return name, stats

        except Exception as e:
            logging.error(f"Error in extract_name_and_stat: {e}")
            return "Unknown Item", []

    def _extract_stats_from_lines(self, stat_lines: List[str]) -> List[Tuple[str, str]]:
        """
        Extract stat names and values from text lines.

        Args:
            stat_lines: List of text lines containing stat information

        Returns:
            List of tuples containing (stat_name, value)
        """
        stats = []
        try:
            for line in stat_lines:
                # Remove leading + or - symbols
                clean_line = line.lstrip('+-')

                # Extract numeric value using regex
                value_match = re.search(r'(\d+\.?\d*)', clean_line)
                value = value_match.group(1) if value_match else '0'

                # Remove the numeric part to get the stat name
                stat_name = re.sub(r'\d+\.?\d*\s*%?\s*', '', clean_line).strip()

                # Match the stat name to known stats
                if stat_name in self.list_of_stat:
                    matched_stat = stat_name
                else:
                    # Use fuzzy matching to find the closest stat name
                    matches = difflib.get_close_matches(stat_name, self.list_of_stat, n=1, cutoff=0.0)
                    matched_stat = matches[0] if matches else stat_name

                stats.append((matched_stat, value))

            return stats

        except Exception as e:
            logging.error(f"Error in _extract_stats_from_lines: {e}")
            return stats

    def _extract_item_from_lines(self, item_name: str) -> str:
        """
        Match an extracted item name to the list of known items.

        Args:
            item_name: Raw item name extracted from OCR

        Returns:
            Matched item name or the original if no match found
        """
        try:
            # Check if the item name is an exact match
            if item_name in self.list_of_item:
                return item_name
            else:
                # Use fuzzy matching to find the closest item name
                matches = difflib.get_close_matches(item_name, self.list_of_item, n=1, cutoff=0.0)
                matched_name = matches[0] if matches else item_name

                # Log if we had to use fuzzy matching
                if matches and matched_name != item_name:
                    logging.info(f"Fuzzy matched item: '{item_name}' -> '{matched_name}'")

                return matched_name

        except Exception as e:
            logging.error(f"Error in _extract_item_from_lines: {e}")
            return item_name
