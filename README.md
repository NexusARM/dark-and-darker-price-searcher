# 📖 **Installation and Usage Guide**

## 🛠 **Installation**

To use this program, follow these simple steps:

1. **Install Tesseract:**

   - You can download Tesseract OCR from the following link: [Tesseract OCR - UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

2. **Install Python AND HIS dependencies:**
   - Download and install python (skip if you have it installed)
   - After downloading the repository, run the command:
     ```bash
     pip install -r requirements.txt
     ```

---

## 🖍 **Program Description**

This program helps you quickly look up item prices on [DND Prices](https://www.dndprices.com/) during gameplay. **Two main components** handle the task efficiently:

### 1️⃣ **ImageProcessor**

This component extracts text from the game screen:

- Takes a screenshot of the item description.
- Identifies and crops the text box around the description.
- Filters and processes the text for accurate recognition using OCR.

> **Important:** Ensure the item description is fully visible in the game for the best results.

### 2️⃣ **ApiUser**

This component uses the data from the **ImageProcessor** to:

- Make an API call to the DND Prices service.
- Retrieve item prices programmatically, eliminating the need for manual searches.

### 3️⃣ **Main Program**

The `main.py` script combines both components, streamlining the entire process for you.

---

## 🚀 **How to Use the Program**

1. **Prepare Your Setup:**

   - Open the file `launcher.bat` and update the two numbers in the file to match your screen resolution.

2. **Run the Program:**

   - Launch the `launcher.bat` file and wait for a terminal to open.
   - In the game, hover over the item and press **Shift + P** to search for the price.
   - The terminal will display the item's price. When two numbers appear, prioritize the second one, as it represents the final calculated price from the API.

---

## 💡 **Suggestions and Future Improvements**

- **User Interface:** Add a graphical interface to make the program easier to configure and use.

---

## 📨 **Contact**

For questions, issues, or suggestions, feel free to reach out!

---

**Thank you for using the program!** 🚀

If you wish to contribute to the development, you can open an issue on GitHub or contact me directly on Discord.

👤 **Username:** nexusarm

#
