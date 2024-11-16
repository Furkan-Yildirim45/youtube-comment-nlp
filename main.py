import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src/")))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src/ui/")))

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model_path = "./models/neural_network/model.keras"
    window = MainWindow("./datasets/CampusX-official_playlist.csv", './datasets/CampusX-official_videos.csv', model_path)
    window.show()
    sys.exit(app.exec_())

