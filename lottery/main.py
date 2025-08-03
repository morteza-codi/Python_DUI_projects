import os
import sys
import random
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,
                             QDialog, QTextEdit, QVBoxLayout, QPushButton, QWidget,
                             QLabel, QLineEdit, QHBoxLayout, QFrame, QSizePolicy,
                             QSpacerItem, QScrollArea, QProgressBar, QGraphicsDropShadowEffect)
from PyQt6.QtGui import (QGuiApplication, QFont, QColor, QPixmap, QIcon,
                         QPainter, QLinearGradient, QPalette, QDragEnterEvent,
                         QDropEvent, QMovie, QIntValidator)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect,
                          pyqtProperty, QSize, QPoint)


class Settings:
    def __init__(self):
        self.config_file = "lottery_config.json"
        self.defaults = {
            "theme": "dark",
            "recent_files": [],
            "save_results": True,
            "animation_speed": 1.0
        }
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.defaults

    def save_settings(self):
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()


class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._scale = 1.0
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(1.1)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        transform = painter.transform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.scale(self.scale, self.scale)
        transform.translate(-self.width() / 2, -self.height() / 2)
        painter.setTransform(transform)

        super().paintEvent(event)


class WinnerDialog(QDialog):
    def __init__(self, winners, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎉 Winners List")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.layout = QVBoxLayout(self)

        # Header
        header = QLabel("Congratulations to the Winners!")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                margin: 15px;
            }
        """)
        self.layout.addWidget(header)

        # Winner list
        self.winner_text = QTextEdit()
        self.winner_text.setReadOnly(True)
        self.winner_text.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                background: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.winner_text.setText("\n".join(f"{i + 1}. {winner}" for i, winner in enumerate(winners)))
        self.layout.addWidget(self.winner_text)

        # Button row
        button_layout = QHBoxLayout()

        self.copy_btn = AnimatedButton("Copy List")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #0b7dda;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        self.save_btn = AnimatedButton("Save Results")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self.save_results)

        self.close_btn = AnimatedButton("Close")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #da190b;
            }
        """)
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.close_btn)

        self.layout.addLayout(button_layout)

        # Add drop shadow
        self.setGraphicsEffect(self.create_shadow_effect())

    def create_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        return shadow

    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.winner_text.toPlainText())
        QMessageBox.information(self, "Copied", "Winners list copied to clipboard!")

    def save_results(self):
        file_name = f"winners_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Save Winners List", file_name, "Text Files (*.txt)")

        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.winner_text.toPlainText())
                QMessageBox.information(self, "Saved", f"Winners list saved to:\n{path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file:\n{str(e)}")


class LotteryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.participants = []
        self.current_theme = self.settings.get("theme")

        self.setup_ui()
        self.setup_animations()
        self.apply_theme(self.current_theme)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def setup_ui(self):
        self.setWindowTitle("🎰 Ultimate Lottery Draw")
        self.setMinimumSize(800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main container
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        self.setCentralWidget(self.main_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Title bar
        self.setup_title_bar()

        # Content area
        self.setup_content_area()

        # Status bar
        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("font-size: 12px; color: #666;")
        self.main_layout.addWidget(self.status_bar)

        # Apply initial styles
        self.update_styles()

    def setup_title_bar(self):
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Title
        self.title_label = QLabel("🎰 Ultimate Lottery Draw")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Theme toggle button
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(30, 30)
        self.theme_btn.setObjectName("ThemeButton")
        self.theme_btn.clicked.connect(self.toggle_theme)

        # Minimize button
        self.minimize_btn = QPushButton("─")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setObjectName("MinimizeButton")
        self.minimize_btn.clicked.connect(self.showMinimized)

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.clicked.connect(self.close)

        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addWidget(spacer)
        title_bar_layout.addWidget(self.theme_btn)
        title_bar_layout.addWidget(self.minimize_btn)
        title_bar_layout.addWidget(self.close_btn)

        self.main_layout.addWidget(title_bar)

    def setup_content_area(self):
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(30)

        # File selection section
        self.setup_file_section()

        # Drawing animation placeholder
        self.setup_animation_section()

        # Results section
        self.setup_results_section()

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

    def setup_file_section(self):
        file_frame = QFrame()
        file_frame.setObjectName("FileFrame")
        file_layout = QVBoxLayout(file_frame)
        file_layout.setContentsMargins(20, 20, 20, 20)
        file_layout.setSpacing(15)

        # Section title
        file_title = QLabel("📁 Participant Selection")
        file_title.setObjectName("SectionTitle")
        file_layout.addWidget(file_title)

        # File input row
        file_input_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Drag & drop a text file or click browse...")
        self.file_input.setObjectName("FileInput")
        self.file_input.setReadOnly(True)

        self.browse_btn = AnimatedButton("Browse")
        self.browse_btn.setObjectName("BrowseButton")
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.clicked.connect(self.browse_file)

        file_input_layout.addWidget(self.file_input)
        file_input_layout.addWidget(self.browse_btn)

        file_layout.addLayout(file_input_layout)

        # File info
        self.file_info = QLabel("No file selected")
        self.file_info.setObjectName("FileInfo")
        self.file_info.setWordWrap(True)
        file_layout.addWidget(self.file_info)

        self.content_layout.addWidget(file_frame)

    def setup_animation_section(self):
        self.animation_frame = QFrame()
        self.animation_frame.setObjectName("AnimationFrame")
        self.animation_frame.setFixedHeight(200)

        animation_layout = QVBoxLayout(self.animation_frame)
        animation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Setup loading animation
        self.loading_movie = QMovie(":images/loading.gif")  # Using Qt resource system
        self.loading_movie.setScaledSize(QSize(100, 100))
        self.animation_label.setMovie(self.loading_movie)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.result_label.hide()

        animation_layout.addWidget(self.animation_label)
        animation_layout.addWidget(self.result_label)

        self.content_layout.addWidget(self.animation_frame)
        self.animation_frame.hide()

    def setup_results_section(self):
        results_frame = QFrame()
        results_frame.setObjectName("ResultsFrame")
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(15)

        # Section title
        results_title = QLabel("⚙️ Draw Settings")
        results_title.setObjectName("SectionTitle")
        results_layout.addWidget(results_title)

        # Number of winners
        num_winners_layout = QHBoxLayout()

        num_label = QLabel("Number of Winners:")
        num_label.setObjectName("SettingLabel")

        self.num_winners = QLineEdit()
        self.num_winners.setPlaceholderText("Enter number of winners...")
        self.num_winners.setValidator(QIntValidator(1, 999))
        self.num_winners.setObjectName("NumberInput")
        self.num_winners.setFixedWidth(100)

        num_winners_layout.addWidget(num_label)
        num_winners_layout.addWidget(self.num_winners)
        num_winners_layout.addStretch()

        results_layout.addLayout(num_winners_layout)

        # Draw button
        self.draw_btn = AnimatedButton("🎲 Draw Winners!")
        self.draw_btn.setObjectName("DrawButton")
        self.draw_btn.clicked.connect(self.draw_winners)

        results_layout.addWidget(self.draw_btn)

        self.content_layout.addWidget(results_frame)

    def setup_animations(self):
        # Window fade animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)

        # Draw animation timer
        self.draw_timer = QTimer()
        self.draw_timer.setInterval(100)
        self.draw_timer.timeout.connect(self.update_draw_animation)

        # Winner display animation
        self.winner_animation = QPropertyAnimation(self.result_label, b"pos")
        self.winner_animation.setDuration(1000)
        self.winner_animation.setEasingCurve(QEasingCurve.Type.OutBounce)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.settings.set("theme", theme)

        if theme == "dark":
            self.setStyleSheet("""
                #MainWidget {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #2c3e50, stop:1 #4ca1af);
                    border-radius: 15px;
                    border: 2px solid #34495e;
                }

                #TitleBar {
                    background: transparent;
                    padding: 5px;
                }

                #TitleLabel {
                    color: #ecf0f1;
                    font-size: 18px;
                    font-weight: bold;
                }

                #ThemeButton, #MinimizeButton, #CloseButton {
                    background: transparent;
                    color: #ecf0f1;
                    border: none;
                    border-radius: 15px;
                    font-size: 14px;
                }

                #ThemeButton:hover, #MinimizeButton:hover {
                    background: rgba(255, 255, 255, 0.1);
                }

                #CloseButton:hover {
                    background: #e74c3c;
                }

                #FileFrame, #ResultsFrame {
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }

                #SectionTitle {
                    color: #ecf0f1;
                    font-size: 18px;
                    font-weight: bold;
                }

                #FileInput {
                    background: rgba(255, 255, 255, 0.1);
                    color: #ecf0f1;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    padding: 8px;
                    selection-background-color: #3498db;
                }

                #BrowseButton, #DrawButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #3498db, stop:1 #2ecc71);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 15px;
                    font-weight: bold;
                }

                #BrowseButton:hover, #DrawButton:hover {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #2980b9, stop:1 #27ae60);
                }

                #NumberInput {
                    background: rgba(255, 255, 255, 0.1);
                    color: #ecf0f1;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    padding: 8px;
                }

                #SettingLabel {
                    color: #bdc3c7;
                }

                #FileInfo {
                    color: #bdc3c7;
                    font-size: 12px;
                }

                #AnimationFrame {
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
        else:
            self.setStyleSheet("""
                #MainWidget {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #f5f7fa, stop:1 #c3cfe2);
                    border-radius: 15px;
                    border: 2px solid #d1d8e0;
                }

                #TitleBar {
                    background: transparent;
                    padding: 5px;
                }

                #TitleLabel {
                    color: #2c3e50;
                    font-size: 18px;
                    font-weight: bold;
                }

                #ThemeButton, #MinimizeButton, #CloseButton {
                    background: transparent;
                    color: #2c3e50;
                    border: none;
                    border-radius: 15px;
                    font-size: 14px;
                }

                #ThemeButton:hover, #MinimizeButton:hover {
                    background: rgba(0, 0, 0, 0.1);
                }

                #CloseButton:hover {
                    background: #e74c3c;
                    color: white;
                }

                #FileFrame, #ResultsFrame {
                    background: rgba(255, 255, 255, 0.7);
                    border-radius: 10px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }

                #SectionTitle {
                    color: #2c3e50;
                    font-size: 18px;
                    font-weight: bold;
                }

                #FileInput {
                    background: white;
                    color: #2c3e50;
                    border: 1px solid #d1d8e0;
                    border-radius: 5px;
                    padding: 8px;
                    selection-background-color: #3498db;
                }

                #BrowseButton, #DrawButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #3498db, stop:1 #2ecc71);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 15px;
                    font-weight: bold;
                }

                #BrowseButton:hover, #DrawButton:hover {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #2980b9, stop:1 #27ae60);
                }

                #NumberInput {
                    background: white;
                    color: #2c3e50;
                    border: 1px solid #d1d8e0;
                    border-radius: 5px;
                    padding: 8px;
                }

                #SettingLabel {
                    color: #7f8c8d;
                }

                #FileInfo {
                    color: #7f8c8d;
                    font-size: 12px;
                }

                #AnimationFrame {
                    background: rgba(255, 255, 255, 0.7);
                    border-radius: 10px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)

    def toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)

    def update_styles(self):
        self.theme_btn.setIcon(QIcon(":images/theme.png"))  # Using Qt resource system

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos'):
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].toLocalFile().endswith('.txt'):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.load_participants(file_path)

    def browse_file(self):
        recent_files = self.settings.get("recent_files")
        start_dir = os.path.dirname(recent_files[0]) if recent_files else ""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Participants File",
            start_dir,
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            self.load_participants(file_path)

    def load_participants(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.participants = [line.strip() for line in f if line.strip()]

            if not self.participants:
                raise ValueError("File is empty")

            self.file_input.setText(file_path)
            self.file_info.setText(f"Loaded {len(self.participants)} participants from:\n{file_path}")

            # Add to recent files
            recent_files = self.settings.get("recent_files")
            if file_path in recent_files:
                recent_files.remove(file_path)
            recent_files.insert(0, file_path)
            recent_files = recent_files[:5]  # Keep only last 5
            self.settings.set("recent_files", recent_files)

            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load file:\n{str(e)}")
            return False

    def validate_inputs(self):
        if not self.participants:
            QMessageBox.warning(self, "No Participants", "Please load a participants file first!")
            return False

        try:
            num_winners = int(self.num_winners.text())
            if num_winners <= 0:
                raise ValueError
            if num_winners > len(self.participants):
                QMessageBox.warning(
                    self,
                    "Too Many Winners",
                    f"You requested {num_winners} winners but only have {len(self.participants)} participants!"
                )
                return False
            return True
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number of winners!")
            return False

    def draw_winners(self):
        if not self.validate_inputs():
            return

        num_winners = int(self.num_winners.text())

        # Show animation
        self.animation_frame.show()
        self.loading_movie.start()
        self.result_label.hide()
        self.draw_btn.setEnabled(False)

        # Start draw animation
        self.draw_counter = 0
        self.final_winners = random.sample(self.participants, num_winners)
        self.draw_timer.start()

        # Set timer to stop animation
        QTimer.singleShot(2000 + num_winners * 300, self.finish_draw)

    def update_draw_animation(self):
        self.draw_counter += 1
        if self.draw_counter % 5 == 0:
            random_name = random.choice(self.participants)
            self.result_label.setText(random_name)
            self.result_label.show()

    def finish_draw(self):
        self.draw_timer.stop()
        self.loading_movie.stop()
        self.animation_label.hide()

        # Display final winners with animation
        winners_text = "\n".join(f"{i + 1}. {winner}" for i, winner in enumerate(self.final_winners))
        self.result_label.setText(winners_text)

        # Animate the result label
        self.result_label.move(self.result_label.x(), self.result_label.y() + 50)
        self.result_label.setStyleSheet("font-size: 16px;")
        self.winner_animation.setStartValue(QPoint(self.result_label.x(), self.result_label.y()))
        self.winner_animation.setEndValue(QPoint(self.result_label.x(), self.result_label.y() - 50))
        self.winner_animation.start()

        self.draw_btn.setEnabled(True)

        # Show winners dialog
        self.show_winners_dialog(self.final_winners)

    def show_winners_dialog(self, winners):
        dialog = WinnerDialog(winners, self)
        dialog.exec()

    def closeEvent(self, event):
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()
        self.fade_animation.finished.connect(event.accept)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style and attributes
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(":images/lottery.png"))

    window = LotteryApp()

    # Start with fade-in animation
    window.setWindowOpacity(0.0)
    window.show()

    fade_in = QPropertyAnimation(window, b"windowOpacity")
    fade_in.setDuration(500)
    fade_in.setStartValue(0.0)
    fade_in.setEndValue(1.0)
    fade_in.start()

    sys.exit(app.exec())