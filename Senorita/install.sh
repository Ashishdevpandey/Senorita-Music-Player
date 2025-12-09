#!/bin/bash

APP_NAME="Señorita"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$PROJECT_DIR/ytmplayer"
VENV_DIR="$PROJECT_DIR/venv"
ICON_PATH="$SRC_DIR/ui/icons/senorita.png"
DESKTOP_FILE="senorita.desktop"

echo "========================================"
echo "   Installing $APP_NAME"
echo "========================================"

# 1. Check for System Dependencies (mpv)
echo "[1/5] Checking for system dependencies..."
if ! command -v mpv &> /dev/null; then
    echo "mpv could not be found. Attempting to install..."
    if [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm mpv
    elif [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y mpv libmpv-dev python3-venv python3-pip
    elif [ -f /etc/fedora-release ]; then
        sudo dnf install -y mpv mpv-libs-devel python3-pip
    else
        echo "WARNING: Could not detect package manager. Please ensure 'mpv' is installed manually."
    fi
else
    echo "mpv is installed."
fi

# 2. Setup Virtual Environment
echo "[2/5] Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# 3. Install Python Dependencies
echo "[3/5] Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$SRC_DIR/requirements.txt"

# 4. Create Desktop Entry
echo "[4/5] Creating desktop entry..."
cat > "$PROJECT_DIR/$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=$APP_NAME
Comment=YouTube Music Player
Exec=$VENV_DIR/bin/python $SRC_DIR/main.py
Icon=$ICON_PATH
Type=Application
Categories=AudioVideo;Player;
Terminal=false
StartupWMClass=Señorita
EOF

# 5. Install Desktop Entry
echo "[5/5] Installing to application menu..."
mkdir -p ~/.local/share/applications
cp "$PROJECT_DIR/$DESKTOP_FILE" ~/.local/share/applications/
# Update database to ensure icon shows up immediately (optional but good)
update-desktop-database ~/.local/share/applications &> /dev/null

echo "========================================"
echo "   Installation Complete!"
echo "========================================"
echo "You can now launch '$APP_NAME' from your application menu."
echo "Or run it directly with: $VENV_DIR/bin/python $SRC_DIR/main.py"
