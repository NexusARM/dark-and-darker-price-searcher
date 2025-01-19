import requests
import json

class PriceSearcher:
    def __init__(self, info_file_path="info.txt"):
        self.info_file_path = info_file_path
        self.url = None
        self.headers = {}
        self.body = []
        self.response_data = None
        self.final_price = None
        self.estimated_price = None
        self.load_info({}, [])  # Call load_info method with empty dictionary and list

    def load_info(self, name, rolls):
        with open(self.info_file_path, 'r') as file:
            lines = file.readlines()
        
        self.url = lines[1].strip()
        header_start = lines.index('headers\n') + 1

        for line in lines[header_start:]:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                self.headers[key.strip()] = value.strip()

        # Construct the body from data and rolls
        rarity = "Unknown"
        if len(rolls) == 1:
            rarity = "Uncommon"
        elif len(rolls) == 2:
            rarity = "Rare"
        elif len(rolls) == 3:
            rarity = "Epic"
        elif len(rolls) == 4:
            rarity = "Legendary"

        self.body = [
            {
            "Name": name,
            "Rarity": rarity,
            "Roll1": rolls[0] if len(rolls) > 0 else "0.0",
            "Itemroll1": "1",
            "Roll2": rolls[1] if len(rolls) > 1 else "0.0",
            "Itemroll2": "1",
            "Roll3": rolls[2] if len(rolls) > 2 else "0.0",
            "Itemroll3": "1",
            "Roll4": rolls[3] if len(rolls) > 3 else "0.0",
            "Itemroll4": "1",
            "Roll5": rolls[4] if len(rolls) > 4 else "0.0",
            "Itemroll5": "1",
            "Lastdays": "4",
            "Amount": "3"
            }
        ]

    def make_request(self):
        response = requests.post(self.url, headers=self.headers, json=self.body)
        self.response_data = response.json()

    def extract_prices(self):
        if 'result' in self.response_data:
            for item in self.response_data['result']:
                if isinstance(item, dict):
                    if 'final_price' in item:
                        self.final_price = item['final_price']
                    if 'estimated_price' in item:
                        self.estimated_price = item['estimated_price']
                elif isinstance(item, list):
                    for sub_item in item:
                        if isinstance(sub_item, dict):
                            if 'final_price' in sub_item:
                                self.final_price = sub_item['final_price']
                            if 'estimated_price' in sub_item:
                                self.estimated_price = sub_item['estimated_price']
        else:
            print("'result' key not found in the response")
        return [self.final_price, self.estimated_price]

            
    def execution(self, name, stat):
        self.load_info(name, stat)
        self.make_request()
        return self.extract_prices()
