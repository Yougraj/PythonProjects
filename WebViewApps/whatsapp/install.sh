#!/bin/bash

# Variables
APP_NAME="WhatsApp"
ICON_NAME="WhatsApp.png"
SCRIPT_NAME="WhatsApp.py"
SYSTEM_PATH="/usr/local/bin/WhatsApp-web"
ICON_PATH="/usr/share/icons/$ICON_NAME"
DESKTOP_ENTRY_PATH="/usr/share/applications/whatsapp_app.desktop"

# Check if the required files exist
if [[ ! -f $SCRIPT_NAME || ! -f $ICON_NAME ]]; then
    echo "Error: Required files ($SCRIPT_NAME or $ICON_NAME) not found in the current directory."
    exit 1
fi

# Step 1: Check if existing files are present and remove them
if [[ -f $SYSTEM_PATH ]]; then
    echo "Removing existing executable at $SYSTEM_PATH..."
    sudo rm "$SYSTEM_PATH"
fi

if [[ -f $ICON_PATH ]]; then
    echo "Removing existing icon at $ICON_PATH..."
    sudo rm "$ICON_PATH"
fi

if [[ -f $DESKTOP_ENTRY_PATH ]]; then
    echo "Removing existing .desktop entry at $DESKTOP_ENTRY_PATH..."
    sudo rm "$DESKTOP_ENTRY_PATH"
fi

# Step 2: Package the app with PyInstaller
echo "Packaging the app using PyInstaller..."
pyinstaller --onefile --windowed --icon="$ICON_NAME" "$SCRIPT_NAME"
if [[ $? -ne 0 ]]; then
    echo "Error: PyInstaller packaging failed."
    exit 1
fi

# Step 3: Move the executable to the system path
echo "Moving the executable to $SYSTEM_PATH..."
sudo mv "dist/$APP_NAME" "$SYSTEM_PATH"
if [[ $? -ne 0 ]]; then
    echo "Error: Moving executable failed."
    exit 1
fi

# Step 4: Move the icon to a secure location
echo "Moving the icon to $ICON_PATH..."
sudo cp "$ICON_NAME" "$ICON_PATH"
if [[ $? -ne 0 ]]; then
    echo "Error: Moving icon failed."
    exit 1
fi

# Step 5: Create the .desktop file
echo "Creating .desktop entry at $DESKTOP_ENTRY_PATH..."
echo "[Desktop Entry]
Version=1.0
Name=WhatsApp Web
Comment=Desktop app for WhatsApp Web
Exec=$SYSTEM_PATH
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Network;Chat;" | sudo tee "$DESKTOP_ENTRY_PATH" > /dev/null

if [[ $? -ne 0 ]]; then
    echo "Error: Creating .desktop file failed."
    exit 1
fi

# Step 6: Clean up PyInstaller build directories
echo "Cleaning up temporary files..."
rm -rf build dist __pycache__ "$APP_NAME.spec"

echo "Installation complete! You can find WhatsApp Web in your application menu."


