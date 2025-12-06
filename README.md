# PaletteLoader
### Batch import custom colors into Fusion from a CSV file.

**Introduction: The "Why" and "What"**
Creating custom appearances in Fusion one by one is a slow process—especially if you have a specific palette of manufacturer colors or filaments you want to visualize. **PaletteLoader** is a simple utility designed to automate this workflow. It reads a CSV list of color data (Hex or RGB), duplicates a base material, and creates a new named appearance for every row in your spreadsheet. As a bonus, if you have a 3D body in your design, it creates a "visual preview" loop, applying each color for half a second so you can see them in action.

* **Bulk Import:** Create dozens of materials in seconds using a simple CSV file.
* **Hex Code Support:** No need to manually calculate RGB values; just paste your Hex codes.
* **Visual Preview:** Automatically cycles through the imported colors on your active design body for a quick visual check.

### Installation

**Windows Users**
* **Download:** Download the latest installer (`PaletteLoader_Win.exe`) from the Releases section on the right.
* **Install:** Double-click the installer to run it.
* **Note:** If Windows protects your PC saying "Unknown Publisher," click **More Info → Run Anyway**.
* **Restart:** If Fusion is open, restart it to load the new script.

**Mac Users**
* **Download:** Download the latest package (`PaletteLoader_Mac.pkg`) from the Releases section on the right.
* **Install:** Double-click the package to run the installer.
* **Note:** If macOS prevents the install, **Right-Click** the file and choose **Open**, then click **Open** again in the dialog box.
* **Restart:** If Fusion is open, restart it to load the new script.

### Verify Installation
Once installed, PaletteLoader should be available in your Fusion Scripts library.

1. Open Fusion.
2. Press **Shift+S** to open the **Scripts and Add-Ins** dialog.
3. Click the **Scripts** tab (Note: This is a Script, not an Add-In).
4. Find "**PaletteLoader**" in the list.
5. Click **Run**.

### Using PaletteLoader

**Resources & Templates**
To make things easier, I have included a `resources` folder in this repository containing a master spreadsheet and ready-to-use samples.

* **Master Spreadsheet:** `Palette_Loader_Script_Companion.xlsx`. This Excel file contains a **Template** tab you can duplicate to build your own lists, as well as instructions on how to export them to CSV.
* **Bambu Lab Samples:** I've done the work for you if you use Bambu Lab filaments! The folder includes ready-to-import CSV files for:
    * Bambu Lab Basic PLA
    * Bambu Lab Matte PLA
    * Bambu Lab Silk PLA
    * Bambu Lab HF PETG
    * Bambu Lab Translucent PETG

**Importing Your Colors**
1. **Prepare your CSV:** Use the provided Excel template or create a file with the following columns:
    * **Short Format (Recommended):** `BaseMaterialName, NewColorName, HexCode`
    * **Full Format:** `BaseMaterialName, NewColorName, Hex, R, G, B, Opacity(0-255)`
2. **Run the Script:** Press **Shift+S**, select **PaletteLoader**, and click **Run**.
3. **Select File:** A system file dialog will appear. Select one of the sample CSVs (like `BL-BasicPLA.csv`) or your own custom file.

**The Script Logic:**
* **File Selection:** The standard OS file window asks you to pick your `.csv`.
* **Processing:** The script reads the file row by row. It looks for the "BaseMaterialName" in your Fusion Appearance Library to use as a template (e.g., "Plastic - Matte (Yellow)").
* **Creation:** It duplicates that material, renames it to your "NewColorName," and applies the Hex/RGB values.
* **Preview Mode:** If you have a body in your active component, the script will apply the new color to that body and pause for 0.5 seconds—giving you a slideshow of your new palette!

### Tech Stack
For the fellow coders and makers out there, here is how PaletteLoader was built:

* **Language:** Python (Fusion API)
* **Interface:** Native OS File Dialog (Script-based interaction)
* **Data:** Standard Python `csv` library for parsing
* **Math:** Custom Hex-to-RGB conversion logic

### Acknowledgements & Credits
* **Developer:** Ed Johnson (Making With An EdJ)
* **AI Assistance:** Developed with coding assistance from Google's Gemini.

**Lucy (The Cavachon Puppy): Chief Wellness Officer & Director of Mandatory Breaks**
Thank you for ensuring I maintained healthy circulation by interrupting my deep coding sessions with urgent requests for play.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

Happy Making!
— EdJ
