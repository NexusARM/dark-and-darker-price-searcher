# Data Files Documentation

## Overview
The Dark and Darker Price Searcher uses several data files to help with item recognition, stat parsing, and price searching. These files are located in the `data/` directory and contain information about item names, stats, and other game-related data.

## Data Files

### info.txt
This file contains information used by the API for price searching. It includes details about the API endpoints, authentication, and other API-related information.

### itemsName.txt
This file contains a list of item names recognized by the application. The OCR results are matched against this list to identify items correctly, even when there are slight discrepancies in the text recognition.

**Format:**
Each line contains a single item name.

**Example:**
```
Steel Sword
Iron Helmet
Leather Boots
Magic Staff
```

### pendantAndRingName.txt
This file contains a list of pendant and ring names, which are special types of items in the game with unique naming conventions.

**Format:**
Each line contains a single pendant or ring name.

**Example:**
```
Ring of Protection
Amulet of Strength
Pendant of Wisdom
Ring of Fire Resistance
```

### randomStat
This file contains information about random stats that can appear on items. It helps the application recognize and parse different stat types.

**Format:**
Each line contains a stat name or pattern.

**Example:**
```
Strength +
Dexterity +
Intelligence +
Damage +
Critical Hit Chance +
```

### specialItemName.txt
This file contains names of special items that have unique properties or naming conventions.

**Format:**
Each line contains a single special item name.

**Example:**
```
Legendary Sword of the Dragon
Ancient Shield of Protection
Mystic Staff of Power
Enchanted Bow of Accuracy
```

## Usage
These data files are loaded by the application at startup and used for various purposes:

1. The `ImageProcessor` class uses these files to match OCR results with known item names and stats
2. The `PriceSearcher` class uses the information to format API requests correctly
3. The application uses these files to validate and correct user input

## Modifying Data Files
You can modify these files to add new items, stats, or update existing ones. Follow these guidelines:

1. Maintain the same format as the existing entries
2. Ensure each entry is on a separate line
3. Be consistent with naming conventions
4. Restart the application after making changes to the data files

## Notes
- The application uses fuzzy matching to compare OCR results with the data files, so minor variations in spelling or formatting are tolerated
- If you encounter items that are not being recognized correctly, consider adding them to the appropriate data file
- The data files are case-sensitive, so ensure that the case matches what appears in the game