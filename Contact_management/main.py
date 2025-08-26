import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from resources.themes.theme_loader import load_theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # بارگذاری تم پیش‌فرض (می‌توانید هر تم دیگری را انتخاب کنید)
    # default_theme = "premium_5_vintage_paper"
    default_theme = "premium_9_desert_winds"
    # default_theme = "premium_11_autumn_leaves"


    load_theme(app, default_theme)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 