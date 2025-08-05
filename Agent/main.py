import os
import subprocess
import sys
import time
import webbrowser
from pprint import pprint
import logging
import json

import cv2
import pyautogui
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import threading
from typing import Optional, Dict

import wolframalpha
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot, Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QVBoxLayout, QPushButton, QTextEdit, QMessageBox,
    QProgressBar, QWidget, QComboBox, QSlider, QGridLayout, QGraphicsDropShadowEffect,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QFont, QPalette, QPixmap, QIcon, QLinearGradient, QBrush, QPainter
from wikipedia import wikipedia

from agent import Ui_MainWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TTSEngine:
    """Singleton class for TTS engine"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.engine = pyttsx3.init()
                cls._instance.engine.setProperty('rate', 150)
                cls._instance.voices = cls._instance.engine.getProperty('voices')
                logger.info("TTS engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize TTS engine: {str(e)}")
                raise
        return cls._instance

    def speak(self, text: str):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"Spoke text: {text[:50]}...")  # Log first 50 chars
        except Exception as e:
            logger.error(f"Error in speaking text: {str(e)}")
            raise


class SettingsManager:
    """Manages application settings"""

    def __init__(self):
        self.settings_file = 'assistant_settings.json'
        self.settings = self.load_settings()

    def load_settings(self) -> Dict:
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    logger.info("Settings loaded successfully")
                    return settings
        except Exception as e:
            logger.error(f"Error loading settings: {str(e)}")

        # Default settings
        return {
            'voice': 0,
            'speed': 150,
            'volume': 1.0,
            'user_name': '',
            'language': 'en-US',
            'timeout': 5
        }

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")

    def update_setting(self, key: str, value):
        """Update a specific setting"""
        self.settings[key] = value
        self.save_settings()


class CommandHandler:
    """Handles voice commands using command pattern"""

    def __init__(self, parent):
        self.parent = parent
        self.commands = {
            'wikipedia': self.handle_wikipedia,
            'youtube': self.handle_youtube,
            'google': self.handle_google,
            'gmail': self.handle_gmail,
            'news': self.handle_news,
            'time': self.handle_time,
            'camera': self.handle_camera,
            'photo': self.handle_camera,
            'screenshot': self.handle_screenshot,
            'search': self.handle_search,
            'question': self.handle_question,
            'who': self.handle_who,
            'write note': self.handle_write_note,
            'show note': self.handle_show_note,
            'telegram': self.handle_telegram,
            'logout': self.handle_logout,
            'weather': self.handle_weather,
            'reminder': self.handle_reminder,
            'calculate': self.handle_calculation
        }

    def execute_command(self, command: str) -> bool:
        """Execute the appropriate command handler"""
        for key, handler in self.commands.items():
            if key in command:
                try:
                    handler(command)
                    return True
                except Exception as e:
                    logger.error(f"Error executing command {key}: {str(e)}")
                    self.parent.speak(f"Sorry, I couldn't complete that action. Error: {str(e)}")
                    return False
        return False

    # Command handlers implementation...
    def handle_wikipedia(self, command: str):
        """Handle wikipedia search command"""
        self.parent.speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "").strip()
        if not query:
            self.parent.speak("What would you like to search on Wikipedia?")
            query = self.parent.take_command()

        try:
            summary = wikipedia.summary(query, sentences=3)
            self.parent.speak(f"According to Wikipedia: {summary}")
        except wikipedia.exceptions.DisambiguationError as e:
            self.parent.speak(
                f"There are multiple options. Please be more specific. Some options are: {', '.join(e.options[:3])}")
        except wikipedia.exceptions.PageError:
            self.parent.speak("Sorry, I couldn't find any information on that topic.")

    def handle_youtube(self, command: str):
        """Handle YouTube opening command"""
        self.parent.speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    def handle_google(self, command: str):
        """Handle Google opening command"""
        self.parent.speak("Opening Google")
        webbrowser.open("https://www.google.com")

    def handle_gmail(self, command: str):
        """Handle Gmail opening command"""
        self.parent.speak("Opening Gmail")
        webbrowser.open("https://www.gmail.com")

    def handle_news(self, command: str):
        """Handle news opening command"""
        self.parent.speak("Opening news")
        webbrowser.open("https://news.google.com")

    def handle_time(self, command: str):
        """Handle time inquiry command"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.parent.speak(f"The current time is {current_time}")

    def handle_camera(self, command: str):
        """Handle camera/photo command"""
        try:
            self.parent.speak("Taking a photo")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"photo_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                self.parent.speak(f"Photo saved as {filename}")
            else:
                self.parent.speak("Sorry, I couldn't access the camera")
            cap.release()
        except Exception as e:
            self.parent.speak("Sorry, there was an error with the camera")
            logger.error(f"Camera error: {str(e)}")

    def handle_screenshot(self, command: str):
        """Handle screenshot command"""
        try:
            self.parent.speak("Taking a screenshot")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            self.parent.speak(f"Screenshot saved as {filename}")
        except Exception as e:
            self.parent.speak("Sorry, there was an error taking the screenshot")
            logger.error(f"Screenshot error: {str(e)}")

    def handle_search(self, command: str):
        """Handle web search command"""
        query = command.replace("search", "").strip()
        if not query:
            self.parent.speak("What would you like to search for?")
            query = self.parent.take_command()

        if query:
            self.parent.speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    def handle_question(self, command: str):
        """Handle question/calculation command"""
        try:
            self.parent.speak("What is your question?")
            question = self.parent.take_command()
            if question:
                # Use Wolfram Alpha for calculations and factual questions
                app_id = "X7RHRG-4JVEER92T2"
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                answer = next(res.results).text
                self.parent.speak(f"The answer is: {answer}")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't find an answer to that question")
            logger.error(f"Question handling error: {str(e)}")

    def handle_who(self, command: str):
        """Handle who am I command"""
        self.parent.speak("I am your AI assistant, created to help you with various tasks using voice commands.")

    def handle_write_note(self, command: str):
        """Handle write note command"""
        self.parent.speak("What would you like me to write?")
        note_content = self.parent.take_command()
        if note_content:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("notes.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {note_content}\n")
                self.parent.speak("Note saved successfully")
            except Exception as e:
                self.parent.speak("Sorry, I couldn't save the note")
                logger.error(f"Note writing error: {str(e)}")

    def handle_show_note(self, command: str):
        """Handle show note command"""
        try:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r", encoding="utf-8") as f:
                    notes = f.read().strip()
                if notes:
                    self.parent.speak("Here are your notes")
                    # Read the last few notes
                    lines = notes.split("\n")
                    recent_notes = lines[-3:] if len(lines) > 3 else lines
                    for note in recent_notes:
                        self.parent.speak(note)
                else:
                    self.parent.speak("You don't have any notes yet")
            else:
                self.parent.speak("You don't have any notes yet")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't read your notes")
            logger.error(f"Note reading error: {str(e)}")

    def handle_telegram(self, command: str):
        """Handle Telegram opening command"""
        try:
            self.parent.speak("Opening Telegram")
            # Try common Telegram paths
            telegram_paths = [
                r"C:\Users\{username}\AppData\Roaming\Telegram Desktop\Telegram.exe".format(
                    username=os.getenv('USERNAME')),
                r"C:\Program Files\Telegram Desktop\Telegram.exe",
                "telegram"  # If in PATH
            ]

            for path in telegram_paths:
                try:
                    if os.path.exists(path):
                        os.startfile(path)
                        return
                except:
                    continue

            # If not found locally, open web version
            webbrowser.open("https://web.telegram.org")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't open Telegram")
            logger.error(f"Telegram opening error: {str(e)}")

    def handle_logout(self, command: str):
        """Handle system logout command"""
        self.parent.speak("Logging out in 5 seconds. Say cancel to stop.")
        # Give user a chance to cancel
        QTimer.singleShot(5000, self._perform_logout)

    def _perform_logout(self):
        """Perform the actual logout"""
        try:
            if sys.platform == "win32":
                os.system("shutdown /l")
            elif sys.platform == "darwin":  # macOS
                os.system("osascript -e 'tell application \"System Events\" to log out'")
            else:  # Linux
                os.system("gnome-session-quit --logout --no-prompt")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't log out the system")
            logger.error(f"Logout error: {str(e)}")

    def handle_weather(self, command: str):
        """Handle weather inquiry command"""
        try:
            self.parent.speak("Which city would you like to know the weather for?")
            city = self.parent.take_command()
            if city:
                # Use OpenWeatherMap API (you'll need to get a free API key)
                api_key = "your_openweather_api_key"  # Replace with actual API key
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    temp = data['main']['temp']
                    description = data['weather'][0]['description']
                    self.parent.speak(
                        f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius")
                else:
                    self.parent.speak("Sorry, I couldn't get the weather information for that city")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't get the weather information")
            logger.error(f"Weather error: {str(e)}")

    def handle_calculation(self, command: str):
        """Handle calculation command"""
        try:
            expression = command.replace("calculate", "").strip()
            if not expression:
                self.parent.speak("What would you like me to calculate?")
                expression = self.parent.take_command()

            if expression:
                # Simple calculation using eval (be careful with this in production)
                # Replace spoken math terms
                expression = expression.replace("plus", "+").replace("minus", "-")
                expression = expression.replace("times", "*").replace("divided by", "/")

                try:
                    result = eval(expression)
                    self.parent.speak(f"The result is {result}")
                except:
                    # Fallback to Wolfram Alpha
                    app_id = "X7RHRG-4JVEER92T2"
                    client = wolframalpha.Client(app_id)
                    res = client.query(expression)
                    answer = next(res.results).text
                    self.parent.speak(f"The result is {answer}")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't perform that calculation")
            logger.error(f"Calculation error: {str(e)}")

    # Other command handlers...
    def handle_reminder(self, command: str):
        """Handle setting reminders"""
        self.parent.speak("What should I remind you about?")
        reminder_text = self.parent.take_command()

        self.parent.speak("When should I remind you? Please say something like 'in 5 minutes' or 'at 3 PM'")
        time_input = self.parent.take_command()

        # Parse time input and set reminder
        # This is a simplified version - would need natural language processing for full implementation
        try:
            if 'minute' in time_input:
                minutes = int(time_input.split()[0])
                reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            elif 'hour' in time_input:
                hours = int(time_input.split()[0])
                reminder_time = datetime.datetime.now() + datetime.timedelta(hours=hours)
            else:
                # Try to parse absolute time
                try:
                    reminder_time = datetime.datetime.strptime(time_input, "%I %p")
                    now = datetime.datetime.now()
                    reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)
                    if reminder_time < now:
                        reminder_time += datetime.timedelta(days=1)
                except ValueError:
                    self.parent.speak("Sorry, I didn't understand the time. Please try again.")
                    return

            # Schedule reminder
            delay = (reminder_time - datetime.datetime.now()).total_seconds() * 1000
            QTimer.singleShot(int(delay), lambda: self.parent.speak(f"Reminder: {reminder_text}"))
            self.parent.speak(f"I'll remind you about {reminder_text} at {reminder_time.strftime('%I:%M %p')}")
        except Exception as e:
            self.parent.speak("Sorry, I couldn't set that reminder. Please try again.")
            logger.error(f"Error setting reminder: {str(e)}")


class SpeechWorker(QThread):
    """Worker thread for speech recognition"""
    recognized = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    listening_started = pyqtSignal()

    def __init__(self, timeout: int = 5, language: str = "en-US"):
        super().__init__()
        self.timeout = timeout
        self.language = language
        self._running = False

    def run(self):
        """Run speech recognition in separate thread"""
        self._running = True
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.listening_started.emit()
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=self.timeout, phrase_time_limit=self.timeout)

                if not self._running:
                    return

                try:
                    command = r.recognize_google(audio, language=self.language)
                    self.recognized.emit(command)
                    logger.info(f"Recognized command: {command}")
                except sr.UnknownValueError:
                    self.error_occurred.emit("Sorry, I didn't understand that.")
                    logger.warning("Speech recognition failed - unknown value")
                except sr.RequestError as e:
                    self.error_occurred.emit(f"Speech service error: {str(e)}")
                    logger.error(f"Speech recognition request failed: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Microphone error: {str(e)}")
            logger.error(f"Microphone error: {str(e)}")

    def stop(self):
        """Stop the speech recognition"""
        self._running = False
        self.quit()
        self.wait()


class TextToSpeech(QDialog):
    """Text to Speech dialog with advanced options"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Text to Speech')
        self.resize(600, 400)
        self.tts = TTSEngine()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Text input
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text to speak...")

        # Voice controls
        controls = QGridLayout()
        self.voice_combo = QComboBox(self)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.speed_slider.setRange(50, 300)
        self.speed_slider.setValue(self.tts.engine.getProperty('rate'))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.tts.engine.getProperty('volume') * 100))

        # Populate voice combo
        for i, voice in enumerate(self.tts.voices):
            self.voice_combo.addItem(voice.name, i)

        # Add controls to layout
        controls.addWidget(QLabel("Voice:"), 0, 0)
        controls.addWidget(self.voice_combo, 0, 1)
        controls.addWidget(QLabel("Speed:"), 1, 0)
        controls.addWidget(self.speed_slider, 1, 1)
        controls.addWidget(QLabel("Volume:"), 2, 0)
        controls.addWidget(self.volume_slider, 2, 1)

        # Buttons
        buttons = QHBoxLayout()
        self.speak_button = QPushButton("Speak", self)
        self.speak_button.clicked.connect(self.speak_text)
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_speech)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_speech)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.text_input.clear)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        buttons.addWidget(self.speak_button)
        buttons.addWidget(self.pause_button)
        buttons.addWidget(self.stop_button)
        buttons.addWidget(self.clear_button)
        buttons.addWidget(self.close_button)

        # Add all to main layout
        layout.addWidget(self.text_input)
        layout.addLayout(controls)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def speak_text(self):
        """Convert text to speech with current settings"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Input Needed", "Please enter some text to speak.")
            return

        try:
            voice_index = self.voice_combo.currentData()
            self.tts.engine.setProperty('voice', self.tts.voices[voice_index].id)
            self.tts.engine.setProperty('rate', self.speed_slider.value())
            self.tts.engine.setProperty('volume', self.volume_slider.value() / 100)

            self.tts.speak(text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to speak text: {str(e)}")
            logger.error(f"Error speaking text: {str(e)}")

    def pause_speech(self):
        """Pause the speech"""
        try:
            self.tts.engine.stop()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to pause speech: {str(e)}")
            logger.error(f"Error pausing speech: {str(e)}")

    def stop_speech(self):
        """Stop the speech"""
        try:
            self.tts.engine.stop()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to stop speech: {str(e)}")
            logger.error(f"Error stopping speech: {str(e)}")


class SpeechToText(QDialog):
    """Speech to Text dialog with advanced features"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Speech to Text')
        self.setMinimumSize(600, 500)
        self.settings = SettingsManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Speech to Text Converter")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Settings
        settings_group = QWidget()
        settings_layout = QGridLayout(settings_group)

        # Language selection
        self.language_combo = QComboBox()
        languages = {
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Italian": "it-IT",
            "Portuguese": "pt-PT",
            "Russian": "ru-RU",
            "Chinese": "zh-CN"
        }
        for lang, code in languages.items():
            self.language_combo.addItem(lang, code)

        # Set current language from settings
        current_lang = self.settings.settings.get('language', 'en-US')
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        # Timeout setting
        self.timeout_spin = QtWidgets.QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setValue(self.settings.settings.get('timeout', 5))

        # Audio source selection
        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItem("Default Microphone", "default")
        # Could add more audio sources here

        # Add settings to layout
        settings_layout.addWidget(QLabel("Language:"), 0, 0)
        settings_layout.addWidget(self.language_combo, 0, 1)
        settings_layout.addWidget(QLabel("Timeout (seconds):"), 1, 0)
        settings_layout.addWidget(self.timeout_spin, 1, 1)
        settings_layout.addWidget(QLabel("Audio Source:"), 2, 0)
        settings_layout.addWidget(self.audio_source_combo, 2, 1)

        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Recognized text will appear here...")

        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("color: green; font-weight: bold;")

        # Buttons
        buttons = QHBoxLayout()
        self.listen_btn = QPushButton("Start Listening")
        self.listen_btn.clicked.connect(self.start_listening)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_listening)
        self.stop_btn.setEnabled(False)
        self.save_btn = QPushButton("Save to File")
        self.save_btn.clicked.connect(self.save_to_file)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_text)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_text)

        buttons.addWidget(self.listen_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.copy_btn)
        buttons.addWidget(self.clear_btn)

        # Add all to main layout
        layout.addWidget(title)
        layout.addWidget(settings_group)
        layout.addWidget(QLabel("Recognized Text:"))
        layout.addWidget(self.output_text)
        layout.addWidget(self.status_bar)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def start_listening(self):
        """Start speech recognition"""
        language = self.language_combo.currentData()
        timeout = self.timeout_spin.value()

        # Save settings
        self.settings.update_setting('language', language)
        self.settings.update_setting('timeout', timeout)

        self.worker = SpeechWorker(timeout, language)
        self.worker.recognized.connect(self.on_recognized)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.listening_started.connect(self.on_listening_started)
        self.worker.finished.connect(self.on_finished)

        self.listen_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.worker.start()

    def stop_listening(self):
        """Stop speech recognition"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()

    def on_recognized(self, text: str):
        """Handle recognized text"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.append(f"[{timestamp}] {text}")
        self.status_bar.setText("Speech recognized successfully!")
        self.status_bar.setStyleSheet("color: green; font-weight: bold;")

    def on_error(self, error: str):
        """Handle recognition error"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.append(f"[{timestamp}] ERROR: {error}")
        self.status_bar.setText(error)
        self.status_bar.setStyleSheet("color: red; font-weight: bold;")

    def on_listening_started(self):
        """Update UI when listening starts"""
        self.status_bar.setText("Listening... Speak now!")
        self.status_bar.setStyleSheet("color: blue; font-weight: bold;")

    def on_finished(self):
        """Clean up when recognition finishes"""
        self.listen_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if "error" not in self.status_bar.text().lower():
            self.status_bar.setText("Ready")
            self.status_bar.setStyleSheet("color: green; font-weight: bold;")

    def save_to_file(self):
        """Save recognized text to file"""
        text = self.output_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "No text to save!")
            return

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Text", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Success", "Text saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                logger.error(f"Error saving file: {str(e)}")

    def copy_text(self):
        """Copy text to clipboard"""
        text = self.output_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_bar.setText("Text copied to clipboard!")
            self.status_bar.setStyleSheet("color: blue; font-weight: bold;")
            QTimer.singleShot(2000, lambda: self.status_bar.setText("Ready"))
        else:
            QMessageBox.warning(self, "Warning", "No text to copy!")

    def clear_text(self):
        """Clear the output text"""
        self.output_text.clear()
        self.status_bar.setText("Ready")
        self.status_bar.setStyleSheet("color: green; font-weight: bold;")


class VipOptions(QDialog):
    """VIP options dialog with advanced commands"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VIP Options")
        self.resize(800, 600)
        self.settings = SettingsManager()
        self.command_handler = CommandHandler(self)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Command list
        command_list = QWidget()
        command_layout = QVBoxLayout(command_list)

        self.command_list = QtWidgets.QListWidget()
        commands = [
            "Wikipedia Search - Say 'wikipedia [topic]'",
            "Open YouTube - Say 'open youtube'",
            "Open Google - Say 'open google'",
            "Check Time - Say 'what time is it'",
            "Take Photo - Say 'take a photo'",
            "Take Screenshot - Say 'take screenshot'",
            "Set Reminder - Say 'set reminder'",
            "Check Weather - Say 'what's the weather'",
            "Make Calculation - Say 'calculate [expression]'",
            "Write Note - Say 'write note'",
            "Show Note - Say 'show note'",
            "System Logout - Say 'logout'"
        ]
        self.command_list.addItems(commands)

        command_layout.addWidget(QLabel("Available Commands:"))
        command_layout.addWidget(self.command_list)

        # Console output
        console_group = QWidget()
        console_layout = QVBoxLayout(console_group)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.start_btn = QPushButton("Start Listening")
        self.start_btn.clicked.connect(self.start_listening)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_listening)
        self.stop_btn.setEnabled(False)

        console_layout.addWidget(QLabel("Console Output:"))
        console_layout.addWidget(self.console)
        console_layout.addWidget(self.start_btn)
        console_layout.addWidget(self.stop_btn)

        # Add to main layout
        layout.addWidget(command_list)
        layout.addWidget(console_group)
        self.setLayout(layout)

    def start_listening(self):
        """Start listening for commands"""
        self.worker = SpeechWorker(timeout=10, language=self.settings.settings.get('language', 'en-US'))
        self.worker.recognized.connect(self.handle_command)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log("Started listening for commands...")

    def stop_listening(self):
        """Stop listening for commands"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log("Stopped listening for commands")

    def handle_command(self, command: str):
        """Handle recognized command"""
        self.log(f"Command: {command}")

        if not self.command_handler.execute_command(command):
            self.log("Command not recognized")
            self.speak("Sorry, I didn't understand that command.")

    def on_error(self, error: str):
        """Handle recognition error"""
        self.log(f"Error: {error}")

    def log(self, message: str):
        """Log message to console"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")

    def speak(self, text: str):
        """Speak text using TTS"""
        try:
            tts = TTSEngine()
            tts.speak(text)
            self.log(f"Assistant: {text}")
        except Exception as e:
            self.log(f"Error speaking: {str(e)}")


class AIAssistant(QMainWindow, Ui_MainWindow):
    """Main AI Assistant application window"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('AI Assistant')
        self.setFixedSize(800, 600)

        # Initialize components
        self.settings = SettingsManager()
        self.tts = TTSEngine()
        self.command_handler = CommandHandler(self)

        # Setup UI
        self.setup_ui()

        # System tray
        self.setup_system_tray()

        # Voice recognition
        self.speech_worker = None
        self.is_listening = False

    def setup_ui(self):
        """Initialize the user interface"""
        # Set initial voice
        self.comboBox.clear()
        for i, voice in enumerate(self.tts.voices):
            self.comboBox.addItem(voice.name)

        # Connect signals
        self.btn_1.clicked.connect(self.greet_user)
        self.btn_2.clicked.connect(self.open_text_to_speech)
        self.btn_3.clicked.connect(self.open_speech_to_text)
        self.btn_4.clicked.connect(self.open_vip_options)
        self.btn_5.clicked.connect(self.close)
        self.comboBox.currentIndexChanged.connect(self.change_voice)

        # Set initial state
        self.textEdit_1.setReadOnly(True)

        # Load user name if exists
        if self.settings.settings.get('user_name'):
            self.textEdit_1.append(f"Welcome back {self.settings.settings['user_name']}!")

    def setup_system_tray(self):
        """Setup system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(":/icons/assistant.png"))  # Replace with your icon

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)

        listen_action = tray_menu.addAction("Start Listening")
        listen_action.triggered.connect(self.start_listening)

        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()

    def change_voice(self, index):
        """Change TTS voice"""
        if 0 <= index < len(self.tts.voices):
            self.tts.engine.setProperty('voice', self.tts.voices[index].id)
            self.settings.update_setting('voice', index)

    def greet_user(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour

        if 0 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        if self.settings.settings.get('user_name'):
            self.speak(f"{greeting}, {self.settings.settings['user_name']}! How can I help you today?")
        else:
            self.speak(f"{greeting}! What is your name?")
            self.get_user_name()

    def get_user_name(self):
        """Get user's name via voice input"""
        name = self.take_command()
        if name and name.lower() != "none":
            self.settings.update_setting('user_name', name)
            self.speak(f"Welcome {name}! How can I help you today?")

    def speak(self, text: str):
        """Speak text and display in UI"""
        self.textEdit_1.append(f"Assistant: {text}")
        self.tts.speak(text)

    def take_command(self) -> Optional[str]:
        """Take voice command from user"""
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.textEdit_1.append("Listening...")
                QApplication.processEvents()

                audio = r.listen(source, timeout=5, phrase_time_limit=5)

                try:
                    command = r.recognize_google(audio, language=self.settings.settings.get('language', 'en-US'))
                    self.textEdit_1.append(f"You: {command}")
                    return command.lower()
                except sr.UnknownValueError:
                    self.speak("Sorry, I didn't understand that.")
                except sr.RequestError:
                    self.speak("Sorry, my speech service is down.")
        except Exception as e:
            self.textEdit_1.append(f"Error: {str(e)}")
            logger.error(f"Error taking command: {str(e)}")

        return None

    def start_listening(self):
        """Start continuous listening for commands"""
        if self.is_listening:
            return

        self.is_listening = True
        self.speech_worker = SpeechWorker(timeout=10, language=self.settings.settings.get('language', 'en-US'))
        self.speech_worker.recognized.connect(self.handle_command)
        self.speech_worker.error_occurred.connect(self.on_listening_error)
        self.speech_worker.start()

        self.textEdit_1.append("Started listening for commands...")

    def stop_listening(self):
        """Stop continuous listening"""
        if not self.is_listening:
            return

        self.is_listening = False
        if self.speech_worker:
            self.speech_worker.stop()

        self.textEdit_1.append("Stopped listening for commands")

    def handle_command(self, command: str):
        """Handle recognized command"""
        self.textEdit_1.append(f"Command: {command}")
        self.command_handler.execute_command(command)

    def on_listening_error(self, error: str):
        """Handle listening error"""
        self.textEdit_1.append(f"Error: {error}")

    def open_text_to_speech(self):
        """Open Text to Speech dialog"""
        try:
            dialog = TextToSpeech(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Text to Speech: {str(e)}")
            logger.error(f"Error opening Text to Speech: {str(e)}")

    def open_speech_to_text(self):
        """Open Speech to Text dialog"""
        try:
            dialog = SpeechToText(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Speech to Text: {str(e)}")
            logger.error(f"Error opening Speech to Text: {str(e)}")

    def open_vip_options(self):
        """Open VIP Options dialog"""
        try:
            dialog = VipOptions(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open VIP Options: {str(e)}")
            logger.error(f"Error opening VIP Options: {str(e)}")

    def closeEvent(self, event):
        """Handle window close event"""
        self.stop_listening()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create and show main window
    assistant = AIAssistant()
    assistant.show()

    sys.exit(app.exec())