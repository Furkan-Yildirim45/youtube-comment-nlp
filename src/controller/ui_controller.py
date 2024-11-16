
from tkinter import messagebox
import pandas as pd
from models.neurel_network_model import NeuralNetworkModel
from services.playlist_videos_service import PlaylistService, VideoService


class UIController:
    def __init__(self, playlist_csv, video_csv, model_path):
        super().__init__()
        self.playlist_service = PlaylistService(playlist_csv)
        self.video_service = VideoService(video_csv)

        # Modeli burada yüklüyoruz
        if model_path:
            self.sentiment_model = NeuralNetworkModel(model_path=model_path)  # Model yolunu gönder
        else:
            self.sentiment_model = None

    def load_playlists(self, playlist_dropdown):
        playlists = self.playlist_service.get_playlists()
        for idx, playlist in playlists.iterrows():
            title = playlist['title'] if pd.notna(playlist['title']) else "Unknown Title"
            playlist_id = playlist['id'] if pd.notna(playlist['id']) else "Unknown ID"
            playlist_dropdown.addItem(title, playlist_id)

    
    def load_videos_by_playlist(self, playlist_id):
        # Video verilerini içeren CSV dosyasını yükle
        videos_df = pd.read_csv('./datasets/CampusX-official_videos.csv')

        # Playlist ID'ye göre filtreleme yap
        filtered_videos = videos_df[videos_df['playlist_id'] == playlist_id]
        print(f"Filtered Videos for Playlist ID {playlist_id}:")  # Playlist ID'sini yazdır
        print(filtered_videos)  # Filtrelenmiş videoları yazdır
        
        # Videoları işlemeye başla
        video_list = []
        for idx, video in filtered_videos.iterrows():
            video_data = {
                'videoId': video['videoId'],
                'videoPublishedAt': video['videoPublishedAt']
            }
            video_list.append(video_data)

        print(f"Video List: {video_list}")  # Oluşan video listesini yazdır
        return video_list


    def load_comments_by_video(self, video_id):
        # Yorum verilerini içeren CSV dosyasını yükle
        comments_df = pd.read_csv('./datasets/CampusX-official_comments.csv')
        translated_comment = pd.read_csv('./datasets/CampusX-official_comments_translated.csv')
        
        # Video ID'ye göre filtreleme yap
        filtered_comments = comments_df[comments_df['snippet_topLevelComment_snippet_videoId'] == video_id]

        print(f"Filtered Comments for Video ID {video_id}:")  # Video ID'sine ait yorumları yazdır
        print(filtered_comments)  # Filtrelenmiş yorumları yazdır

        # Yorumları işlemeye başla
        comment_list = []
        for index, comment in filtered_comments.iterrows():

            comment_data = {
                'commentId': comment['snippet_topLevelComment_id'],
                'commentText': str(comment['translated_tr']) if not pd.isna(comment['translated_tr']) else "",  # NaN değerleri kontrol et ve dönüştür
                'originalCommentText': comment['snippet_topLevelComment_snippet_textOriginal'],
                'viewerRating': comment['snippet_topLevelComment_snippet_viewerRating'],
                'likeCount': comment['snippet_topLevelComment_snippet_likeCount'],
                'publishedAt': comment['snippet_topLevelComment_snippet_publishedAt'],
                'updatedAt': comment['snippet_topLevelComment_snippet_updatedAt'],
                'canReply': comment['snippet_canReply'],
                'totalReplyCount': comment['snippet_totalReplyCount'],
                'isPublic': comment['snippet_isPublic']
            }
            comment_list.append(comment_data)

        print(f"Comment List: {comment_list}")  # Oluşan yorum listesini yazdır
        return comment_list

    def classify_comments(self, comments):
        # Yorumları sırayla sınıflandırmak
        sentiments = []
        for comment in comments:
            # Yorum metni boş mu kontrol et
            if not comment['commentText'].strip():  # Boş veya sadece boşluk olan yorumları kontrol et
                sentiment = "Nötr"  # Eğer boşsa, nötr olarak işaretle
            else:
                sentiment = self.sentiment_model.predict_sentiment(comment['commentText'])  # Diğer yorumları sınıflandır
            sentiments.append(sentiment)
        return sentiments

