import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QCoreApplication, Qt

from custom_ui import CustomUI
from message_handler import MessageHandler
from game_logic import GameLogic
from icon import create_icon, save_icon_to_file


class MainWindow(QMainWindow):
    """کلاس اصلی برنامه بازی حدس عدد"""
    
    def __init__(self):
        """مقداردهی اولیه برنامه"""
        super(MainWindow, self).__init__()
        
        # ایجاد و راه‌اندازی رابط کاربری
        self.ui = CustomUI()
        self.ui.setup_ui(self)
        self.setFixedSize(550 , 800)
        # تنظیم آیکون برنامه
        try:
            # ابتدا تلاش برای خواندن از فایل
            self.setWindowIcon(create_icon())
        except:
            # اگر فایل وجود نداشت، آن را ایجاد می‌کنیم
            save_icon_to_file()
            self.setWindowIcon(create_icon())
        
        # ایجاد مدیریت پیام‌ها
        self.message_handler = MessageHandler(
            self.ui.textEdit_6,
            self.ui.textEdit_5
        )
        
        # ایجاد منطق بازی
        self.game_logic = GameLogic(
            self.message_handler,
            self.ui
        )
        
        # اتصال دکمه‌های جدید
        self.connect_additional_buttons()
        
        # اتصال اکشن‌های منو
        self.connect_menu_actions()
    
    def connect_additional_buttons(self):
        """اتصال دکمه‌های اضافی به توابع مربوطه"""
        if hasattr(self.ui, 'help_button'):
            self.ui.help_button.clicked.connect(self.show_help)
            
        if hasattr(self.ui, 'restart_button'):
            self.ui.restart_button.clicked.connect(self.restart_game)
    
    def connect_menu_actions(self):
        """اتصال اکشن‌های منو به توابع مربوطه"""
        if hasattr(self.ui, 'action_restart'):
            self.ui.action_restart.triggered.connect(self.restart_game)
            
        if hasattr(self.ui, 'action_exit'):
            self.ui.action_exit.triggered.connect(self.close_application)
    
    def show_help(self):
        """نمایش راهنمای بازی"""
        help_text = """
        <h3>راهنمای بازی حدس عدد</h3>
        <p>1. ابتدا بازه شروع و پایان را مشخص کنید</p>
        <p>2. تعداد شانس‌های خود را تعیین کنید (اختیاری)</p>
        <p>3. حدس خود را وارد کنید و دکمه ثبت را بزنید</p>
        <p>4. دکمه بررسی را بزنید تا نتیجه حدس شما مشخص شود</p>
        <p>5. از راهنمایی‌ها برای حدس بعدی استفاده کنید</p>
        
        <h4>کلیدهای میانبر:</h4>
        <p>Ctrl+1: ثبت بازه اول</p>
        <p>Ctrl+2: ثبت بازه دوم</p>
        <p>Ctrl+3: ثبت تعداد شانس</p>
        <p>Ctrl+4: ثبت حدس</p>
        <p>Enter: بررسی حدس</p>
        <p>F5: شروع مجدد بازی</p>
        <p>F1: نمایش این راهنما</p>
        """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("راهنمای بازی")
        msg_box.setTextFormat(Qt.TextFormat.RichText)  # استفاده از نوع شمارشی Qt.TextFormat
        msg_box.setText(help_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()
    
    def restart_game(self):
        """شروع مجدد بازی"""
        if hasattr(self.game_logic, 'reset_game'):
            self.game_logic.reset_game()
            self.message_handler.show_info_message("بازی از نو شروع شد")
            self.message_handler.show_result_welcome()
    
    def close_application(self):
        """بستن برنامه با تأیید کاربر"""
        reply = QMessageBox.question(
            self, 'خروج از بازی',
            "آیا مطمئن هستید که می‌خواهید از بازی خارج شوید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QCoreApplication.instance().quit()


# اجرای برنامه
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

