from PyQt5.QtWidgets import QApplication, QHeaderView, QWidget, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from controller.ui_controller import UIController

class MainWindow(QWidget):
    def __init__(self, playlist_csv, video_csv, model_path):
        super().__init__()
        self.playlist_csv = playlist_csv
        self.video_csv = video_csv
        self.setWindowTitle("YouTube Yorum Sınıflandırıcı")
        self.setGeometry(100, 100, 800, 600)
        self.ui_controller = UIController(playlist_csv, video_csv, model_path)
 
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
        self.classify_button.clicked.connect(self.classify_comments)  # Sınıflandırma işlevini bağla

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
        
        self.comments_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 1 numaralı sütun "Yorum Metni"

    def update_table_headers_with_sentiment(self):
        self.comments_table.setColumnCount(5)  # Duygu Durumu eklemesiyle sütun sayısını artır
        self.comments_table.setHorizontalHeaderLabels(["Yorum ID", "Yorum Metni", "Beğeni Sayısı", "Yayınlanma Tarihi", "Duygu Durumu"])

    def update_video_dropdown(self, index):
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

            # Duygu durumu sütununu sıfırlayalım (5. sütun)
            self.comments_table.setColumnCount(4)  # Duygu durumu sütunu (5. sütun) kaldırıldı

            # Yorumları tabloya ekle
            self.comments_table.setRowCount(len(comments))  # Tabloyu, yorum sayısına göre ayarla

            for row, comment in enumerate(comments):
                self.comments_table.setItem(row, 0, QTableWidgetItem(comment['commentId']))  # Yorum ID
                self.comments_table.setItem(row, 1, QTableWidgetItem(comment['commentText']))  # Yorum Metni
                self.comments_table.setItem(row, 2, QTableWidgetItem(str(comment['likeCount'])))  # Beğeni Sayısı
                self.comments_table.setItem(row, 3, QTableWidgetItem(comment['publishedAt']))  # Yayınlanma Tarihi

    def classify_comments(self):
        selected_video_id = self.video_dropdown.currentData()
        if selected_video_id:
            comments = self.ui_controller.load_comments_by_video(selected_video_id)
            sentiments = self.ui_controller.classify_comments(comments)

            # Tabloya 5. sütunu ekleyelim
            self.update_table_headers_with_sentiment()  # Duygu Durumu sütununu ekle

            # Sonuçları tabloya ekleyelim
            for row, sentiment in enumerate(sentiments):
                # 5. sütunda (index 4) hücreyi ekleyin
                item = self.comments_table.item(row, 4)
                if item is None:  # Eğer hücre mevcut değilse
                    item = QTableWidgetItem(sentiment)
                    self.comments_table.setItem(row, 4, item)

                # Renk değiştirme işlemini burada yapın
                item = self.comments_table.item(row, 4)  # Duygu Durumu sütununu al
                if sentiment == "Pozitif":
                    item.setBackground(QColor(0, 255, 0))  # Yeşil
                elif sentiment == "Negatif":
                    item.setBackground(QColor(255, 0, 0))  # Kırmızı
                else:
                    item.setBackground(QColor(128, 128, 128))  # Gri