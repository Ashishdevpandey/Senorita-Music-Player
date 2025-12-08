import sys
import os
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem, QPushButton, QInputDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QImage

from player.mpv_player import MPVPlayer
from player.ytm import YTMusicClient
from utils.theme import SENORITA_THEME
from utils.history import HistoryManager
# from utils.playlists import PlaylistManager # Removed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.load_ui()
        self.setWindowTitle("Señorita")
        
        # Initialize players
        self.player = MPVPlayer()
        self.ytm_client = YTMusicClient()
        self.history_manager = HistoryManager()
        # self.playlist_manager = PlaylistManager() # Removed
        
        # Setup UI connections
        self.setup_connections()
        
        # Apply Theme
        self.apply_theme()
        
        # Load Sidebar Image
        self.load_sidebar_image()
        
        # Populate Home Page
        self.populate_home_page()
        
        # Populate Playlists
        # self.populate_playlists() # Removed
        
        # Timer for updating UI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_playback_progress)
        self.timer.start(1000)
        
        self.current_track = None
        self.is_seeking = False

    def load_ui(self):
        loader = QUiLoader()
        ui_file = os.path.join(os.path.dirname(__file__), "ui/main_window.ui")
        self.ui = loader.load(ui_file)
        self.setCentralWidget(self.ui)
        self.setMinimumSize(900, 600)
        
        # Find widgets
        self.list_widget_results = self.ui.findChild(QWidget, "listWidget_results")
        self.input_search = self.ui.findChild(QWidget, "lineEdit_search")
        self.btn_play_pause = self.ui.findChild(QWidget, "btn_play_pause")
        self.slider_seek = self.ui.findChild(QWidget, "slider_seek")
        self.label_time_start = self.ui.findChild(QWidget, "label_time_start")
        self.label_time_end = self.ui.findChild(QWidget, "label_time_end")
        self.slider_volume = self.ui.findChild(QWidget, "verticalSlider_volume")
        self.label_title = self.ui.findChild(QWidget, "label_title")
        self.label_artist = self.ui.findChild(QWidget, "label_artist")
        self.label_album_art = self.ui.findChild(QWidget, "label_album_art")
        self.label_sidebar_image = self.ui.findChild(QWidget, "label_sidebar_image")
        
        # Home Page Widgets
        self.list_recent = self.ui.findChild(QWidget, "list_recent")
        self.list_recommend = self.ui.findChild(QWidget, "list_recommend")
        
        # Playlist Widgets
        # self.list_playlists = self.ui.findChild(QWidget, "list_playlists") # Removed
        # self.btn_create_playlist = self.ui.findChild(QWidget, "btn_create_playlist") # Removed
        
        # Navigation buttons
        self.btn_home = self.ui.findChild(QWidget, "btn_home")
        self.btn_search = self.ui.findChild(QWidget, "btn_search")
        # self.btn_library = self.ui.findChild(QWidget, "btn_library") # Removed
        # self.btn_settings = self.ui.findChild(QWidget, "btn_settings") # Removed
        
        # Stacked Widget
        self.stacked_widget = self.ui.findChild(QWidget, "stackedWidget")

    def setup_connections(self):
        self.input_search.returnPressed.connect(self.search_music)
        # Switch to single click for better UX
        self.list_widget_results.itemClicked.connect(self.play_selected_track)
        
        # Home Page Connections
        if self.list_recent:
            self.list_recent.itemClicked.connect(self.play_selected_track)
        if self.list_recommend:
            self.list_recommend.itemClicked.connect(self.play_selected_track)
            
        # Playlist Connections
        # if self.btn_create_playlist:
        #     self.btn_create_playlist.clicked.connect(self.create_new_playlist)
            
        self.btn_play_pause.clicked.connect(self.toggle_play_pause)
        
        # Connect new controls (placeholders for now)
        self.btn_shuffle = self.findChild(QPushButton, "btn_shuffle")
        self.btn_repeat = self.findChild(QPushButton, "btn_repeat")
        if self.btn_shuffle: self.btn_shuffle.clicked.connect(lambda: print("Shuffle clicked"))
        if self.btn_repeat: self.btn_repeat.clicked.connect(lambda: print("Repeat clicked"))
        
        self.slider_seek.sliderPressed.connect(self.on_seek_start)
        self.slider_seek.sliderReleased.connect(self.on_seek_end)
        
        self.slider_volume.valueChanged.connect(self.set_volume)
        
        # Navigation
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_search.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        # self.btn_library.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2)) # Removed
        # self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3)) # Removed

    # def create_new_playlist(self):
    #     name, ok = QInputDialog.getText(self, "Create Playlist", "Enter playlist name:")
    #     if ok and name:
    #         if self.playlist_manager.create_playlist(name):
    #             self.populate_playlists()
    #         else:
    #             QMessageBox.warning(self, "Error", "Playlist already exists!")

    # def populate_playlists(self):
    #     if not self.list_playlists:
    #         return
        
    #     self.list_playlists.clear()
    #     playlists = self.playlist_manager.get_playlists()
    #     for playlist in playlists:
    #         item = QListWidgetItem(playlist)
    #         # item.setIcon(QIcon("path/to/playlist_icon.png")) # Optional
    #         self.list_playlists.addItem(item)

    def populate_home_page(self):
        if not self.list_recent or not self.list_recommend:
            return
            
        self.list_recent.clear()
        self.list_recommend.clear()
        
        # Helper to set icon from URL
        def set_item_icon(item, url):
            if not url:
                return
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    icon = QIcon(pixmap)
                    item.setIcon(icon)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")

        # Recent Tracks
        recent_tracks = self.history_manager.get_recent_tracks(10)
        for track in recent_tracks:
            item = QListWidgetItem(f"{track['title']}\n{track['artist']}")
            item.setData(Qt.UserRole, track)
            self.list_recent.addItem(item)
            # Load icon (blocking for now, ideally threaded)
            set_item_icon(item, track.get('thumbnail'))
            
        # Recommendations (based on last played)
        last_played = self.history_manager.get_last_played()
        if last_played:
            recommendations = self.ytm_client.get_recommendations(last_played['videoId'])
            for track in recommendations:
                item = QListWidgetItem(f"{track['title']} - {track['artist']}")
                item.setData(Qt.UserRole, track)
                self.list_recommend.addItem(item)
                set_item_icon(item, track.get('thumbnail'))
        else:
            # Fallback if no history (e.g. trending or specific artist)
            pass

    def apply_theme(self):
        self.setStyleSheet(SENORITA_THEME)
        self.update_greeting()

    def update_greeting(self):
        import datetime
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
            
        # Find welcome label and update it
        label_welcome = self.ui.findChild(QWidget, "label_welcome")
        if label_welcome:
            label_welcome.setText(greeting)
            # Style is now handled by theme.py or UI file, but we can override if needed
            # label_welcome.setStyleSheet("font-size: 32px; font-weight: bold; color: #121212; margin-bottom: 20px;")

    def load_sidebar_image(self):
        if self.label_sidebar_image:
            image_path = os.path.join(os.path.dirname(__file__), "ui/icons/senorita.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                # Scale to width of sidebar (approx 250px) minus padding
                target_width = 160
                scaled_pixmap = pixmap.scaledToWidth(target_width, Qt.SmoothTransformation)
                self.label_sidebar_image.setPixmap(scaled_pixmap)
                self.label_sidebar_image.setAlignment(Qt.AlignCenter)

    def search_music(self):
        query = self.input_search.text()
        if not query:
            return
            
        results = self.ytm_client.search(query)
        self.list_widget_results.clear()
        
        for result in results:
            item = QListWidgetItem(f"{result['title']} - {result['artist']}")
            item.setData(Qt.UserRole, result)
            self.list_widget_results.addItem(item)
            
        self.stacked_widget.setCurrentIndex(1) # Switch to search page

    def play_selected_track(self, item):
        track_data = item.data(Qt.UserRole)
        if not track_data:
            return
            
        self.current_track = track_data
        
        # Add to history
        self.history_manager.add_track(track_data)
        
        # Refresh Home Page (optional, maybe not every time to avoid lag)
        # self.populate_home_page() 
        
        video_id = track_data['videoId']
        url = self.ytm_client.get_song_url(video_id)
        
        self.player.play(url)
        
        # Update UI
        self.label_title.setText(track_data['title'])
        self.label_artist.setText(track_data['artist'])
        self.btn_play_pause.setText("⏸")
        
        # Load thumbnail
        self.load_thumbnail(track_data['thumbnail'])

    def load_thumbnail(self, url):
        if not url:
            return
        try:
            response = requests.get(url)
            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap(image)
            self.label_album_art.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error loading thumbnail: {e}")

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.btn_play_pause.setText("▶")
        else:
            self.player.resume()
            self.btn_play_pause.setText("⏸")

    def on_seek_start(self):
        self.is_seeking = True

    def on_seek_end(self):
        if self.current_track:
            value = self.slider_seek.value()
            self.player.seek(value)
        else:
            self.slider_seek.setValue(0)
        self.is_seeking = False

    def set_volume(self, value):
        self.player.set_volume(value)

    def update_playback_progress(self):
        if not self.player.is_playing() and not self.is_seeking:
            return
            
        current_time = self.player.get_time_pos()
        duration = self.player.get_duration()
        
        if duration:
            self.slider_seek.setMaximum(int(duration))
            if not self.is_seeking:
                self.slider_seek.setValue(int(current_time))
            
            # Update labels
            self.label_time_start.setText(self.format_time(current_time))
            self.label_time_end.setText(self.format_time(duration))

    def format_time(self, seconds):
        if not seconds:
            return "00:00"
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
