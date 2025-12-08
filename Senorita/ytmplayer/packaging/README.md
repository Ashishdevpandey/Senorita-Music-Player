# Packaging Instructions

## 1. PyInstaller Build

To create a standalone executable using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build command from the project root (`ytmplayer/`):
   ```bash
   pyinstaller --name=senorita \
               --windowed \
               --onefile \
               --add-data "ui/main_window.ui:ui" \
               --hidden-import="PySide6" \
               --hidden-import="ytmusicapi" \
               --hidden-import="mpv" \
               main.py
   ```

   The executable will be in the `dist/` folder.

## 2. AppImage Creation

To create an AppImage:

1. Download `appimagetool` from GitHub.
2. Create an AppDir structure:
   ```bash
   mkdir -p AppDir/usr/bin
   mkdir -p AppDir/usr/share/applications
   mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps
   ```

3. Copy the PyInstaller executable to `AppDir/usr/bin/senorita`.

4. Copy `ytmplayer.desktop` to `AppDir/usr/share/applications/`.
   Update the `Exec` line in `ytmplayer.desktop` to:
   ```ini
   Exec=senorita
   ```

5. Add an icon (e.g., `icon.png`) to `AppDir/usr/share/icons/hicolor/256x256/apps/senorita.png` and `AppDir/`.

6. Create `AppRun` script in `AppDir/`:
   ```bash
   #!/bin/bash
   exec "$APPDIR/usr/bin/senorita" "$@"
   ```
   Make it executable: `chmod +x AppDir/AppRun`

7. Run `appimagetool`:
   ```bash
   ./appimagetool-x86_64.AppImage AppDir/
   ```

## 3. Arch Linux Package (PKGBUILD)

1. Create a `PKGBUILD` file:

   ```bash
   # Maintainer: Your Name <email@example.com>
   pkgname=senorita
   pkgver=1.0
   pkgrel=1
   pkgdesc="Senorita Music Player"
   arch=('x86_64')
   url="https://github.com/yourusername/senorita"
   license=('MIT')
   depends=('python' 'python-pyside6' 'python-requests' 'python-pillow' 'mpv')
   makedepends=('python-setuptools')
   source=("senorita-$pkgver.tar.gz") # Assuming you have a source tarball
   # For local development, you can just copy files
   
   package() {
       cd "$srcdir/$pkgname-$pkgver"
       
       # Install python files
       install -Dm644 main.py "$pkgdir/usr/lib/senorita/main.py"
       cp -r player ui utils "$pkgdir/usr/lib/senorita/"
       
       # Install desktop entry
       install -Dm644 ytmplayer.desktop "$pkgdir/usr/share/applications/senorita.desktop"
       
       # Create launcher script
       mkdir -p "$pkgdir/usr/bin"
       echo "#!/bin/bash" > "$pkgdir/usr/bin/senorita"
       echo "cd /usr/lib/senorita && python main.py \"\$@\"" >> "$pkgdir/usr/bin/senorita"
       chmod +x "$pkgdir/usr/bin/senorita"
   }
   ```

2. Build and install:
   ```bash
   makepkg -si
   ```

   *Note: You might need to adjust dependencies if you are using a virtual environment or pip packages. The above assumes system packages.*

## 4. Debian Package (.deb)

1. Create directory structure:
   ```bash
   mkdir -p senorita_1.0-1/usr/local/bin
   mkdir -p senorita_1.0-1/DEBIAN
   ```

2. Create `DEBIAN/control` file:
   ```
   Package: senorita
   Version: 1.0-1
   Section: sound
   Priority: optional
   Architecture: amd64
   Maintainer: Your Name <email@example.com>
   Description: Senorita Music Player
    A simple desktop player for YouTube Music.
   ```

3. Copy the executable to `usr/local/bin/senorita`.

4. Build the package:
   ```bash
   dpkg-deb --build senorita_1.0-1
   ```
