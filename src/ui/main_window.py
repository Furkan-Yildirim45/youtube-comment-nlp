from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from controller.ui_controller import UIController

class MainWindow(QWidget):
    def __init__(self, playlist_csv, video_csv):
        super().__init__()
        self.playlist_csv = playlist_csv
        self.video_csv = video_csv
        self.setWindowTitle("YouTube Yorum Sınıflandırıcı")
        self.setGeometry(100, 100, 800, 600)
        self.ui_controller = UIController(playlist_csv,video_csv)

        # Arayüz elemanları
        self.init_ui()
        
    def init_ui(self):
        self.title_label = QLabel("YouTube Yorumları Duygu Sınıflandırması", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Playlist Dropdown
        self.playlist_label = QLabel("Playlist Seçin:", self)
        self.playlist_dropdown = QComboBox(self)
        self.ui_controller.load_playlists(self.playlist_dropdown)

        # Video Dropdown
        self.video_label = QLabel("Video Seçin:", self)
        self.video_dropdown = QComboBox(self)

        # Playlist değiştiğinde video dropdown'ı güncelle
        self.playlist_dropdown.currentIndexChanged.connect(
            lambda index: self.update_video_dropdown(index)
        )

        # Yorumları gösteren tablo
        self.comments_table = QTableWidget(self)
        self.comments_table.setColumnCount(4)  # 4 sütun: Yorum ID, Yorum Metni, Beğeni Sayısı, Yayınlanma Tarihi
        self.comments_table.setHorizontalHeaderLabels(["Yorum ID", "Yorum Metni", "Beğeni Sayısı", "Yayınlanma Tarihi"])
        self.comments_table.setGeometry(100, 150, 600, 400)  # Tablonun boyutunu ve yerini ayarlayın

        # Yorumları Yükle butonu
        self.load_comments_button = QPushButton("Yorumları Yükle", self)
        self.load_comments_button.clicked.connect(self.load_comments)


        # Sınıflandırma butonu
        self.classify_button = QPushButton("Yorumları Sınıflandır", self)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.playlist_label)
        layout.addWidget(self.playlist_dropdown)
        layout.addWidget(self.video_label)
        layout.addWidget(self.video_dropdown)
        layout.addWidget(self.load_comments_button)
        layout.addWidget(self.comments_table)
        layout.addWidget(self.classify_button)
        self.setLayout(layout)

    def update_video_dropdown(self,index):
        try:
            selected_playlist_id = self.playlist_dropdown.itemData(index)
            print(f"Selected Playlist ID: {selected_playlist_id}")
            if selected_playlist_id:
                videos = self.ui_controller.load_videos_by_playlist(selected_playlist_id)
                print(f"Videos: {videos}")
                self.video_dropdown.clear()
                for video in videos:
                    video_title = f"Video ID: {video['videoId']} - Published At: {video['videoPublishedAt']}"
                    self.video_dropdown.addItem(video_title, video['videoId'])
        except Exception as e:
            print(f"Error: {e}")

    def load_comments(self):
        # Seçilen video ID'sini al (örneğin, önceden seçilen video ID'si)
        selected_video_id = self.video_dropdown.currentData()  # video dropdown'dan alınabilir
        print(f"Selected Video ID: {selected_video_id}")  # Seçilen video ID'sini yazdır

        if selected_video_id:
            # Yorumları al
            comments = self.ui_controller.load_comments_by_video(selected_video_id)
            print(f"Comments: {comments}")  # Alınan yorumları yazdır

            # Yorumları tabloya ekle
            self.comments_table.setRowCount(len(comments))  # Tabloyu, yorum sayısına göre ayarla

            for row, comment in enumerate(comments):
                self.comments_table.setItem(row, 0, QTableWidgetItem(comment['commentId']))  # Yorum ID
                self.comments_table.setItem(row, 1, QTableWidgetItem(comment['commentText']))  # Yorum Metni
                self.comments_table.setItem(row, 2, QTableWidgetItem(str(comment['likeCount'])))  # Beğeni Sayısı
                self.comments_table.setItem(row, 3, QTableWidgetItem(comment['publishedAt']))  # Yayınlanma Tarihi


    # def classify_comments(self):
    #     for row in range(self.comments_table.rowCount()):
    #         comment = self.comments_table.item(row, 0).text()
    #         sentiment = self.get_sentiment(comment)
    #         self.comments_table.setItem(row, 1, QTableWidgetItem(sentiment))
    #         if sentiment == "Olumlu":
    #             self.comments_table.item(row, 1).setBackground(Qt.green)
    #         elif sentiment == "Olumsuz":
    #             self.comments_table.item(row, 1).setBackground(Qt.red)
    #         else:
    #             self.comments_table.item(row, 1).setBackground(Qt.gray)
    #     self.comments_table.setRowCount(0)

    # def get_sentiment(self, comment):
    #     if "kötü" in comment:
    #         return "Olumsuz"
    #     elif "güzel" in comment:
    #         return "Olumlu"
    #     return "Nötr"

