import os
import shutil
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap
from PyQt6.QtCore import Qt, QSize
from manager import Ui_MainWindow

app = QApplication(sys.argv)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 12px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004275;
            }
            QPushButton#btn_1 {
                background-color: #4CAF50;
            }
            QPushButton#btn_1:hover {
                background-color: #45a049;
            }
            QPushButton#btn_2 {
                background-color: #2196F3;
            }
            QPushButton#btn_2:hover {
                background-color: #0b7dda;
            }
            QPushButton#btn_3 {
                background-color: #f44336;
            }
            QPushButton#btn_3:hover {
                background-color: #d32f2f;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                color: #333;
            }
            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        # Set window properties
        self.setWindowTitle("File Organizer Pro")
        self.setFixedSize(400 , 400)
        self.display.setReadOnly(True)

        # Customize UI elements
        self.display.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)

        # Set button icons (using text as fallback)
        self.btn_1.setText("📁 Select Folder")
        self.btn_2.setText("🔄 Organize Files")
        self.btn_3.setText("❌ Exit")

        # Set button sizes
        self.btn_1.setMinimumHeight(40)
        self.btn_2.setMinimumHeight(40)
        self.btn_3.setMinimumHeight(40)

        # Add application icon (if available)
        try:
            self.setWindowIcon(QIcon("folder_icon.png"))
        except:
            pass

        # Initialize variables
        self.file_path = None

        # Connect signals
        self.btn_1.clicked.connect(self.select_folder)
        self.btn_2.clicked.connect(self.manage)
        self.btn_3.clicked.connect(self.close_window)

        # Add initial message
        self.display.append("Welcome to File Organizer Pro!")
        self.display.append("Please select a folder to begin organizing your files.")
        self.display.append("=" * 30)

    def select_folder(self):
        self.file_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if self.file_path:
            self.display.append(f"Selected folder: {self.file_path}")
            self.display.append("Click 'Organize Files' to start organizing.")
            self.display.append("=" * 30)
        else:
            self.display.append("No folder selected. Please try again.")

    def manage(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return

        try:
            # Define folder mapping for file extensions
            extension_folders = {
                '.gif': 'Images',
                '.jpeg': 'Images',
                '.jpg': 'Images',
                '.png': 'Images',
                '.webp': 'Images',
                '.mp4': 'Videos',
                '.mov': 'Videos',
                '.avi': 'Videos',
                '.wmv': 'Videos',
                '.zip': 'Compressed',
                '.rar': 'Compressed',
                '.7z': 'Compressed',
                '.tar': 'Compressed',
                '.gz': 'Compressed',
                '.mp3': 'Music',
                '.wav': 'Music',
                '.flac': 'Music',
                '.aac': 'Music',
                '.pdf': 'Documents',
                '.doc': 'Documents',
                '.docx': 'Documents',
                '.xlsx': 'Documents',
                '.pptx': 'Documents',
                '.csv': 'Documents',
                '.txt': 'Documents',
                '.py': 'Programs',
                '.java': 'Programs',
                '.cpp': 'Programs',
                '.html': 'Programs',
                '.css': 'Programs',
                '.js': 'Programs',
                '.deb': 'Programs',
                '.exe': 'Programs',
                '.msi': 'Programs',
                '.ini': 'System Files',
                '.icc': 'System Files',
                '.dll': 'System Files',
                '.sys': 'System Files',
            }

            # Get list of existing folders (case insensitive)
            existing_folders = [folder.lower() for folder in os.listdir(self.file_path)
                                if os.path.isdir(os.path.join(self.file_path, folder))]

            moved_count = 0
            skipped_count = 0

            for item in os.listdir(self.file_path):
                item_path = os.path.join(self.file_path, item)
                if os.path.isfile(item_path):
                    _, ext = os.path.splitext(item)
                    ext = ext.lower()  # Normalize to lowercase

                    if ext in extension_folders:
                        # Determine target folder name
                        target_folder = extension_folders[ext]

                        # Check if folder already exists (case insensitive)
                        if target_folder.lower() not in existing_folders:
                            # Create new folder if not already present
                            os.makedirs(os.path.join(self.file_path, target_folder), exist_ok=True)
                            existing_folders.append(target_folder.lower())
                            self.display.append(f"Created folder: {target_folder}")

                        # Move file to the appropriate folder
                        shutil.move(item_path, os.path.join(self.file_path, target_folder, item))
                        self.display.append(f"✓ Moved: {item} → {target_folder}")
                        moved_count += 1
                    else:
                        self.display.append(f"✗ Skipped: {item} (unknown extension)")
                        skipped_count += 1

            # Display summary
            self.display.append("=" * 30)
            self.display.append(f"Organization complete!")
            self.display.append(f"Moved {moved_count} files, skipped {skipped_count} files.")
            self.display.append("=" * 30)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{str(e)}")

    def close_window(self):
        reply = QMessageBox.question(self, 'Confirm Exit',
                                     'Are you sure you want to exit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()


if __name__ == "__main__":
    window = MainWindow()
    window.show()
    sys.exit(app.exec())