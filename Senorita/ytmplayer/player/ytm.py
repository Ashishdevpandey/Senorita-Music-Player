from ytmusicapi import YTMusic

class YTMusicClient:
    def __init__(self):
        self.ytmusic = YTMusic()

    def search(self, query):
        """
        Search for songs and videos on YouTube Music.
        Returns a list of dictionaries with title, artist, videoId, and thumbnail.
        """
        try:
            results = self.ytmusic.search(query, filter="songs")
            # Also search for videos if songs are sparse, but "songs" filter is usually best for a music player
            # We can also try "videos" or just general search.
            # Let's stick to songs for now to ensure we get audio tracks.
            
            parsed_results = []
            for item in results:
                if item['resultType'] not in ['song', 'video']:
                    continue
                
                title = item['title']
                artists = ", ".join([a['name'] for a in item['artists']])
                video_id = item['videoId']
                
                # Get the best thumbnail
                thumbnails = item.get('thumbnails', [])
                thumbnail_url = thumbnails[-1]['url'] if thumbnails else ""
                
                parsed_results.append({
                    'title': title,
                    'artist': artists,
                    'videoId': video_id,
                    'thumbnail': thumbnail_url
                })
            
            return parsed_results
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            return []

    def get_song_url(self, video_id):
        return f"https://www.youtube.com/watch?v={video_id}"

    def get_recommendations(self, video_id):
        try:
            # Get "Watch Playlist" (Radio) for the song
            results = self.ytmusic.get_watch_playlist(videoId=video_id, limit=10)
            
            tracks = []
            if 'tracks' in results:
                for track in results['tracks']:
                    if track.get('videoId') != video_id:
                        tracks.append({
                            'videoId': track['videoId'],
                            'title': track['title'],
                            'artist': track['artists'][0]['name'] if track.get('artists') else "Unknown",
                            'duration': track.get('length', ''),
                            'thumbnail': track['thumbnail'][0]['url'] if track.get('thumbnail') else None
                        })
            return tracks
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    def get_artist_top_songs(self, artist_name):
        try:
            # Search for the artist to get their ID
            search_results = self.ytmusic.search(artist_name, filter='artists')
            if search_results:
                artist_id = search_results[0]['browseId']
                artist_details = self.ytmusic.get_artist(artist_id)
                
                tracks = []
                if 'songs' in artist_details and 'results' in artist_details['songs']:
                    for song in artist_details['songs']['results']:
                        tracks.append({
                            'videoId': song['videoId'],
                            'title': song['title'],
                            'artist': artist_name,
                            'duration': song.get('duration', ''), # Might be missing
                            'thumbnail': song['thumbnails'][0]['url'] if song.get('thumbnails') else None
                        })
                return tracks
            return []
        except Exception as e:
            print(f"Error getting artist top songs: {e}")
            return []
