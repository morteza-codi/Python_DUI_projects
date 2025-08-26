"""
Main Window module for the Password Generator application.

Contains the main application window.
"""

from PyQt6.QtWidgets import QApplication, QMenu, QMenuBar, QComboBox, QLabel, QStatusBar, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from password_generator.ui.base import BaseWindow
from password_generator.ui.generated import Ui_Form
from password_generator.ui.styles import StyleManager
from password_generator.core.generator import (
    DifficultyPasswordGenerator,
    CustomLengthPasswordGenerator,
    CustomCharSetPasswordGenerator
)
from password_generator.utils.threads import PasswordWorkerThread
from password_generator.utils.config import Config
from password_generator.utils.password_strength import evaluate_password_strength


class MainWindow(BaseWindow, Ui_Form):
    """Main application window for the Password Generator."""
    
    def __init__(self):
        """Initialize the main window and setup the UI."""
        super().__init__(title=Config.APP_NAME, width=Config.DEFAULT_WIDTH, height=Config.DEFAULT_HEIGHT + 40)  # Add height for menu bar
        
        # Setup menu bar first
        self.setup_menu()
        
        # Setup UI
        self.setupUi(self)
        
        # Adjust frame positions to account for menu bar
        self.adjust_frame_positions()
        
        # Setup styles and UI improvements
        self.setup_styles()
        
        # Setup predefined character sets combobox
        self.setup_char_sets()
        
        # Setup password strength indicators
        self.setup_strength_indicators()
        
        # Connect button signals to slots
        self.connect_signals()
        
        # Initialize threading
        self.worker = None
        
        # Create status bar
        status_bar = QStatusBar()
        status_bar.setStyleSheet(StyleManager.get_status_bar_style())
        self.setStatusBar(status_bar)
        self.show_status_message("آماده به کار")
        
        # Show the window
        self.show()
        
    def adjust_frame_positions(self):
        """Adjust frame positions to account for menu bar."""
        # Move frames down to make room for menu bar
        menu_height = 40
        self.frame.move(self.frame.x(), self.frame.y() + menu_height)
        self.frame_2.move(self.frame_2.x(), self.frame_2.y() + menu_height)
        self.frame_3.move(self.frame_3.x(), self.frame_3.y() + menu_height)
        
    def setup_strength_indicators(self):
        """Setup password strength indicators for each generated password."""
        # Create strength progress bars and labels
        self.create_strength_indicator(self.frame, 500, "strength_1", self.textEdit_1)
        self.create_strength_indicator(self.frame_2, 500, "strength_2", self.textEdit_2)
        self.create_strength_indicator(self.frame_3, 550, "strength_3", self.textEdit_4)
        
    def create_strength_indicator(self, parent, y_pos, name, text_edit):
        """Create password strength indicator (progress bar and label).
        
        Args:
            parent (QWidget): Parent widget
            y_pos (int): Y position
            name (str): Base name for widgets
            text_edit (QTextEdit): Text edit to monitor
        """
        # Create label
        label = QLabel("قدرت رمز:", parent)
        label.setGeometry(240, y_pos, 70, 20)
        label.setStyleSheet(StyleManager.get_regular_label_style())
        setattr(self, f"{name}_label", label)
        
        # Create progress bar
        progress = QProgressBar(parent)
        progress.setGeometry(30, y_pos, 200, 20)
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setTextVisible(False)
        progress.setStyleSheet(StyleManager.get_progress_bar_style())
        setattr(self, f"{name}_bar", progress)
        
        # Create rating label
        rating = QLabel("", parent)
        rating.setGeometry(20, y_pos, 80, 20)
        rating.setStyleSheet(StyleManager.get_regular_label_style())
        rating.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setattr(self, f"{name}_rating", rating)
        
        # Connect text edit's textChanged signal to update strength
        text_edit.textChanged.connect(lambda: self.update_password_strength(text_edit, name))
        
    def setup_menu(self):
        """Setup the application menu bar."""
        # Create menu bar with fixed height
        self.menuBar = QMenuBar(self)
        self.menuBar.setFixedHeight(40)
        self.menuBar.setStyleSheet(StyleManager.get_menu_bar_style())
        self.setMenuBar(self.menuBar)
        
        # Set right-to-left layout for the entire menu bar
        self.menuBar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Create menus with larger font and padding
        file_menu = QMenu("فایل", self)
        file_menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        file_menu.setFont(self.font())
        
        help_menu = QMenu("راهنما", self)
        help_menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        help_menu.setFont(self.font())
        
        # Add menus to the menubar - add in reverse order for RTL layout
        self.menuBar.addMenu(help_menu)
        self.menuBar.addMenu(file_menu)
        
        # Add actions to File menu
        exit_action = file_menu.addAction("خروج")
        exit_action.triggered.connect(self.close)
        
        # Add actions to Help menu
        about_action = help_menu.addAction("درباره برنامه")
        about_action.triggered.connect(self.show_about)
        
        # Make sure the menu bar is visible and has focus
        self.menuBar.show()
        self.menuBar.setFocus()
        
    def setup_char_sets(self):
        """Setup the predefined character sets dropdown."""
        # Create a label for predefined sets
        self.label_preset = QLabel("مجموعه‌های آماده:", self.frame_3)
        self.label_preset.setGeometry(150, 90, 161, 31)
        self.label_preset.setStyleSheet(StyleManager.get_regular_label_style())
        
        # Create a combobox
        self.combo_presets = QComboBox(self.frame_3)
        self.combo_presets.setGeometry(20, 90, 120, 41)
        self.combo_presets.setStyleSheet(StyleManager.get_combo_box_style())
        
        # Add items
        for preset in Config.PREDEFINED_CHAR_SETS:
            self.combo_presets.addItem(preset)
            
        # Connect signal
        self.combo_presets.currentTextChanged.connect(self.preset_selected)
        
    def preset_selected(self, preset_name):
        """Handle selection of a predefined character set.
        
        Args:
            preset_name (str): Name of the selected preset
        """
        if preset_name in Config.PREDEFINED_CHAR_SETS:
            self.textEdit_3.setText(Config.PREDEFINED_CHAR_SETS[preset_name])
            self.show_status_message(f"مجموعه '{preset_name}' انتخاب شد")
            
    def show_about(self):
        """Show about dialog."""
        about_text = f"{Config.APP_NAME} نسخه {Config.APP_VERSION}\n\n"
        about_text += "یک برنامه مدرن برای تولید رمزهای عبور امن\n\n"
        about_text += "نویسنده: Mory"
        
        self.show_info_message(about_text, "درباره برنامه")

    def setup_styles(self):
        """Apply styling to all UI elements."""
        # Set main window background
        self.setStyleSheet(StyleManager.get_main_window_style())
        
        # Style frames with gold borders
        frame_style = StyleManager.get_frame_style()
        self.frame.setStyleSheet(frame_style)
        self.frame_2.setStyleSheet(frame_style)
        self.frame_3.setStyleSheet(frame_style)
        
        # Style title labels with better visibility
        title_style = StyleManager.get_title_label_style()
        self.label.setStyleSheet(title_style)
        self.label_2.setStyleSheet(title_style)
        self.label_3.setStyleSheet(title_style)
        
        # Set title texts
        self.label.setText("تولید کد اختصاصی")
        self.label_2.setText("تولید رمز با طول دلخواه")
        self.label_3.setText("تولید رمز با سطح سختی")
        
        # Style regular labels
        label_style = StyleManager.get_regular_label_style()
        self.label_4.setStyleSheet(label_style)
        self.label_9.setStyleSheet(label_style)
        self.label_10.setStyleSheet(label_style)
        self.label_12.setStyleSheet(label_style)
        
        # Style text fields for much better visibility
        text_style = StyleManager.get_text_edit_style()
        self.textEdit_1.setStyleSheet(text_style)
        self.textEdit_2.setStyleSheet(text_style)
        self.textEdit_3.setStyleSheet(text_style)
        self.textEdit_4.setStyleSheet(text_style)
        
        # Add placeholder text
        self.textEdit_1.setPlaceholderText("رمز عبور تولید شده...")
        self.textEdit_2.setPlaceholderText("رمز عبور تولید شده...")
        self.textEdit_3.setPlaceholderText("کاراکترهای دلخواه را وارد کنید")
        self.textEdit_4.setPlaceholderText("رمز عبور تولید شده...")
        
        # Style "Generate" buttons with green color
        generate_style = StyleManager.get_generate_button_style()
        self.generat_1.setStyleSheet(generate_style)
        self.generat_3.setStyleSheet(generate_style)
        self.generat_5.setStyleSheet(generate_style)
        
        # Style "Copy" buttons with orange color
        copy_style = StyleManager.get_copy_button_style()
        self.generat_2.setStyleSheet(copy_style)
        self.generat_4.setStyleSheet(copy_style)
        self.generat_6.setStyleSheet(copy_style)
        
        # Style combo box
        self.comboBox.setStyleSheet(StyleManager.get_combo_box_style())
        
        # Style spinboxes
        spinbox_style = StyleManager.get_spin_box_style()
        self.spinBox_1.setStyleSheet(spinbox_style)
        self.spinBox_2.setStyleSheet(spinbox_style)
        
        # Set default values for spinboxes
        self.spinBox_1.setMinimum(Config.MIN_PASSWORD_LENGTH)
        self.spinBox_1.setMaximum(Config.MAX_PASSWORD_LENGTH)
        self.spinBox_1.setValue(Config.DEFAULT_PASSWORD_LENGTH)
        
        self.spinBox_2.setMinimum(Config.MIN_PASSWORD_LENGTH)
        self.spinBox_2.setMaximum(Config.MAX_PASSWORD_LENGTH)
        self.spinBox_2.setValue(Config.DEFAULT_PASSWORD_LENGTH)
        
        # Set default combo box selection
        index = self.comboBox.findText(Config.DEFAULT_DIFFICULTY)
        if index >= 0:
            self.comboBox.setCurrentIndex(index)

    def connect_signals(self):
        """Connect all button signals to their corresponding slots."""
        # Connect copy buttons
        self.generat_2.clicked.connect(self.copy_text_1)
        self.generat_4.clicked.connect(self.copy_text_2)
        self.generat_6.clicked.connect(self.copy_text_3)
        
        # Connect generate buttons
        self.generat_1.clicked.connect(self.generate_passed_1)
        self.generat_3.clicked.connect(self.generate_passed_2)
        
        # Use the animated generation for custom character sets
        self.generat_5.clicked.connect(self.signal)

    def copy_text_1(self):
        """Copy content of first text field to clipboard."""
        self.copy_to_clipboard(self.textEdit_1.toPlainText())

    def copy_text_2(self):
        """Copy content of second text field to clipboard."""
        self.copy_to_clipboard(self.textEdit_2.toPlainText())

    def copy_text_3(self):
        """Copy content of third text field to clipboard."""
        self.copy_to_clipboard(self.textEdit_4.toPlainText())

    def generate_passed_1(self):
        """Generate password based on selected difficulty level."""
        try:
            difficulty = self.comboBox.currentText()
            
            # Create generator and generate password
            generator = DifficultyPasswordGenerator(difficulty)
            password = generator.generate()
            
            # Update UI
            self.textEdit_1.setText(password)
            self.show_status_message(f"رمز عبور با سطح {difficulty} با موفقیت تولید شد")
        except Exception as e:
            self.show_error_message(f"خطا در تولید رمز عبور: {str(e)}")

    def generate_passed_2(self):
        """Generate password with custom length."""
        try:
            # Get length from spinbox
            length = int(self.spinBox_1.value())
            
            # Create generator and generate password
            generator = CustomLengthPasswordGenerator(length)
            password = generator.generate()
            
            # Update UI
            self.textEdit_2.setText(password)
            self.show_status_message(f"رمز عبور با طول {length} با موفقیت تولید شد")
        except ValueError as e:
            self.show_error_message(str(e))
        except Exception as e:
            self.show_error_message(f"خطا در تولید رمز عبور: {str(e)}")

    def generate_passed_3(self):
        """Generate password with custom characters and length."""
        try:
            # Get parameters
            length = int(self.spinBox_2.value())
            char_set = self.textEdit_3.toPlainText()
            
            # Create generator and generate password
            generator = CustomCharSetPasswordGenerator(char_set, length)
            password = generator.generate()
            
            # Update UI
            self.textEdit_4.setText(password)
            self.show_status_message(f"رمز عبور سفارشی با موفقیت تولید شد")
        except ValueError as e:
            self.show_error_message(str(e))
        except Exception as e:
            self.show_error_message(f"خطا در تولید رمز عبور: {str(e)}")

    def signal(self):
        """Start animated password generation in a separate thread."""
        try:
            # Get parameters
            length = int(self.spinBox_2.value())
            char_set = self.textEdit_3.toPlainText()
            
            # If there is an active worker thread, stop it
            if self.worker and self.worker.isRunning():
                self.worker.stop()
                self.worker.wait()  # Wait for the thread to finish
                self.worker = None
                self.show_status_message("تولید رمز متوقف شد")
                return

            # Create worker thread and start it
            self.worker = PasswordWorkerThread(char_set, length)
            self.worker.result_ready.connect(self.update_result)
            self.worker.progress_update.connect(self.update_progress)
            self.worker.start()
            
            # Update button text to "توقف"
            self.generat_5.setText("توقف")
            
            self.show_status_message("در حال تولید رمز عبور...")
        except Exception as e:
            self.show_error_message(f"خطا در تولید رمز عبور: {str(e)}")

    def update_result(self, result):
        """Update UI with result from worker thread."""
        self.textEdit_4.setText(result)
        
        # If thread is finished, update button text back
        if not self.worker.isRunning():
            self.generat_5.setText("تولید کردن")
            
    def update_progress(self, progress):
        """Update progress in status bar.
        
        Args:
            progress (int): Progress percentage (0-100)
        """
        self.show_status_message(f"در حال تولید رمز عبور... {progress}%")

    def update_password_strength(self, text_edit, name):
        """Update password strength indicators based on password.
        
        Args:
            text_edit (QTextEdit): Text edit containing password
            name (str): Base name for strength indicator widgets
        """
        # Get password
        password = text_edit.toPlainText()
        
        # Get strength indicator widgets
        progress_bar = getattr(self, f"{name}_bar")
        rating_label = getattr(self, f"{name}_rating")
        
        # Evaluate password strength
        score, rating, message = evaluate_password_strength(password)
        
        # Update progress bar
        progress_bar.setValue(score)
        
        # Update color based on score
        if score >= 80:
            color = StyleManager.PRIMARY_GREEN  # Green
        elif score >= 60:
            color = StyleManager.PRIMARY_BLUE  # Blue
        elif score >= 40:
            color = StyleManager.PRIMARY_PURPLE  # Purple
        else:
            color = StyleManager.PRIMARY_RED  # Red
            
        progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
        
        # Update rating label
        rating_label.setText(rating)
        rating_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        # Update status message with detailed feedback
        if password:
            self.show_status_message(message) 