from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QApplication, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from resources.themes.theme_loader import load_theme, get_available_themes

class ThemeSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("انتخاب تم")
        self.setup_ui()
        self.current_theme = None
        self.selected_theme = None
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("انتخاب تم برای برنامه")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        theme_layout = QHBoxLayout()
        theme_label = QLabel("تم:")
        self.theme_combo = QComboBox()
        
        themes = get_available_themes()
        for theme in themes:
            display_name = theme.replace("_", " ").title()
            if theme.startswith("premium_"):
                display_name = "⭐ " + display_name[8:]
            self.theme_combo.addItem(display_name, theme)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("اعمال")
        self.apply_button.clicked.connect(self.apply_theme)
        
        cancel_button = QPushButton("لغو")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def set_current_theme(self, theme_name):
        self.current_theme = theme_name
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == theme_name:
                self.theme_combo.setCurrentIndex(i)
                break
    
    def apply_theme(self):
        self.selected_theme = self.theme_combo.currentData()
        self.accept()
    
    def get_selected_theme(self):
        return self.selected_theme