# 📖 **Installation and Usage Guide**

## 🛠 **Installation**

To use this program, follow these simple steps:

1. **Install Tesseract:**

   - You can download Tesseract OCR from the following link: [Tesseract OCR - UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

2. **Install Python dependencies:**

   - After downloading the repository, run the command:
     ```bash
     pip install -r requirements.txt
     ```

---

## 📝 **Program Description**

This program is designed to facilitate the price lookup of an item on [DND Prices](https://www.dndprices.com/) during a game. **Two screens are required** for optimal use: one dedicated to the game and the other to the browser.

The program is divided into two main components:

### 1️⃣ **ImageProcessor**

This part is a Python class that:

- **Extracts text from the item description** visible on the game screen.
- **How it works:**
  1. Takes a screenshot.
  2. Identifies the borders of the box containing the item description.
  3. Crops the box to isolate only the item's text.
  4. Filters colors, keeping only those relevant (item name and random modifiers).
  5. Processes the remaining text for accurate reading using OCR.

> **Note:** For correct operation, the item description must be fully visible on the game screen when this class is executed.

### 2️⃣ **Dirty Clicker**

This second part of the program performs predefined clicks on the second screen. It is useful for automatically navigating the site and searching for the item.

- **How it works:**
  - Executes clicks on specific coordinates of the second screen.
  - Currently, the coordinates must be manually configured based on your computer setup.
  - The resolution is currently set to **2K**; if you use a different resolution, you will need to modify the code to adjust it.

> **Note:** This component is still "rough" and could be improved to adapt automatically to different configurations.

---

## 🚀 **How to Use the Program**

1. Set up your environment:

   - Ensure that the second screen is positioned and configured correctly.
   - Modify the coordinates in Dirty Clicker to suit your setup.

2. Run the program:

   - Execute the Python code and ensure the item description is visible when **ImageProcessor** is executed.

3. Let the program do the rest! 😊

---

## 💡 **Suggestions and Future Improvements**

- **Coordinate automation:** Implement a more dynamic system to automatically detect click coordinates.
- **Support for other resolutions:** Adapt the program to work without manual adjustments for different screen resolutions.
- **User interface:** Add a graphical interface to simplify configuration and program usage.

---

## 📬 **Contact**

For questions, issues, or suggestions, feel free to reach out!

---

**Thank you for using the program!** 🚀

If you wish to contribute to the development, you can open an issue on GitHub or contact me directly on Discord.

👤 **Username:** nexusarm



# 🔮 **Future Possibilities with DND Prices API**

If, in the future, it becomes possible to obtain access to the APIs of [DND Prices](https://www.dndprices.com/), the program could be significantly enhanced. Specifically:

1. **Elimination of the Second Screen Requirement:**

   - With direct access to the DND Prices API, it would no longer be necessary to use a second screen for price lookups. The program could retrieve item prices programmatically, reducing complexity and improving usability.

2. **In-Game Overlay Integration:**

   - The program could evolve into an overlay system directly displayed on the game screen. This would allow users to see item prices in real-time without interrupting their gameplay experience.

3. **Enhanced Speed and Accuracy:**

   - By using APIs, data retrieval would be faster and more accurate, avoiding potential issues with OCR errors or misclicks.


These improvements would make the tool more user-friendly and efficient, opening up new opportunities for advanced features and seamless integration.


---

For now, the current program setup serves as a workaround until such API access becomes available.
