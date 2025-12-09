# Señorita 🎵

**Señorita** is a beautiful, modern desktop music player built with Python and PySide6. It streams music directly from YouTube Music, offering a premium ad-free listening experience with a sleek user interface.

## ✨ Features

*   **YouTube Music Streaming**: Search and play any song from YouTube Music.
*   **Modern UI**: A clean, responsive interface with a dark theme.
*   **History & Recommendations**: Keeps track of your listening history and provides recommendations.
*   **MPV Backend**: High-quality audio playback using the powerful `mpv` player.
*   **Android Support**: Can be packaged as an APK for Android devices.

## 🚀 Installation

### Prerequisites

*   **Python 3.8+**
*   **mpv**: The system media player is required for the backend.

### Linux (Arch/Debian/Fedora)

We provide an automated installation script that sets up the virtual environment, installs dependencies, and creates a desktop entry.

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/Ashishdevpandey/Senorita-Music-Player.git
    cd Senorita-Music-Player
    ```

2.  **Run the installer**:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3.  **Launch**: Open "Señorita" from your application menu.

### Manual Installation

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    python main.py
    ```

## 📱 Android Build

Señorita can be compiled into an Android APK using **Buildozer**.

👉 **[Read the Android Build Instructions](README_ANDROID.md)** for a step-by-step guide.

## 🛠️ Built With

*   [PySide6](https://doc.qt.io/qtforpython/) - The GUI framework.
*   [python-mpv](https://github.com/jaseg/python-mpv) - Python interface for mpv.
*   [ytmusicapi](https://github.com/sigma67/ytmusicapi) - Unofficial YouTube Music API.
*   [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Media downloader.

## 📄 License

This project is open source.
