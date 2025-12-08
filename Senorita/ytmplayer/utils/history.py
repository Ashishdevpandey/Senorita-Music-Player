import json
import os

class HistoryManager:
    def __init__(self, history_file="history.json"):
        self.history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), history_file)
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_track(self, track_data):
        # track_data should have 'videoId', 'title', 'artist'
        if not track_data or 'videoId' not in track_data:
            return

        # Remove if exists (to move to top)
        self.history = [t for t in self.history if t['videoId'] != track_data['videoId']]
        
        # Add to beginning
        self.history.insert(0, track_data)
        
        # Keep limit (e.g., 50)
        if len(self.history) > 50:
            self.history = self.history[:50]
            
        self.save_history()

    def get_recent_tracks(self, limit=5):
        return self.history[:limit]

    def get_last_played(self):
        if self.history:
            return self.history[0]
        return None

    def get_top_artists(self, limit=3):
        artist_counts = {}
        for track in self.history:
            artist = track.get('artist')
            if artist:
                artist_counts[artist] = artist_counts.get(artist, 0) + 1
        
        sorted_artists = sorted(artist_counts.items(), key=lambda item: item[1], reverse=True)
        return [artist for artist, count in sorted_artists[:limit]]
