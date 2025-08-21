import os
import sys
from moviepy import VideoFileClip
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from mp4_GUI import Ui_MainWindow

app = QApplication(sys.argv)

class MainWindow(QMainWindow , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Convert mp4 to mp3")
        self.setFixedSize(400 , 400)
        self.display.setReadOnly(True)

        self.btn_1.clicked.connect(self.select_file)
        self.btn_2.clicked.connect(self.convert)
        self.btn_3.clicked.connect(self.close_window)
        self.file_path = None


    def select_file(self):
        self.file_path = QFileDialog.getOpenFileName(self , 'select file' , '' , '(*.mp4)')[0]
        self.display.append(self.file_path)

    def convert(self):
        if not self.file_path:
            return
        try:
            clip = VideoFileClip(self.file_path)
            output_path = os.path.splitext(self.file_path)[0] + ".mp3"
            clip.audio.write_audiofile(output_path)
            QMessageBox.information(self, "Success", f"MP3 saved to:\n{output_path}")
            self.display.append(f"Success -> MP3 saved to:\n{output_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Something went wrong:\n{e}")

    def close_window(self):
        self.close()

window = MainWindow()
window.show()
sys.exit(app.exec())