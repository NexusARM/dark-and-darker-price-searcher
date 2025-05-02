# apiUser.py Documentation

## Overview
The `apiUser.py` file contains the `PriceSearcher` class, which is responsible for retrieving price information for Dark and Darker game items from an external API. It handles the creation of API requests, processing of responses, and extraction of relevant price data.

## Dependencies
- requests
- Standard libraries: os, json, logging
- Typing annotations

## Class: PriceSearcher

### Initialization
```python
def __init__(self, info_file_path: str = "data/info.txt", last_days: str = "4", amount: str = "3")
```

**Parameters:**
- `info_file_path`: Path to the information file (default: "data/info.txt")
- `last_days`: Number of days to look back for price data (default: "4")
- `amount`: Number of results to retrieve (default: "3")

### Methods

#### `load_info(self, name: str, rolls: List[Tuple[str, str]], rarity: str)`
Loads item information and prepares it for API request.

**Parameters:**
- `name`: Name of the item
- `rolls`: List of tuples containing stat name and value
- `rarity`: Rarity of the item

**Returns:**
- Boolean indicating success or failure

#### `_determine_rarity_from_rolls(self, rolls: List[Tuple[str, str]])`
Helper method to determine item rarity based on its stats.

**Parameters:**
- `rolls`: List of tuples containing stat name and value

**Returns:**
- String representing the item rarity

#### `_create_request_body(self, name: str, rolls: List[Tuple[str, str]], rarity: str)`
Creates the request body for the API call.

**Parameters:**
- `name`: Name of the item
- `rolls`: List of tuples containing stat name and value
- `rarity`: Rarity of the item

**Returns:**
- Dictionary containing the request body

#### `make_request(self)`
Makes the API request to retrieve price data.

**Returns:**
- Boolean indicating success or failure

#### `extract_prices(self)`
Extracts price information from the API response.

**Returns:**
- List of dictionaries containing price information

#### `_process_result_data(self, result_data: Any)`
Processes the raw result data from the API.

**Parameters:**
- `result_data`: Raw result data from the API

**Returns:**
- Processed result data

#### `_extract_price_from_item(self, item: Any)`
Extracts price information from a single item in the API response.

**Parameters:**
- `item`: Item data from the API response

**Returns:**
- Dictionary containing extracted price information

#### `execution(self, name: str, stat: List[Tuple[str, str]], rarity: str)`
Main execution method that performs the entire price search process.

**Parameters:**
- `name`: Name of the item
- `stat`: List of tuples containing stat name and value
- `rarity`: Rarity of the item

**Returns:**
- List of dictionaries containing price information

## Usage Example
```python
# Initialize the price searcher
searcher = PriceSearcher(
    info_file_path="data/info.txt",
    last_days="7",
    amount="5"
)

# Search for an item
item_name = "Steel Sword"
item_stats = [("Damage", "10"), ("Durability", "100")]
item_rarity = "Uncommon"

# Get price information
prices = searcher.execution(item_name, item_stats, item_rarity)

# Print the results
for price in prices:
    print(f"Price: {price['price']} gold")
    print(f"Date: {price['date']}")
    print(f"Seller: {price['seller']}")
    print("---")
```

## Notes
- The class uses an external API to retrieve price data for Dark and Darker items
- It can determine item rarity based on the stats if not provided
- The API response is processed to extract relevant price information
- Error handling is implemented to handle API request failures