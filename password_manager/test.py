import secrets
import string
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox,
                             QStackedWidget, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import hashlib
import sqlite3

from cryptography.fernet import Fernet

from passwd import Ui_MainWindow
from main import cipher_suite


# ایجاد دیتابیس و جدول کاربران
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(website, username, user_id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# def generate_strong_password(length=12):
#     characters = string.ascii_letters + string.digits + "!@#$%^&*()_+<>?"
#     strong_password = ''.join(secrets.choice(characters) for _ in range(length))
#     return strong_password

class LoginPage(QWidget):
    login_success = pyqtSignal(str)  # سیگنال برای ورود موفق

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # عنوان
        title = QLabel('ورود به سیستم')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # فیلد نام کاربری
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('نام کاربری')
        layout.addWidget(self.username_input)

        # فیلد رمز عبور
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('رمز عبور')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # دکمه ورود
        login_btn = QPushButton('ورود')
        login_btn.clicked.connect(self.authenticate)
        layout.addWidget(login_btn)

        # لینک ثبت نام
        register_link = QPushButton('حساب کاربری ندارید؟ ثبت نام کنید')
        register_link.setStyleSheet('color: blue; border: none;')
        register_link.clicked.connect(self.show_register)
        layout.addWidget(register_link)

        self.setLayout(layout)

    def authenticate(self):
        global username
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'خطا', 'لطفاً تمام فیلدها را پر کنید')
            return

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # هش کردن رمز عبور ورودی برای مقایسه
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute('SELECT password FROM users WHERE username=?', (username,))
            result = cursor.fetchone()

            if result and result[0] == hashed_password:
                self.login_success.emit(username)
                QMessageBox.information(self, 'موفقیت', 'ورود با موفقیت انجام شد')
            else:
                QMessageBox.warning(self, 'خطا', 'نام کاربری یا رمز عبور اشتباه است')

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'خطا', f'خطا در ارتباط با دیتابیس: {str(e)}')
        finally:
            conn.close()

    def show_register(self):
        self.parent().setCurrentIndex(1)  # رفتن به صفحه ثبت نام


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # عنوان
        title = QLabel('ثبت نام کاربر جدید')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # فیلد نام کاربری
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('نام کاربری')
        layout.addWidget(self.username_input)

        # فیلد رمز عبور
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('رمز عبور')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # فیلد تکرار رمز عبور
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('تکرار رمز عبور')
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_input)

        # فیلد سن
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText('سن')
        layout.addWidget(self.age_input)

        # دکمه ثبت نام
        register_btn = QPushButton('ثبت نام')
        register_btn.clicked.connect(self.register_user)
        layout.addWidget(register_btn)

        # لینک ورود
        login_link = QPushButton('قبلاً ثبت نام کرده‌اید؟ وارد شوید')
        login_link.setStyleSheet('color: blue; border: none;')
        login_link.clicked.connect(self.show_login)
        layout.addWidget(login_link)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()
        age = self.age_input.text().strip()

        if not all([username, password, confirm, age]):
            QMessageBox.warning(self, 'خطا', 'لطفاً تمام فیلدها را پر کنید')
            return

        if password != confirm:
            QMessageBox.warning(self, 'خطا', 'رمز عبور و تکرار آن مطابقت ندارند')
            return

        try:
            age = int(age)
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'خطا', 'لطفاً سن معتبر وارد کنید')
            return

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # بررسی وجود کاربر
            cursor.execute('SELECT id FROM users WHERE username=?', (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, 'خطا', 'این نام کاربری قبلاً ثبت شده است')
                return

            # هش کردن رمز عبور
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # ذخیره کاربر جدید
            cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)',
                           (username, hashed_password, age))
            conn.commit()

            QMessageBox.information(self, 'موفقیت', 'ثبت نام با موفقیت انجام شد')
            self.show_login()

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'خطا', f'خطا در ثبت نام: {str(e)}')
        finally:
            conn.close()

    def show_login(self):
        self.parent().setCurrentIndex(0)  # رفتن به صفحه ورود

# -----------------------------

class Change_passwd(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Change password ...')
        self.setFont(QFont('Arial', 20))
        self.setFixedSize(400, 250)

        self.vbox = QVBoxLayout(self)

        # Current Password Section
        self.hbox_current = QHBoxLayout()
        self.label_current = QLabel(self)
        self.label_current.setText('Current password:')
        self.input_current = QLineEdit(self)
        self.input_current.setPlaceholderText('Enter current password')
        self.input_current.setEchoMode(QLineEdit.EchoMode.Password)
        self.hbox_current.addWidget(self.label_current)
        self.hbox_current.addWidget(self.input_current)

        # New Password Section
        self.hbox_new = QHBoxLayout()
        self.label_new = QLabel(self)
        self.label_new.setText('New password:')
        self.input_new = QLineEdit(self)
        self.input_new.setPlaceholderText('Enter new password')
        self.input_new.setEchoMode(QLineEdit.EchoMode.Password)
        self.hbox_new.addWidget(self.label_new)
        self.hbox_new.addWidget(self.input_new)

        # Confirm Password Section
        self.hbox_confirm = QHBoxLayout()
        self.label_confirm = QLabel(self)
        self.label_confirm.setText('Confirm password:')
        self.input_confirm = QLineEdit(self)
        self.input_confirm.setPlaceholderText('Confirm new password')
        self.input_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.hbox_confirm.addWidget(self.label_confirm)
        self.hbox_confirm.addWidget(self.input_confirm)

        # Change Password Button
        self.btn = QPushButton(self)
        self.btn.setText('Change password')
        self.btn.clicked.connect(self.change_password)

        # Add widgets to layout
        self.vbox.addLayout(self.hbox_current)
        self.vbox.addLayout(self.hbox_new)
        self.vbox.addLayout(self.hbox_confirm)
        self.vbox.addWidget(self.btn)

    def change_password(self):
        try:
            current_password = self.input_current.text()
            new_password = self.input_new.text()
            confirm_password = self.input_confirm.text()

            # اعتبارسنجی ورودی‌ها
            if not all([current_password, new_password, confirm_password]):
                QMessageBox.warning(self, 'Error', 'Please fill all fields')
                return

            if new_password != confirm_password:
                QMessageBox.warning(self, 'Error', 'New passwords do not match!')
                return

            if len(new_password) < 8:
                QMessageBox.warning(self, 'Error', 'Password must be at least 8 characters long!')
                return

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # بررسی رمز عبور فعلی
            hashed_current = hashlib.sha256(current_password.encode()).hexdigest()
            cursor.execute('SELECT password FROM users WHERE username=?', (username,))
            result = cursor.fetchone()

            if not result or result[0] != hashed_current:
                QMessageBox.warning(self, 'Error', 'Current password is incorrect!')
                return

            # هش کردن رمز عبور جدید
            hashed_new = hashlib.sha256(new_password.encode()).hexdigest()

            # به‌روزرسانی رمز عبور در پایگاه داده
            cursor.execute("UPDATE users SET password=? WHERE username=?",
                         (hashed_new,username))
            conn.commit()

            QMessageBox.information(self, 'Success',
                                  "Your password has been changed successfully!")
            self.close()

        except Exception as e:
            QMessageBox.warning(self, 'Error',
                              f"An error occurred: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


class Add_Password(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username  # ذخیره نام کاربری به عنوان متغیر نمونه
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Add New Password')
        self.setFont(QFont('Arial', 12))
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Website Section
        website_layout = QHBoxLayout()
        website_label = QLabel('Website/App:')
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText('e.g. google.com')
        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_input)

        # Username Section
        username_layout = QHBoxLayout()
        username_label = QLabel('Username/Email:')
        self.entry_username_input = QLineEdit()  # تغییر نام برای جلوگیری از اشتباه
        self.entry_username_input.setPlaceholderText('Your username or email')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.entry_username_input)

        # Password Section
        password_layout = QHBoxLayout()
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Show/Hide Password Button
        self.toggle_btn = QPushButton('Show')
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_btn)

        # Generate Password Button
        generate_btn = QPushButton('Generate Strong Password')
        generate_btn.clicked.connect(self.generate_password)

        # Save Button
        save_btn = QPushButton('Save Password')
        save_btn.clicked.connect(self.save_password)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white;")

        # Add widgets to layout
        layout.addLayout(website_layout)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(generate_btn)
        layout.addWidget(save_btn)

    def toggle_password_visibility(self):
        if self.toggle_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText('Hide')
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText('Show')

    def generate_password(self):
        """Generate a strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+<>?"
        strong_password = ''.join(secrets.choice(chars) for _ in range(16))
        self.password_input.setText(strong_password)
        QMessageBox.information(self, 'Generated Password',
                                f'Your new password is: {strong_password}')

    def save_password(self):
        website = self.website_input.text().strip()
        entry_username = self.entry_username_input.text().strip()  # استفاده از نام جدید
        password = self.password_input.text().strip()

        # Validate inputs
        if not all([website, entry_username, password]):
            QMessageBox.warning(self, 'Error', 'All fields are required!')
            return

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # 1. بررسی وجود کاربر در دیتابیس
            cursor.execute('SELECT id FROM users WHERE username=?', (self.username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.critical(self, 'Error', f'User "{self.username}" not found in database!')
                return

            user_id = user[0]

            # 2. رمزنگاری رمز عبور
            try:
                encrypted_password = cipher_suite.encrypt(password.encode()).decode()
            except Exception as e:
                QMessageBox.critical(self, 'Encryption Error', f'Failed to encrypt password: {str(e)}')
                return

            # 3. ذخیره در دیتابیس
            try:
                cursor.execute('''
                    INSERT INTO passwords (website, username, password, user_id)
                    VALUES (?, ?, ?, ?)
                ''', (website, entry_username, encrypted_password, user_id))
                conn.commit()

                QMessageBox.information(self, 'Success',
                                        'Password saved successfully!')
                self.close()

            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Duplicate Entry',
                                    'This website/username combination already exists for your account!')
                conn.rollback()

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error',
                                 f'Database error: {str(e)}')
            if 'conn' in locals():
                conn.rollback()
        except Exception as e:
            QMessageBox.critical(self, 'Error',
                                 f'An unexpected error occurred: {str(e)}')
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ابتدا رابط کاربری از Ui_MainWindow را تنظیم کنید
        self.setWindowTitle('سیستم احراز هویت')
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(380, 500)
        self.current_username = None

        # ذخیره ویجت مرکزی اصلی قبل از جایگزینی
        self.original_central_widget = self.centralWidget()
        self.original_layout = self.original_central_widget.layout()

        # مخفی کردن ویجت اصلی در ابتدا
        self.original_central_widget.setVisible(False)
# ----------------------------------------------------------------------------------------
        self.btn_2.clicked.connect(self.change_password)
        self.btn_3.clicked.connect(self.add_password)
        self.btn_6.clicked.connect(self.close_window)

# ----------------------------------------------------------------------------------------

        self.setup_auth_system()

    def close_window(self):
        self.close()

    def change_password(self):
        win = Change_passwd(self)
        win.show()

    def add_password(self):
        win = Add_Password(self.current_username, self)
        win.show()


    def setup_auth_system(self):
        # ایجاد stacked widget برای مدیریت صفحات
        self.stack = QStackedWidget(self)

        # ایجاد صفحات احراز هویت
        self.login_page = LoginPage()
        self.register_page = RegisterPage()

        # اضافه کردن صفحات به stack
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.original_central_widget)  # صفحه اصلی

        # اتصال سیگنال ورود موفق
        self.login_page.login_success.connect(self.on_login_success)

        # تنظیم stacked widget به عنوان ویجت مرکزی
        self.setCentralWidget(self.stack)

    def on_login_success(self, username):
        QMessageBox.information(self, 'خوش آمدید', f'سلام {username}!\nشما با موفقیت وارد شدید.')
        # نمایش صفحه اصلی و مخفی کردن صفحات احراز هویت
        self.original_central_widget.setVisible(True)
        self.stack.setCurrentIndex(2)  # نمایش صفحه اصلی برنامه


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())