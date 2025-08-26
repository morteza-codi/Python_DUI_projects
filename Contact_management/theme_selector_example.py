"""
مثال ساده برای تغییر تم در زمان اجرا
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QVBoxLayout, 
    QLabel, QPushButton, QWidget, QTextEdit
)
from resources.themes.theme_loader import load_theme, get_available_themes


class ThemeSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("انتخاب تم")
        self.setMinimumSize(600, 400)
        
        # ایجاد ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # ایجاد چیدمان عمودی
        layout = QVBoxLayout(central_widget)
        
        # افزودن برچسب
        title_label = QLabel("انتخاب تم برنامه")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(title_label)
        
        # افزودن کمبوباکس برای انتخاب تم
        self.theme_combo = QComboBox()
        themes = get_available_themes()
        
        # نمایش نام‌های تم‌ها به صورت خوانا
        for theme in themes:
            # حذف عدد ابتدای نام و تبدیل _ به فاصله
            display_name = " ".join(theme.split("_")[1:]).title()
            self.theme_combo.addItem(display_name, theme)
            
        layout.addWidget(self.theme_combo)
        
        # افزودن دکمه برای اعمال تم
        apply_button = QPushButton("اعمال تم")
        apply_button.clicked.connect(self.apply_theme)
        layout.addWidget(apply_button)
        
        # افزودن برخی ویجت‌ها برای نمایش تم
        layout.addWidget(QLabel("این یک برچسب است"))
        
        text_edit = QTextEdit()
        text_edit.setPlainText("این یک متن نمونه است برای نمایش تم")
        layout.addWidget(text_edit)
        
        button1 = QPushButton("دکمه نمونه ۱")
        layout.addWidget(button1)
        
        button2 = QPushButton("دکمه نمونه ۲")
        layout.addWidget(button2)
        
        # نمایش وضعیت
        self.status_label = QLabel("تم پیش‌فرض اعمال شده است")
        layout.addWidget(self.status_label)
        
    def apply_theme(self):
        # دریافت نام تم انتخاب شده
        selected_index = self.theme_combo.currentIndex()
        theme_name = self.theme_combo.itemData(selected_index)
        
        # اعمال تم
        if load_theme(QApplication.instance(), theme_name):
            self.status_label.setText(f"تم {self.theme_combo.currentText()} با موفقیت اعمال شد")
        else:
            self.status_label.setText("خطا در اعمال تم")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # بارگذاری تم پیش‌فرض
    default_theme = "1_dark_blue"
    load_theme(app, default_theme)
    
    window = ThemeSelectorWindow()
    window.show()
    
    sys.exit(app.exec()) 