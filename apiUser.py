import requests

class PriceSearcher:
    def __init__(self, info_file_path="info.txt"):
        self.info_file_path = info_file_path
        self.url = None
        self.headers = {}
        self.body = []
        self.response_data = None
        self.final_price = None
        self.estimated_price = None
        self.demand= None
        self.load_info({}, [], "common")  # Call load_info method with empty dictionary and list

    def load_info(self, name, rolls, rarity):
        with open(self.info_file_path, 'r') as file:
            lines = file.readlines()
        
        self.url = lines[1].strip()
        header_start = lines.index('headers\n') + 1

        for line in lines[header_start:]:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                self.headers[key.strip()] = value.strip()
                

        self.body = [
            {
            "Name": name,
            "Rarity": rarity,
            "Roll1": rolls[0][0] if len(rolls) > 0 else "0.0",
            "Itemroll1": rolls[0][1] if len(rolls) > 0 else "1",
            "Roll2": rolls[1][0] if len(rolls) > 1 else "0.0",
            "Itemroll2": rolls[1][1] if len(rolls) > 1 else "1",
            "Roll3": rolls[2][0] if len(rolls) > 2 else "0.0",
            "Itemroll3": rolls[2][1] if len(rolls) > 2 else "1",
            "Roll4": rolls[3][0] if len(rolls) > 3 else "0.0",
            "Itemroll4": rolls[3][1] if len(rolls) > 3 else "1",
            "Roll5": rolls[4][0] if len(rolls) > 4 else "0.0",
            "Itemroll5": rolls[4][1] if len(rolls) > 4 else "1",
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
                    if 'estimated_demand' in item:
                        self.demand = item['estimated_demand']
                elif isinstance(item, list):
                    for sub_item in item:
                        if isinstance(sub_item, dict):
                            if 'final_price' in sub_item:
                                self.final_price = sub_item['final_price']
                            if 'estimated_price' in sub_item:
                                self.estimated_price = sub_item['estimated_price']
                            if 'estimated_demand' in sub_item:
                                self.demand = sub_item['estimated_demand']
        else:
            print("'result' key not found in the response")
        return [self.final_price, self.estimated_price, self.demand]
            
    def execution(self, name, stat, rarity):
        self.load_info(name, stat, rarity)
        self.make_request()
        return self.extract_prices()
