import json
import re
import pandas as pd

class PlaylistService:
    def __init__(self, playlist_csv):
        self.playlists = pd.read_csv(playlist_csv, engine="python")
    
    def _process_snippet(self, snippet_string):
        # Tek tırnakları çift tırnağa çevirme
        snippet_string = re.sub(r"(?<!\\)'", '"', snippet_string)  # Kaçış yapılmamış tek tırnakları çevirir.
        try:
            return json.loads(snippet_string)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error for snippet: {snippet_string}\nError: {e}")
            return {}  # JSON ayrıştırılamazsa boş bir dict döndür

    def get_playlists(self):
        # Snippet içeriğini işler ve veri setine ekler
        self.playlists['snippet'] = self.playlists['snippet'].apply(self._process_snippet)
        # Snippet içerisindeki verileri normalleştiririz
        self.playlists = self.playlists.join(pd.json_normalize(self.playlists['snippet']))
        # Eski snippet sütununu kaldır
        self.playlists.drop(columns=['snippet'], inplace=True)
        return self.playlists

class VideoService:
    def __init__(self, video_csv):
        self.videos = pd.read_csv(video_csv, engine="python")
    
    def get_videos_by_playlist(self, playlist_id):
        # Verilen playlist ID'sine göre videoları alır
        return self.videos[self.videos['playlist_id'] == playlist_id]

    def list_video_ids(self, playlist_id):
        # Playlist ID'sine ait video ID'lerini döndürür
        videos = self.get_videos_by_playlist(playlist_id)
        return videos['videoId'].tolist() if not videos.empty else []
