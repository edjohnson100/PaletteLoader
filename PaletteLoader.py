# ---------------------------------------------------------------------
# PaletteLoader
# ---------------------------------------------------------------------
# Author-Ed Johnson
# Description-Script to use a CSV file input to create
#             and add custom color appearances to the CURRENT DESIGN.
#             If a body is found, it applies each color with a
#             quick, 1/2-second pause for visual preview.
# Date - 2024-10-15
# Last Update - 2025-11-27
# ---------------------------------------------------------------------
# API LIMITATION NOTE:
# Fusion 360's API does not currently support writing appearances 
# directly to material libraries. This script adds colors to the 
# active design document, where they can be manually managed.
# ---------------------------------------------------------------------
# CSV File Details:
# ---------------------------------------------------------------------
# First line contains header information:
# Format 1 (Full):
#   CopyColor - Color name of existing Fusion appearance - used as a base for creating the new color
#   NewColorName - The name for your new custom color
#   Hex - Hex value of the new color (for reference only)
#   R - Red value of the RGBA color for the new color
#   G - Green value of the RGBA color for the new color
#   B - Blue value of the RGBA color for the new color
#   A - Opacity value of the RGBA color for the new color (0 (fully opaque) - 255=(fully transparent)
#
# Format 2 (Short):
#   CopyColor
#   NewColorName
#   Hex (e.g., #FF0000 or FF0000). R,G,B will be calculated. Opacity defaults to 0.
# ---------------------------------------------------------------------
# This version does NOT require a body.
# If a body exists, it will be used for a color preview.
# 
# ---------------------------------------------------------------------

import adsk.core, adsk.fusion, traceback, os, csv, math, time

handlers = []

folder = ''

def run(context):
    ui = None

    try: 
        lastUpdate = 'Last Update: 2025-11-27'
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        
        rootComp = design.rootComponent
        activeComp = design.activeComponent
        apps=design.appearances

        # --- Check for a body, but don't require it ---
        body = None
        originalAppearance = None # Variable to store the starting color
        try:
            body = activeComp.bRepBodies.item(0)
            if body:
                originalAppearance = body.appearance
                debugPrint('Body found. Will apply colors with 0.5-second pause.')
        except:
            debugPrint('No body found in active component. Will only load appearances.')
            pass # body remains None
        # --- End New Section ---

        # ---------------------------------------------------------------------
        # Open the CSV file and get busy
        # ---------------------------------------------------------------------
        # Use the OS file selector to get the input file
        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.title = "Select the CSV file to import"
        fileDialog.filter = 'CSV files (*.csv)'
        fileDialog.filterIndex = 0
        dialogResult = fileDialog.showOpen()
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
        else:
            return
        
        # get the total number of rows in file
        csvFile = open(filename, 'r')
        allRows = csvFile.readlines()
        totalRows = (len(allRows)-1)
        csvFile.close()

        csvFile = open(filename, 'r')
        textLines = csv.reader(csvFile)
        header = next(textLines)

        # time how long this takes
        startTime = time.time()

        lineNum = 0

        debugPrint('CSV file imported...\n--------------------')
        for textLine in textLines:
            lineNum += 1
            listString = ''
            indexNum = 0

            # --- Flexible CSV Parsing ---
            try:
                # Check number of columns to decide parsing logic
                if len(textLine) >= 7:
                    # Full format: CopyColor, NewColorName, Hex, R, G, B, A
                    copyColor = textLine[0]
                    newColorName = textLine[1]
                    hex_val = textLine[2] # hex is just for reference here
                    rgbR = int(textLine[3])
                    rgbG = int(textLine[4])
                    rgbB = int(textLine[5])
                    rgbA = int(textLine[6])
                    
                elif len(textLine) >= 3:
                    # Short format: CopyColor, NewColorName, Hex
                    copyColor = textLine[0]
                    newColorName = textLine[1]
                    hex_val = textLine[2]
                    
                    # Calculate RGB from hex
                    rgb_tuple = hex_to_rgb(hex_val)
                    if rgb_tuple is None:
                        debugPrint(f"Skipping line {lineNum}: Invalid Hex code '{hex_val}'.")
                        continue
                    
                    rgbR, rgbG, rgbB = rgb_tuple
                    rgbA = 0 # Default to fully opaque
                
                else:
                    # Not enough data
                    debugPrint(f"Skipping line {lineNum}: Incomplete row data.")
                    continue

            except Exception as e:
                debugPrint(f"Error parsing line {lineNum}: {e}")
                continue
            # --- End Parsing Section ---


            # Get an existing appearance that we know exists to base our new colors on.
            fusionMaterials = app.materialLibraries.itemByName('Fusion Appearance Library')
            
            # Find the base color
            try:
                baseColor = fusionMaterials.appearances.itemByName(copyColor)
            except:
                debugPrint(f"Could not find base color '{copyColor}'. Skipping '{newColorName}'.")
                continue # Skip this color if base color isn't found

            # Copy it to the design, giving it a new name.
            try:
                newColor = design.appearances.addByCopy(baseColor, newColorName)
            except:
                # This catches if the color already exists in the *design*
                try:
                    newColor = design.appearances.itemByName(newColorName)
                    if not newColor:
                        debugPrint(f"Could not add or find color: {newColorName}")
                        continue # Skip if we can't add or find it
                except:
                    debugPrint(f"Skipping color {newColorName} due to error.")
                    continue # Skip on any other error
                    
            # Point to the color properties of the new color
            colorProp = adsk.core.ColorProperty.cast(newColor.appearanceProperties.itemByName('Color'))
            # Apply the new RGBA value (which was set by either format)
            colorProp.value = adsk.core.Color.create(rgbR,rgbG,rgbB, rgbA)
            
            # --- Add to Favorites ---
            try:
                newColor.isFavorite = True
                # debugPrint(f"Added {newColorName} to Favorites.")
            except Exception as e:
                debugPrint(f"Failed to add {newColorName} to Favorites: {e}")

            # --- Apply to body and pause, if body exists ---
            if body:
                try:
                    body.appearance = newColor
                    # Force viewport to update to show the new color
                    app.activeViewport.refresh()
                    # Pause for a 1/2 second
                    time.sleep(.5)
                except Exception as e:
                    debugPrint(f'Failed to apply {newColorName} to body: {str(e)}')
            # --- End New Section ---

            debugPrint(f"Processed: {newColorName} (R:{rgbR}, G:{rgbG}, B:{rgbB}, A:{rgbA})")
            # -------------------------------------------------------------------------
            # Create the color from the imported data
            # -------------------------------------------------------------------------
            
            
        csvFile.close()

        # --- Restore original appearance if body was used ---
        if body and originalAppearance:
            try:
                body.appearance = originalAppearance
                app.activeViewport.refresh()
                debugPrint('Restored original body appearance.')
            except Exception as e:
                debugPrint(f'Failed to restore original appearance: {e}')
        # ----------------------------------------------------

        stopTime = time.time()
        elapsedTime = displayElapsedTime(startTime, stopTime)


    except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# -------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Convert Hex string to (R, G, B) tuple
# -------------------------------------------------------------------------
def hex_to_rgb(hex_color):
    """Converts a hex color string (with or without #) to (R, G, B) tuple."""
    hex_val = hex_color.lstrip('#').strip() # Remove '#' and any whitespace
    if len(hex_val) != 6:
        return None  # Invalid hex code length
    try:
        # Convert hex string pairs to integers
        r = int(hex_val[0:2], 16)
        g = int(hex_val[2:4], 16)
        b = int(hex_val[4:6], 16)
        return r, g, b
    except ValueError:
        # Handle cases like 'GG' or other non-hex characters
        return None
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Print a message in the Text Commands window
# -------------------------------------------------------------------------
# Get the palette that represents the TEXT COMMANDS window.
def debugPrint(message):
    # Display a debug message in the Fusion 360 Text Commands window
    # Get the palette that represents the TEXT COMMANDS window
    app = adsk.core.Application.get()
    ui = app.userInterface
    textPalette = ui.palettes.itemById('TextCommands')

    # Make sure the palette is visible.
    if not textPalette.isVisible:
        textPalette.isVisible = True

    # Write some text
    textPalette.writeText(message)

# -------------------------------------------------------------------------
# Display elapsed time 
# Usage:
# set start time in code
# set stop time variable in code
# call this function after setting stop time to display message
#
#    startTime = time.time()
#    ...
#    ... # do some stuff
#    ...
#    stopTime = time.time()
#    message = 'Elapsed time: '
#    displayElapsedTime(startTime, stopTime, [message = 'Elapsed time: '], [displayMsxbox = False])
#
# message box displayed with message text 
# -------------------------------------------------------------------------
def displayElapsedTime(startTime, stopTime, message = 'Elapsed time: ', displayMsgbox = False):
    # Display a messagebox with minutes, seconds elapsed
    ui = None
    app = adsk.core.Application.get()
    ui = app.userInterface

    totalSeconds = stopTime - startTime
    totalMinutes = int(totalSeconds / 60)
    totalTime = '{:0.2f}'.format(stopTime - startTime)
    minutesSeconds = '\n\n' + str(totalMinutes) + ' minutes, ' + '{:0.2f}'.format((stopTime - startTime - totalMinutes * 60)) + ' seconds.'
    if displayMsgbox:
        ui.messageBox(message + minutesSeconds, 'Mission Complete!')

    textPalette = ui.palettes.itemById('TextCommands')

    # Make sure the palette is visible.
    if not textPalette.isVisible:
        textPalette.isVisible = True

    # Write some text
    returnValue = message + minutesSeconds.replace('\n\n','')
    textPalette.writeText(returnValue)
    return returnValue

# ---------------------------------------------------------------------
# End of Functions
# ---------------------------------------------------------------------