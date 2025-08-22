import os
import sys
import time
from moviepy import VideoFileClip
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QTextEdit,
    QPushButton, QVBoxLayout, QWidget, QLabel, QProgressBar, QHBoxLayout
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class ConversionThread(QThread):
    conversion_finished = pyqtSignal(str, float, float)  # path, size, duration
    error_occurred = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            start_time = time.time()

            clip = VideoFileClip(self.file_path)
            output_path = os.path.splitext(self.file_path)[0] + ".mp3"

            if not clip.audio:
                raise ValueError("No audio track found in the video!")

            # ✅ Fixed: removed verbose/logger (not supported in MoviePy v2+)
            clip.audio.write_audiofile(output_path, fps=44100, bitrate="320k")
            clip.close()

            conversion_time = time.time() - start_time
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB

            self.conversion_finished.emit(output_path, output_size, conversion_time)

        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Window Settings ---
        self.setWindowTitle("⚡ Ultra-Fast MP4 ➝ MP3 Converter")
        self.setFixedSize(600, 500)
        try:
            self.setWindowIcon(QIcon.fromTheme("media-record"))
        except:
            pass

        # --- Widgets ---
        self.title_label = QLabel("🎶 Convert MP4 Video to MP3 Audio (High Speed)")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel("Select an MP4 file and convert it to MP3 instantly!")
        self.info_label.setFont(QFont("Segoe UI", 10))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #bd93f9;")

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText("File info and conversion logs will appear here...")

        self.btn_1 = QPushButton("📂 Select MP4 File")
        self.btn_2 = QPushButton("🎧 Convert to MP3")
        self.btn_3 = QPushButton("🗑️ Clear Log")
        self.btn_4 = QPushButton("❌ Exit")

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #50fa7b; background-color: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px;")

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.display)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_1)
        button_layout.addWidget(self.btn_2)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.btn_3)
        button_layout2.addWidget(self.btn_4)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.btn_1.clicked.connect(self.select_file)
        self.btn_2.clicked.connect(self.convert)
        self.btn_3.clicked.connect(self.clear_log)
        self.btn_4.clicked.connect(self.close_window)

        self.file_path = None
        self.conversion_thread = None

        # Styling
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #f8f8f2; margin: 5px; }
            QTextEdit {
                background-color: #2c2c3c;
                color: #f8f8f2;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                border: 1px solid #44475a;
            }
            QPushButton {
                background-color: #44475a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #6272a4; }
            QPushButton:pressed { background-color: #bd93f9; }
            QPushButton:disabled { background-color: #333344; color: #888888; }
            QProgressBar {
                border: 2px solid #44475a;
                border-radius: 5px;
                text-align: center;
                background-color: #2c2c3c;
                color: white;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #50fa7b, stop:1 #8be9fd);
                border-radius: 3px;
            }
        """)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select MP4 File', '', 'MP4 Files (*.mp4)')
        if file_path:
            self.file_path = file_path
            self.display.clear()
            self.display.append(f"📂 Selected File: {file_path}")
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            self.display.append(f"📊 Size: {size_mb:.2f} MB")
            self.status_label.setText("File ready for conversion")

    def convert(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select a file first!")
            return

        self.progress_bar.setVisible(True)
        self.status_label.setText("Converting...")

        self.btn_1.setEnabled(False)
        self.btn_2.setEnabled(False)

        self.conversion_thread = ConversionThread(self.file_path)
        self.conversion_thread.conversion_finished.connect(self.conversion_complete)
        self.conversion_thread.error_occurred.connect(self.conversion_error)
        self.conversion_thread.start()

    def conversion_complete(self, output_path, output_size, conversion_time):
        self.progress_bar.setVisible(False)
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)
        self.btn_3.setEnabled(True)

        self.display.append("\n✅ Conversion Complete!")
        self.display.append(f"🎵 Output: {output_path}")
        self.display.append(f"📊 Size: {output_size:.2f} MB")
        self.display.append(f"⚡ Time Taken: {conversion_time:.2f} sec")

        self.status_label.setText("Conversion completed successfully!")
        QMessageBox.information(self, "Success", f"✅ MP3 saved!\n\n{output_path}")

    def conversion_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)
        self.btn_3.setEnabled(True)

        self.display.append(f"\n❌ Error: {error_msg}")
        self.status_label.setText("Conversion failed")
        QMessageBox.critical(self, "Error", f"⚠️ Conversion failed:\n{error_msg}")

    def clear_log(self):
        self.display.clear()
        if self.file_path:
            self.display.append(f"📂 Selected file: {self.file_path}")
        self.status_label.setText("Log cleared")

    def close_window(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
