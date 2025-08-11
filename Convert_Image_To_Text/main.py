import sys
import os
from pathlib import Path
from typing import override, Optional
import logging

from PIL import Image
import pytesseract

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QLinearGradient, QPainter, QBrush
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, 
    QTextEdit, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QMessageBox, QProgressBar, QComboBox, QSplitter, QGroupBox,
    QScrollArea, QFrame, QGraphicsDropShadowEffect
)
from deep_translator import GoogleTranslator
from convert import Ui_MainWindow

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Modern styling constants
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'accent': '#F18F01',
    'success': '#06FFA5',
    'warning': '#FFD23F',
    'danger': '#FF3366',
    'dark': '#1A1A2E',
    'light': '#F8F9FA',
    'gray': '#6C757D',
    'white': '#FFFFFF'
}

def get_modern_button_style(color='primary', hover_color=None, pressed_color=None):
    """Generate modern button stylesheet."""
    base_color = COLORS.get(color, COLORS['primary'])
    hover = hover_color or lighten_color(base_color, 20)
    pressed = pressed_color or darken_color(base_color, 20)
    
    return f"""
    QPushButton {{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 {base_color}, stop: 1 {darken_color(base_color, 10)});
        border: 2px solid {base_color};
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 11px;
        padding: 8px 16px;
        min-height: 16px;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 {hover}, stop: 1 {base_color});
        border: 2px solid {hover};
    }}
    QPushButton:pressed {{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 {pressed}, stop: 1 {darken_color(pressed, 10)});
        border: 2px solid {pressed};
    }}
    QPushButton:disabled {{
        background: #CCCCCC;
        border: 2px solid #CCCCCC;
        color: #666666;
    }}
    """

def get_modern_textedit_style():
    """Generate modern text edit stylesheet."""
    return """
    QTextEdit {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        background-color: #FAFAFA;
        color: #1A1A2E;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11px;
        padding: 8px;
        selection-background-color: #2E86AB;
        selection-color: white;
    }
    QTextEdit:focus {
        border: 2px solid #2E86AB;
        background-color: white;
        color: #1A1A2E;
    }
    """

def get_modern_combobox_style():
    """Generate modern combobox stylesheet."""
    return """
    QComboBox {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        background-color: white;
        color: #1A1A2E;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11px;
        padding: 6px 12px;
        min-height: 20px;
    }
    QComboBox:focus {
        border: 2px solid #2E86AB;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #666666;
        margin-right: 5px;
    }
    QComboBox QAbstractItemView {
        border: 2px solid #E0E0E0;
        background-color: white;
        color: #1A1A2E;
        selection-background-color: #2E86AB;
        selection-color: white;
    }
    """

def get_modern_progressbar_style():
    """Generate modern progress bar stylesheet."""
    return """
    QProgressBar {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        background-color: #F0F0F0;
        text-align: center;
        font-weight: bold;
        color: #333333;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #06FFA5, stop: 1 #2E86AB);
        border-radius: 6px;
    }
    """

def get_modern_label_style(size='medium', color='dark'):
    """Generate modern label stylesheet."""
    sizes = {'small': '10px', 'medium': '12px', 'large': '14px', 'xlarge': '16px'}
    font_size = sizes.get(size, '12px')
    text_color = COLORS.get(color, COLORS['dark'])
    
    return f"""
    QLabel {{
        color: {text_color};
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: {font_size};
        font-weight: 500;
    }}
    """

def get_dialog_style():
    """Generate modern dialog stylesheet."""
    return """
    QDialog {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #FFFFFF, stop: 1 #F8F9FA);
        border: 1px solid #E0E0E0;
    }
    """

def lighten_color(hex_color, percent):
    """Lighten a hex color by a percentage."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(min(255, int(c + (255 - c) * percent / 100)) for c in rgb)
    return f"#{''.join(f'{c:02x}' for c in rgb)}"

def darken_color(hex_color, percent):
    """Darken a hex color by a percentage."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
    return f"#{''.join(f'{c:02x}' for c in rgb)}"

def apply_shadow_effect(widget, blur_radius=10, offset_x=0, offset_y=2, color=QColor(0, 0, 0, 60)):
    """Apply drop shadow effect to widget."""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(offset_x)
    shadow.setYOffset(offset_y)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)

# Configure Tesseract path with better error handling
def configure_tesseract():
    """Configure Tesseract OCR path with multiple fallback locations."""
    possible_paths = [
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{username}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(
            username=os.getenv('USERNAME', '')
        ),
        "tesseract"  # If tesseract is in PATH
    ]
    
    for path in possible_paths:
        if path == "tesseract" or (Path(path).exists() if path != "tesseract" else False):
            pytesseract.pytesseract.tesseract_cmd = path
            logger.info(f"Tesseract configured at: {path}")
            return True
    
    logger.error("Tesseract not found. Please install Tesseract OCR.")
    return False

# Worker thread for OCR processing
class OCRWorker(QThread):
    """Worker thread to perform OCR in the background to prevent UI freezing."""
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    
    def __init__(self, image_path, lang="eng"):
        super().__init__()
        self.image_path = image_path
        self.lang = lang
        
    def run(self):
        try:
            if not self.image_path:
                self.error.emit("No image selected")
                return
                
            self.progress.emit(10)
            # Open image
            img = Image.open(self.image_path)
            self.progress.emit(30)
            
            # Perform OCR
            text = pytesseract.image_to_string(img, lang=self.lang)
            self.progress.emit(90)
            
            # Emit results
            self.finished.emit(text)
            self.progress.emit(100)
        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}")
            self.error.emit(f"Error processing image: {str(e)}")


class TranslationWorker(QThread):
    """Worker thread to perform translation in the background."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, text, source='en', target='fa'):
        super().__init__()
        self.text = text
        self.source = source
        self.target = target
        
    def run(self):
        try:
            if not self.text.strip():
                self.error.emit("No text to translate")
                return
                
            translated = GoogleTranslator(source=self.source, target=self.target).translate(self.text)
            self.finished.emit(translated)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            self.error.emit(f"Error during translation: {str(e)}")


class BaseConvertDialog(QDialog):
    """Base dialog class for image conversion functionality."""
    def __init__(self, title, placeholder_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(700, 600)  # Larger default size
        self.setModal(True)
        
        # Apply modern dialog styling
        self.setStyleSheet(get_dialog_style())
        
        # Main layout with proper spacing
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title label
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(get_modern_label_style('xlarge', 'primary'))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # Image preview section with frame
        self.preview_frame = QFrame()
        self.preview_frame.setFrameStyle(QFrame.Shape.Box)
        self.preview_frame.setLineWidth(1)
        self.preview_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #CCCCCC;
                border-radius: 12px;
                background-color: #F8F9FA;
                min-height: 180px;
                margin: 10px;
            }
        """)
        
        self.preview_layout = QVBoxLayout(self.preview_frame)
        self.image_label = QLabel("📁 Drop an image here or click Upload")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(150)
        self.image_label.setStyleSheet(get_modern_label_style('medium', 'gray'))
        
        # Add shadow effect to image preview
        apply_shadow_effect(self.preview_frame, blur_radius=8)
        
        self.preview_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.preview_frame)
        
        # Text output section
        self.output_label = QLabel("Extracted Text:")
        self.output_label.setStyleSheet(get_modern_label_style('medium', 'dark'))
        self.main_layout.addWidget(self.output_label)
        
        self.out_put_text = QTextEdit()
        self.out_put_text.setReadOnly(True)
        self.out_put_text.setPlaceholderText(placeholder_text)
        self.out_put_text.setStyleSheet(get_modern_textedit_style())
        self.out_put_text.setMinimumHeight(180)
        
        # Add shadow effect to text edit
        apply_shadow_effect(self.out_put_text, blur_radius=5)
        
        self.main_layout.addWidget(self.out_put_text)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(get_modern_progressbar_style())
        self.progress_bar.setMinimumHeight(25)
        self.main_layout.addWidget(self.progress_bar)
        
        # Button layout with proper spacing
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(12)
        
        # Buttons with modern styling
        self.btn_upload = QPushButton('📤 Upload Image')
        self.btn_upload.setStyleSheet(get_modern_button_style('primary'))
        self.btn_upload.clicked.connect(self.upload_image)
        apply_shadow_effect(self.btn_upload, blur_radius=5)
        
        self.btn_process = QPushButton('⚡ Process')
        self.btn_process.setStyleSheet(get_modern_button_style('success'))
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)  # Disabled until image is uploaded
        apply_shadow_effect(self.btn_process, blur_radius=5)
        
        self.btn_copy = QPushButton('📋 Copy Text')
        self.btn_copy.setStyleSheet(get_modern_button_style('accent'))
        self.btn_copy.clicked.connect(self.copy_text)
        apply_shadow_effect(self.btn_copy, blur_radius=5)
        
        self.btn_save = QPushButton('💾 Save Text')
        self.btn_save.setStyleSheet(get_modern_button_style('secondary'))
        self.btn_save.clicked.connect(self.save_text)
        apply_shadow_effect(self.btn_save, blur_radius=5)
        
        self.btn_exit = QPushButton('❌ Close')
        self.btn_exit.setStyleSheet(get_modern_button_style('danger'))
        self.btn_exit.clicked.connect(self.close)
        apply_shadow_effect(self.btn_exit, blur_radius=5)
        
        # Add buttons to layout
        self.button_layout.addWidget(self.btn_upload)
        self.button_layout.addWidget(self.btn_process)
        self.button_layout.addWidget(self.btn_copy)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addWidget(self.btn_exit)
        
        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)
        
        # Set dialog layout
        self.setLayout(self.main_layout)
        
        # Class variables
        self.text = ''
        self.image_path = ''
        self.worker = None

    def upload_image(self):
        """Open file dialog to select an image."""
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Image files (*.png *.jpg *.jpeg *.bmp *.gif)"])
        file_dialog.selectNameFilter("Image files (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if file_dialog.exec():
            self.image_path = file_dialog.selectedFiles()[0]
            self.display_image_preview()
            logger.info(f"Image uploaded: {self.image_path}")
            
            # Enable process button once an image is uploaded
            self.btn_process.setEnabled(True)
        
    def display_image_preview(self):
        """Display a preview of the selected image."""
        if not self.image_path:
            return
            
        try:
            pixmap = QPixmap(self.image_path)
            
            # Scale the pixmap to fit the label while maintaining aspect ratio
            max_size = QSize(400, 150)
            scaled_pixmap = pixmap.scaled(
                max_size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            logger.error(f"Error displaying image preview: {str(e)}")
            self.image_label.setText("Error loading image preview")
    
    def process_image(self):
        """Process the image - to be implemented by subclasses."""
        pass
    
    def copy_text(self):
        """Copy text to clipboard."""
        text = self.out_put_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Copied", "Text copied to clipboard")
        else:
            QMessageBox.warning(self, "Warning", "No text to copy")
    
    def save_text(self):
        """Save extracted text to a file."""
        text = self.out_put_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "No text to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Text", 
            os.path.expanduser("~/Documents"),
            "Text files (*.txt);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Saved", f"Text saved to {file_path}")
            except Exception as e:
                logger.error(f"Error saving text: {str(e)}")
                QMessageBox.critical(self, "Error", f"Could not save the file: {str(e)}")

    def handle_ocr_finished(self, text):
        """Handle OCR completion."""
        self.text = text
        self.out_put_text.setText(text)
        self.progress_bar.setVisible(False)
        
    def handle_ocr_error(self, error_message):
        """Handle OCR errors."""
        QMessageBox.critical(self, "Error", error_message)
        self.progress_bar.setVisible(False)
        
    def handle_progress(self, value):
        """Update progress bar."""
        self.progress_bar.setValue(value)


class PersianConvertDialog(BaseConvertDialog):
    """Dialog for converting images to Persian text."""
    def __init__(self, parent=None):
        super().__init__(
            title='Convert Image to Text - Persian',
            placeholder_text='Persian text will appear here after processing',
            parent=parent
        )
        self.btn_process.setText("Convert to Persian Text")
    
    def process_image(self):
        """Process the image with Persian OCR."""
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "Please upload an image first")
            return
            
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        self.worker = OCRWorker(self.image_path, lang="fas")
        self.worker.finished.connect(self.handle_ocr_finished)
        self.worker.error.connect(self.handle_ocr_error)
        self.worker.progress.connect(self.handle_progress)
        self.worker.start()


class EnglishConvertDialog(BaseConvertDialog):
    """Dialog for converting images to English text."""
    def __init__(self, parent=None):
        super().__init__(
            title='Convert Image to Text - English',
            placeholder_text='English text will appear here after processing',
            parent=parent
        )
        self.btn_process.setText("Convert to English Text")
    
    def process_image(self):
        """Process the image with English OCR."""
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "Please upload an image first")
            return
            
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        self.worker = OCRWorker(self.image_path, lang="eng")
        self.worker.finished.connect(self.handle_ocr_finished)
        self.worker.error.connect(self.handle_ocr_error)
        self.worker.progress.connect(self.handle_progress)
        self.worker.start()


class TranslateImageDialog(BaseConvertDialog):
    """Dialog for translating images from English to Persian."""
    def __init__(self, parent=None):
        super().__init__(
            title='Translate Image: English → Persian',
            placeholder_text='Translated text will appear here after processing',
            parent=parent
        )
        self.btn_process.setText("Translate")
        
        # Language selection section
        self.lang_group = QGroupBox("🌐 Language Selection")
        self.lang_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2E86AB;
            }
        """)
        
        self.lang_layout = QHBoxLayout(self.lang_group)
        self.lang_layout.setSpacing(15)
        
        # From language
        self.from_label = QLabel("From:")
        self.from_label.setStyleSheet(get_modern_label_style('medium', 'dark'))
        self.from_lang_combo = QComboBox()
        self.from_lang_combo.setStyleSheet(get_modern_combobox_style())
        
        # Arrow label
        self.arrow_label = QLabel("→")
        self.arrow_label.setStyleSheet("""QLabel { 
            color: #2E86AB; 
            font-size: 18px; 
            font-weight: bold;
        }""")
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # To language
        self.to_label = QLabel("To:")
        self.to_label.setStyleSheet(get_modern_label_style('medium', 'dark'))
        self.to_lang_combo = QComboBox()
        self.to_lang_combo.setStyleSheet(get_modern_combobox_style())
        
        # Add languages with emojis
        languages = {
            'en': '🇺🇸 English',
            'fa': '🇮🇷 Persian',
            'ar': '🇸🇦 Arabic',
            'fr': '🇫🇷 French',
            'de': '🇩🇪 German',
            'es': '🇪🇸 Spanish',
            'ru': '🇷🇺 Russian',
            'zh-CN': '🇨🇳 Chinese (Simplified)',
            'ja': '🇯🇵 Japanese'
        }
        
        for code, name in languages.items():
            self.from_lang_combo.addItem(name, code)
            self.to_lang_combo.addItem(name, code)
        
        # Set defaults
        self.from_lang_combo.setCurrentText('🇺🇸 English')
        self.to_lang_combo.setCurrentText('🇮🇷 Persian')
        
        # Add to layout
        self.lang_layout.addWidget(self.from_label)
        self.lang_layout.addWidget(self.from_lang_combo)
        self.lang_layout.addWidget(self.arrow_label)
        self.lang_layout.addWidget(self.to_label)
        self.lang_layout.addWidget(self.to_lang_combo)
        
        # Add shadow effect to language group
        apply_shadow_effect(self.lang_group, blur_radius=6)
        
        # Insert language selection layout after title, before preview
        self.main_layout.insertWidget(1, self.lang_group)
        
        # OCR Results
        self.ocr_results = ""
        
    def process_image(self):
        """Process the image with OCR and translation."""
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "Please upload an image first")
            return
            
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Get language selection
        source_lang = self.from_lang_combo.currentData()
        target_lang = self.to_lang_combo.currentData()
        
        # Determine OCR language based on source language
        ocr_lang_map = {
            'en': 'eng',
            'fa': 'fas',
            'ar': 'ara',
            'fr': 'fra',
            'de': 'deu',
            'es': 'spa',
            'ru': 'rus',
            'zh-CN': 'chi_sim',
            'ja': 'jpn'
        }
        ocr_lang = ocr_lang_map.get(source_lang, 'eng')
        
        # Create and start OCR worker
        self.worker = OCRWorker(self.image_path, lang=ocr_lang)
        self.worker.finished.connect(self.handle_ocr_finished)
        self.worker.error.connect(self.handle_ocr_error)
        self.worker.progress.connect(self.handle_progress)
        self.worker.start()
    
    def handle_ocr_finished(self, text):
        """Handle OCR completion and start translation."""
        self.ocr_results = text
        
        # Update progress to show OCR is done
        self.progress_bar.setValue(50)
        
        # Start translation
        source_lang = self.from_lang_combo.currentData()
        target_lang = self.to_lang_combo.currentData()
        
        # Create and start translation worker
        self.translation_worker = TranslationWorker(text, source=source_lang, target=target_lang)
        self.translation_worker.finished.connect(self.handle_translation_finished)
        self.translation_worker.error.connect(self.handle_translation_error)
        self.translation_worker.start()
    
    def handle_translation_finished(self, translated_text):
        """Handle translation completion."""
        output = f"Original Text:\n{self.ocr_results}\n\n{'=' * 40}\n\nTranslated Text:\n{translated_text}"
        self.text = output
        self.out_put_text.setText(output)
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
    
    def handle_translation_error(self, error_message):
        """Handle translation errors."""
        QMessageBox.critical(self, "Translation Error", error_message)
        # Still show OCR results even if translation failed
        self.out_put_text.setText(f"Original Text:\n{self.ocr_results}\n\n{'=' * 40}\n\nTranslation failed: {error_message}")
        self.progress_bar.setVisible(False)


def get_main_window_style():
    """Generate modern main window stylesheet."""
    return f"""
    QMainWindow {{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 {COLORS['white']}, stop: 1 {COLORS['light']});
    }}
    QWidget {{
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    """

class MainWindow(QMainWindow, Ui_MainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle('✨ Image Text Processor')
        
        # Apply modern styling to the main window
        self.setStyleSheet(get_main_window_style())
        
        # Try to load icon
        try:
            self.setWindowIcon(QIcon('icon.ico'))
        except:
            logger.warning("Could not load application icon")
        
        self.setFixedSize(420, 470)
        # self.resize(500, 600)
        
        # Apply modern styling to buttons
        self.style_main_buttons()
        
        # Style the main label
        if hasattr(self, 'label_1'):
            self.label_1.setStyleSheet(get_modern_label_style('xlarge', 'primary'))
            self.label_1.setText('🚀 Image Text Processor')
        
        # Connect buttons
        self.btn_1.clicked.connect(self.convert_persian)
        self.btn_2.clicked.connect(self.convert_english)
        self.btn_3.clicked.connect(self.translate_image)
        self.btn_4.clicked.connect(self.close)
        
        # Initialize about dialog
        self.actionconvert_and_translate_image.triggered.connect(self.show_about)
        
        # Check Tesseract installation
        if not configure_tesseract():
            QMessageBox.warning(
                self,
                "Tesseract Not Found",
                "Tesseract OCR was not found on your system. Please install it to use this application."
            )
    
    def style_main_buttons(self):
        """Apply modern styling to main window buttons."""
        button_configs = [
            (self.btn_1, '🇮🇷 Convert to Persian', 'primary'),
            (self.btn_2, '🇺🇸 Convert to English', 'success'),
            (self.btn_3, '🌐 Translate Image', 'accent'),
            (self.btn_4, '🚪 Exit', 'danger')
        ]
        
        for button, text, color in button_configs:
            button.setText(text)
            button.setStyleSheet(get_modern_button_style(color))
            button.setMinimumHeight(45)
            button.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
            
            # Add shadow effects
            apply_shadow_effect(button, blur_radius=8, offset_y=3)
    
    def convert_persian(self):
        """Open Persian OCR dialog."""
        dialog = PersianConvertDialog(self)
        dialog.exec()
    
    def convert_english(self):
        """Open English OCR dialog."""
        dialog = EnglishConvertDialog(self)
        dialog.exec()
    
    def translate_image(self):
        """Open translation dialog."""
        dialog = TranslateImageDialog(self)
        dialog.exec()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Image Text Processor",
            "<h2>Image Text Processor</h2>"
            "<p>Version 1.0</p>"
            "<p>An application for extracting text from images using OCR "
            "and translating between languages.</p>"
            "<p>Uses Tesseract OCR engine and Google Translate API.</p>"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
