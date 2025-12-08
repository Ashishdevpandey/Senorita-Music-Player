import mpv
import os
import locale

class MPVPlayer:
    def __init__(self, input_ipc_server=None):
        # Initialize MPV
        # We use ytdl hook to play youtube URLs directly
        # Fix for MPV/Qt locale conflict
        locale.setlocale(locale.LC_NUMERIC, 'C')
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)
        
        # Set default options
        self.player['vo'] = 'null'  # Audio only, no video output window
        self.player['keep-open'] = 'yes'
        self.player['ytdl-format'] = 'bestaudio/best'
        self.player['msg-level'] = 'all=v' # Enable verbose logging for debugging
        
        # Explicitly set yt-dlp path from venv
        venv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Assuming standard venv structure: venv/bin/yt-dlp
        # We need to find where the venv is relative to this file or use a fixed path if known
        # Better: use the one in the same bin dir as the python executable if running from venv
        # Or hardcode for this user environment as we know it:
        ytdl_path = "/home/ashish/Desktop/Senorita/venv/bin/yt-dlp"
        if os.path.exists(ytdl_path):
             self.player['script-opts'] = f'ytdl_hook-ytdl_path={ytdl_path}'
        else:
             print(f"WARNING: yt-dlp not found at {ytdl_path}")
        
        # Callbacks
        self.on_position_change = None
        self.on_duration_change = None
        self.on_state_change = None # playing/paused/idle
        self.on_metadata_change = None # title/artist updates if available from stream

        # Observe properties
        self.player.observe_property('time-pos', self._position_handler)
        self.player.observe_property('duration', self._duration_handler)
        self.player.observe_property('core-idle', self._idle_handler)
        self.player.observe_property('pause', self._pause_handler)

    def _position_handler(self, name, value):
        if self.on_position_change and value is not None:
            self.on_position_change(value)

    def _duration_handler(self, name, value):
        if self.on_duration_change and value is not None:
            self.on_duration_change(value)

    def _idle_handler(self, name, value):
        # value is True if idle
        pass

    def _pause_handler(self, name, value):
        if self.on_state_change:
            self.on_state_change('paused' if value else 'playing')

    def play(self, url):
        print(f"DEBUG: Attempting to play URL: {url}")
        try:
            self.player.play(url)
            print("DEBUG: MPV play command sent.")
        except Exception as e:
            print(f"DEBUG: Error sending play command: {e}")

        if self.on_state_change:
            self.on_state_change('playing')

    def pause(self):
        self.player.pause = not self.player.pause

    def stop(self):
        self.player.stop()
        if self.on_state_change:
            self.on_state_change('stopped')

    def seek(self, position):
        """Seek to position in seconds"""
        try:
            self.player.seek(position, reference="absolute")
        except Exception as e:
            print(f"Error seeking: {e}")

    def set_volume(self, level):
        """Set volume 0-100"""
        self.player.volume = level

    def get_volume(self):
        return self.player.volume

    def is_playing(self):
        try:
            return not self.player.pause and not self.player.core_idle
        except:
            return False

    def resume(self):
        self.player.pause = False

    def get_time_pos(self):
        try:
            return self.player.time_pos or 0
        except:
            return 0

    def get_duration(self):
        try:
            return self.player.duration or 0
        except:
            return 0

    def set_args(self, args_str):
        """
        Set additional MPV arguments.
        Note: Many arguments must be set at initialization.
        This is a placeholder for runtime properties if needed.
        """
        pass
