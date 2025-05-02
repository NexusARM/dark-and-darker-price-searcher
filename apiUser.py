import json
import logging
import os
from typing import Dict, List, Tuple, Optional, Any

import requests


class PriceSearcher:
    """
    A class for searching and retrieving price information for Dark and Darker items.

    This class handles API interactions with the dndprices.com service to get price estimates
    for items based on their name, rarity, and stat rolls.
    """

    def __init__(self, info_file_path: str = "data/info.txt", 
                 last_days: str = "4", 
                 amount: str = "3"):
        """
        Initialize the PriceSearcher with configuration.

        Args:
            info_file_path: Path to the file containing API configuration
            last_days: Number of days of price history to consider
            amount: Number of price points to retrieve
        """
        self.info_file_path = info_file_path
        self.last_days = last_days
        self.amount = amount
        self.url = None
        self.headers = {}
        self.body = []
        self.response_data = None
        self.final_price = None
        self.estimated_price = None
        self.demand = None

        # Load API configuration
        self.load_info({}, [], "common")

    def load_info(self, name: str, rolls: List[Tuple[str, str]], rarity: str) -> None:
        """
        Load API configuration and prepare the request body.

        Args:
            name: Item name
            rolls: List of tuples containing stat rolls (value, stat_id)
            rarity: Item rarity
        """
        try:
            # Load API configuration from file
            with open(self.info_file_path, 'r') as file:
                lines = file.readlines()

            # Extract URL and headers
            self.url = lines[1].strip()
            header_start = lines.index('headers\n') + 1

            # Parse headers
            self.headers = {}
            for line in lines[header_start:]:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    self.headers[key.strip()] = value.strip()

            # Determine rarity based on number of rolls if not specified
            valid_rarities = ["Uncommon", "Rare", "Epic", "Legendary", "Unique"]
            if rarity not in valid_rarities:
                rarity = self._determine_rarity_from_rolls(rolls)

            # Prepare request body
            self.body = [self._create_request_body(name, rolls, rarity)]

        except Exception as e:
            logging.error(f"Error loading API configuration: {e}")
            # Set default values if configuration loading fails
            self.url = "https://www.dndprices.com/_api/wix-code-public-dispatcher-ng/siteview/_webMethods/backend/predict.jsw/get_offers_new.ajax"
            self.headers = {"Content-Type": "application/json"}
            self.body = [self._create_request_body(name, rolls, rarity)]

    def _determine_rarity_from_rolls(self, rolls: List[Tuple[str, str]]) -> str:
        """
        Determine item rarity based on the number of stat rolls.

        Args:
            rolls: List of tuples containing stat rolls

        Returns:
            Rarity string
        """
        if len(rolls) == 1:
            return "Uncommon"
        elif len(rolls) == 2:
            return "Rare"
        elif len(rolls) == 3:
            return "Epic"
        elif len(rolls) == 4:
            return "Legendary"
        elif len(rolls) >= 5:
            return "Unique"
        else:
            return "Common"

    def _create_request_body(self, name: str, rolls: List[Tuple[str, str]], rarity: str) -> Dict[str, str]:
        """
        Create the request body for the API call.

        Args:
            name: Item name
            rolls: List of tuples containing stat rolls (value, stat_id)
            rarity: Item rarity

        Returns:
            Dictionary containing the request body
        """
        body = {
            "Name": name,
            "Rarity": rarity,
            "Lastdays": self.last_days,
            "Amount": self.amount
        }

        # Add roll information
        for i in range(5):
            if i < len(rolls):
                body[f"Roll{i+1}"] = rolls[i][0]
                body[f"Itemroll{i+1}"] = rolls[i][1]
            else:
                body[f"Roll{i+1}"] = "0.0"
                body[f"Itemroll{i+1}"] = "1"

        return body

    def make_request(self) -> bool:
        """
        Make an API request to get price information.

        Returns:
            True if the request was successful, False otherwise
        """
        try:
            # Make the API request
            response = requests.post(self.url, headers=self.headers, json=self.body, timeout=10)

            # Check if the request was successful
            response.raise_for_status()

            # Parse the response
            self.response_data = response.json()

            # Save response for debugging
            debug_dir = "debug"
            os.makedirs(debug_dir, exist_ok=True)
            with open(os.path.join(debug_dir, "dump.json"), "w") as f:
                json.dump(self.response_data, f, indent=2)

            return True

        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            self.response_data = None
            return False
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse API response: {e}")
            self.response_data = None
            return False
        except Exception as e:
            logging.error(f"Unexpected error during API request: {e}")
            self.response_data = None
            return False

    def extract_prices(self) -> List[Optional[str]]:
        """
        Extract price information from the API response.

        Returns:
            List containing [final_price, estimated_price, demand]
        """
        # Reset price values
        self.final_price = None
        self.estimated_price = None
        self.demand = None

        try:
            if not self.response_data:
                logging.warning("No response data available")
                return [self.final_price, self.estimated_price, self.demand]

            if 'result' not in self.response_data:
                logging.warning("'result' key not found in the response")
                return [self.final_price, self.estimated_price, self.demand]

            # Process the result data
            self._process_result_data(self.response_data['result'])

            logging.info(f"Extracted prices: final={self.final_price}, estimated={self.estimated_price}, demand={self.demand}")
            return [self.final_price, self.estimated_price, self.demand]

        except Exception as e:
            logging.error(f"Error extracting prices: {e}")
            return [self.final_price, self.estimated_price, self.demand]

    def _process_result_data(self, result_data: Any) -> None:
        """
        Process the result data from the API response.

        Args:
            result_data: The 'result' field from the API response
        """
        if isinstance(result_data, list):
            for item in result_data:
                self._extract_price_from_item(item)
        else:
            self._extract_price_from_item(result_data)

    def _extract_price_from_item(self, item: Any) -> None:
        """
        Extract price information from an item in the result data.

        Args:
            item: An item from the result data
        """
        if isinstance(item, dict):
            # Extract values directly from dictionary
            if 'final_price' in item and not self.final_price:
                self.final_price = item['final_price']
            if 'estimated_price' in item and not self.estimated_price:
                self.estimated_price = item['estimated_price']
            if 'estimated_demand' in item and not self.demand:
                self.demand = item['estimated_demand']
        elif isinstance(item, list):
            # Process each item in the list
            for sub_item in item:
                self._extract_price_from_item(sub_item)

    def execution(self, name: str, stat: List[Tuple[str, str]], rarity: str) -> List[Optional[str]]:
        """
        Execute the complete price search process.

        This method performs the full workflow:
        1. Load API configuration and prepare request
        2. Make the API request
        3. Extract price information from the response

        Args:
            name: Item name
            stat: List of tuples containing stat rolls (value, stat_id)
            rarity: Item rarity

        Returns:
            List containing [final_price, estimated_price, demand]
        """
        try:
            logging.info(f"Searching price for: {name} (Rarity: {rarity}, Stats: {stat})")

            # Load configuration and prepare request
            self.load_info(name, stat, rarity)

            # Make the API request
            request_success = self.make_request()

            # Extract prices if request was successful
            if request_success:
                return self.extract_prices()
            else:
                logging.warning("Price search failed due to API request failure")
                return [None, None, None]

        except Exception as e:
            logging.error(f"Error during price search execution: {e}")
            return [None, None, None]
