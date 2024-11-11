"""import nltk
from services.comment_service import CommentService

def main():
    dosya_adi = "CampusX-translated_comments"
    yorum_servisi = CommentService('./datasets/{0}.csv'.format(dosya_adi))
    
    # Tek seferde tüm işlemleri gerçekleştir
    yorum_servisi.process_all_steps(dosya_adi)

if __name__ == "__main__":
    main()
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src/")))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src/ui/")))

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("./datasets/CampusX-official_playlist.csv",'./datasets/CampusX-official_videos.csv')
    window.show()
    sys.exit(app.exec_())
