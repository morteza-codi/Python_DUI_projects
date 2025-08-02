import secrets
import string
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox,
                             QStackedWidget, QTextEdit, QInputDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import hashlib
import sqlite3

from cryptography.fernet import Fernet

from passwd import Ui_MainWindow
# from main import cipher_suite

import json
import os
from datetime import datetime

# Constants
DATABASE_NAME = 'users.db'
MIN_PASSWORD_LENGTH = 8
DEFAULT_PASSWORD_LENGTH = 16
ENCRYPTION_KEY = b'Ke3NG7IWYBOdv42RPxPRhdQcK0WRVY-cGnGvpHyTVvM='
cipher_suite = Fernet(ENCRYPTION_KEY)

# Create database and user tables
def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
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

# Initialize the database
init_db()

def generate_strong_password(length=DEFAULT_PASSWORD_LENGTH):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+<>?"
    strong_password = ''.join(secrets.choice(characters) for _ in range(length))
    return strong_password

# Helper function for database connections
def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

# Helper function to get user_id from username
def get_user_id(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username=?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None
    except Exception:
        if 'conn' in locals():
            conn.close()
        return None
        
# Helper function for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
    
# Helper function for password encryption
def encrypt_password(password):
    try:
        password_bytes = password.encode('utf-8')
        return cipher_suite.encrypt(password_bytes).decode('utf-8')
    except Exception as e:
        raise Exception(f"Encryption error: {str(e)}")

# Helper function for password decryption
def decrypt_password(encrypted_password):
    try:
        encrypted_bytes = encrypted_password.encode('utf-8')
        return cipher_suite.decrypt(encrypted_bytes).decode('utf-8')
    except Exception as e:
        raise Exception(f"Decryption error: {str(e)}")
        
class LoginPage(QWidget):
    login_success = pyqtSignal(str)  # Signal for successful login

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel('Login to System')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.authenticate)
        layout.addWidget(login_btn)

        # Register link
        register_link = QPushButton("Don't have an account? Register")
        register_link.setStyleSheet('color: blue; border: none;')
        register_link.clicked.connect(self.show_register)
        layout.addWidget(register_link)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill all fields')
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Hash the input password for comparison
            hashed_password = hash_password(password)

            cursor.execute('SELECT password FROM users WHERE username=?', (username,))
            result = cursor.fetchone()

            if result and result[0] == hashed_password:
                self.login_success.emit(username)
                QMessageBox.information(self, 'Success', 'Login successful')
            else:
                QMessageBox.warning(self, 'Error', 'Incorrect username or password')

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Database connection error: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def show_register(self):
        self.parent().setCurrentIndex(1)  # Go to registration page


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel('Register New User')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Confirm password field
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('Confirm Password')
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_input)

        # Age field
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText('Age')
        layout.addWidget(self.age_input)

        # Register button
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.register_user)
        layout.addWidget(register_btn)

        # Login link
        login_link = QPushButton('Already registered? Login')
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
            QMessageBox.warning(self, 'Error', 'Please fill all fields')
            return

        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
            
        if len(password) < MIN_PASSWORD_LENGTH:
            QMessageBox.warning(self, 'Error', f'Password must be at least {MIN_PASSWORD_LENGTH} characters long')
            return

        try:
            age = int(age)
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid age')
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE username=?', (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, 'Error', 'This username is already registered')
                return

            # Hash the password
            hashed_password = hash_password(password)

            # Save the new user
            cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)',
                           (username, hashed_password, age))
            conn.commit()

            QMessageBox.information(self, 'Success', 'Registration successful')
            self.show_login()

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Registration error: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def show_login(self):
        self.parent().setCurrentIndex(0)  # Go to login page

# -----------------------------

class Change_passwd(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Get the username from the parent MainWindow
        self.username = parent.current_username if parent and hasattr(parent, 'current_username') else None

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

            # Validate inputs
            if not all([current_password, new_password, confirm_password]):
                QMessageBox.warning(self, 'Error', 'Please fill all fields')
                return

            if new_password != confirm_password:
                QMessageBox.warning(self, 'Error', 'New passwords do not match!')
                return

            if len(new_password) < MIN_PASSWORD_LENGTH:
                QMessageBox.warning(self, 'Error', f'Password must be at least {MIN_PASSWORD_LENGTH} characters long!')
                return
                
            # Check if new password is different from current
            if current_password == new_password:
                QMessageBox.warning(self, 'Error', 'New password must be different from current password!')
                return

            # Get user ID first
            user_id = get_user_id(self.username)
            if not user_id:
                QMessageBox.warning(self, 'Error', 'User not found in database!')
                return

            conn = get_db_connection()
            cursor = conn.cursor()

            # Verify current password
            hashed_current = hash_password(current_password)
            cursor.execute('SELECT password FROM users WHERE id=?', (user_id,))
            result = cursor.fetchone()

            if not result or result[0] != hashed_current:
                QMessageBox.warning(self, 'Error', 'Current password is incorrect!')
                return

            # Hash the new password
            hashed_new = hash_password(new_password)

            # Update password in database
            cursor.execute("UPDATE users SET password=? WHERE id=?",
                         (hashed_new, user_id))
            conn.commit()

            QMessageBox.information(self, 'Success',
                                  "Your password has been changed successfully!")
            self.close()

        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Database Error',
                              f"Database error: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
        except Exception as e:
            QMessageBox.warning(self, 'Error',
                              f"An error occurred: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


# Helper function to check password strength
def check_password_strength(password):
    """
    Check password strength and return a score from 0-4
    0: Very Weak, 1: Weak, 2: Medium, 3: Strong, 4: Very Strong
    """
    score = 0
    
    # Length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
        
    # Complexity checks
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
        score += 1
        
    return min(4, score)

class Add_Password(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username  # ذخیره نام کاربری به عنوان متغیر نمونه
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Add New Password')
        self.setFont(QFont('Arial', 12))
        self.setFixedSize(500, 450)  # Increased height for strength meter

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
        self.password_input.textChanged.connect(self.update_strength_meter)

        # Show/Hide Password Button
        self.toggle_btn = QPushButton('Show')
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_btn)
        
        # Password Strength Meter
        strength_layout = QHBoxLayout()
        strength_label = QLabel('Password Strength:')
        self.strength_meter = QLabel('Not Rated')
        self.strength_meter.setStyleSheet("font-weight: bold;")
        strength_layout.addWidget(strength_label)
        strength_layout.addWidget(self.strength_meter)

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
        layout.addLayout(strength_layout)
        layout.addWidget(generate_btn)
        layout.addWidget(save_btn)
        
    def update_strength_meter(self):
        """Update the password strength meter based on current password"""
        password = self.password_input.text()
        
        if not password:
            self.strength_meter.setText('Not Rated')
            self.strength_meter.setStyleSheet("font-weight: bold;")
            return
            
        strength = check_password_strength(password)
        
        if strength == 0:
            self.strength_meter.setText('Very Weak')
            self.strength_meter.setStyleSheet("color: #d9534f; font-weight: bold;")
        elif strength == 1:
            self.strength_meter.setText('Weak')
            self.strength_meter.setStyleSheet("color: #f0ad4e; font-weight: bold;")
        elif strength == 2:
            self.strength_meter.setText('Medium')
            self.strength_meter.setStyleSheet("color: #f0ad4e; font-weight: bold;")
        elif strength == 3:
            self.strength_meter.setText('Strong')
            self.strength_meter.setStyleSheet("color: #5cb85c; font-weight: bold;")
        else:
            self.strength_meter.setText('Very Strong')
            self.strength_meter.setStyleSheet("color: #5cb85c; font-weight: bold;")

    def toggle_password_visibility(self):
        if self.toggle_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText('Hide')
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText('Show')

    def generate_password(self):
        """Generate a strong random password"""
        strong_password = generate_strong_password(DEFAULT_PASSWORD_LENGTH)
        self.password_input.setText(strong_password)
        # Strength meter will update automatically via textChanged signal
        QMessageBox.information(self, 'Generated Password',
                                'A strong password has been generated!')

    def save_password(self):
        website = self.website_input.text().strip()
        entry_username = self.entry_username_input.text().strip()  # استفاده از نام جدید
        password = self.password_input.text().strip()

        # Validate inputs
        if not all([website, entry_username, password]):
            QMessageBox.warning(self, 'Error', 'All fields are required!')
            return
            
        # Get user ID first
        user_id = get_user_id(self.username)
        if not user_id:
            QMessageBox.critical(self, 'Error', f'User "{self.username}" not found in database!')
            return

        try:
            # 1. Encrypt the password
            try:
                encrypted_password = encrypt_password(password)
            except Exception as e:
                QMessageBox.critical(self, 'Encryption Error', f'Failed to encrypt password: {str(e)}')
                return

            # 2. Save to database
            conn = get_db_connection()
            cursor = conn.cursor()
            
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

class Delete_Password(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.parent = parent
        self.setup_ui()
        self.load_passwords()
        
    def setup_ui(self):
        self.setWindowTitle('Delete Password')
        self.setFont(QFont('Arial', 12))
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('Select Password to Delete')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Password list
        self.password_list = QTextEdit()
        self.password_list.setReadOnly(True)
        layout.addWidget(self.password_list)
        
        # Website input
        website_layout = QHBoxLayout()
        website_label = QLabel('Website:')
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText('Enter website to delete')
        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_input)
        layout.addLayout(website_layout)
        
        # Username input
        username_layout = QHBoxLayout()
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username to delete')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton('Delete Password')
        self.delete_btn.clicked.connect(self.delete_password)
        self.delete_btn.setStyleSheet("background-color: #d9534f; color: white;")
        
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def load_passwords(self):
        # Get user ID first
        user_id = get_user_id(self.username)
        if not user_id:
            QMessageBox.warning(self, 'Error', 'User not found in database.')
            self.close()
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch all passwords for this user
            cursor.execute('''
                SELECT website, username FROM passwords
                WHERE user_id = ?
                ORDER BY website
            ''', (user_id,))
            
            passwords = cursor.fetchall()
            
            if not passwords:
                QMessageBox.information(self, 'No Passwords', 'You have not saved any passwords yet.')
                self.close()
                return
                
            # Format and display passwords
            text_content = "<h2>Your Saved Passwords</h2><hr>"
            
            for website, username in passwords:
                text_content += f"<p><b>Website:</b> {website}<br>"
                text_content += f"<b>Username:</b> {username}</p><hr>"
            
            self.password_list.setHtml(text_content)
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', f'Error accessing database: {str(e)}')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {str(e)}')
            self.close()
        finally:
            if 'conn' in locals():
                conn.close()
    
    def delete_password(self):
        website = self.website_input.text().strip()
        username = self.username_input.text().strip()
        
        if not website or not username:
            QMessageBox.warning(self, 'Error', 'Please enter both website and username.')
            return
        
        # Ask for confirmation
        confirm = QMessageBox.question(
            self, 
            'Confirm Deletion',
            f'Are you sure you want to delete the password for {website} ({username})?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.No:
            return
        
        # Get user ID first
        user_id = get_user_id(self.username)
        if not user_id:
            QMessageBox.warning(self, 'Error', 'User not found in database.')
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Delete the password
            cursor.execute('''
                DELETE FROM passwords 
                WHERE user_id = ? AND website = ? AND username = ?
            ''', (user_id, website, username))
            
            conn.commit()
            
            if cursor.rowcount == 0:
                QMessageBox.warning(self, 'Not Found', 
                                   f'No password found for {website} with username {username}.')
                return
                
            QMessageBox.information(self, 'Success', 'Password deleted successfully!')
            
            # Refresh the password list
            self.load_passwords()
            
            # Clear inputs
            self.website_input.clear()
            self.username_input.clear()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', f'Error deleting password: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {str(e)}')
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

        # Store the original central widget before replacement
        self.original_central_widget = self.centralWidget()
        self.original_layout = self.original_central_widget.layout()

        # Hide the original widget initially
        self.original_central_widget.setVisible(False)
# ----------------------------------------------------------------------------------------
        self.btn_2.clicked.connect(self.change_password)
        self.btn_3.clicked.connect(self.add_password)
        self.btn_4.clicked.connect(self.view_passwords)
        self.btn_5.clicked.connect(self.delete_password)
        self.btn_6.clicked.connect(self.close_window)
        
        # Add menu bar
        self.create_menu_bar()
        
        # Add search action to menu
        search_action = self.menuBar().addAction('Search Passwords')
        search_action.triggered.connect(self.search_password)

# ----------------------------------------------------------------------------------------

        self.setup_auth_system()
        
    def create_menu_bar(self):
        """Create menu bar with additional options"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Backup action
        backup_action = file_menu.addAction('Backup Passwords')
        backup_action.triggered.connect(self.backup_passwords)
        
        # Restore action
        restore_action = file_menu.addAction('Restore Passwords')
        restore_action.triggered.connect(self.restore_passwords)
        
        # Exit action
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
    
    def backup_passwords(self):
        """Backup all passwords for the current user"""
        if not self.current_username:
            QMessageBox.warning(self, 'Error', 'You must be logged in to backup passwords.')
            return
            
        # Get user ID
        user_id = get_user_id(self.current_username)
        if not user_id:
            QMessageBox.warning(self, 'Error', 'User not found in database.')
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch all passwords for this user
            cursor.execute('''
                SELECT website, username, password FROM passwords
                WHERE user_id = ?
            ''', (user_id,))
            
            passwords = cursor.fetchall()
            
            if not passwords:
                QMessageBox.information(self, 'No Passwords', 
                                      'You have no passwords to backup.')
                return
                
            # Create backup data
            backup_data = {
                'username': self.current_username,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'passwords': []
            }
            
            # Add passwords to backup
            for website, username, encrypted_password in passwords:
                try:
                    # Decrypt for backup
                    decrypted_password = decrypt_password(encrypted_password)
                    backup_data['passwords'].append({
                        'website': website,
                        'username': username,
                        'password': decrypted_password
                    })
                except Exception as e:
                    QMessageBox.warning(self, 'Decryption Error', 
                                      f'Could not decrypt password for {website}: {str(e)}')
            
            # Create backup directory if it doesn't exist
            if not os.path.exists('backups'):
                os.makedirs('backups')
                
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'backups/passwords_{self.current_username}_{timestamp}.json'
            
            # Write backup file
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=4)
                
            QMessageBox.information(self, 'Backup Complete', 
                                  f'Passwords backed up to {backup_file}')
            
        except Exception as e:
            QMessageBox.critical(self, 'Backup Error', f'Error backing up passwords: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()
    
    def restore_passwords(self):
        """Restore passwords from a backup file"""
        if not self.current_username:
            QMessageBox.warning(self, 'Error', 'You must be logged in to restore passwords.')
            return
            
        # Get backup file path
        from PyQt6.QtWidgets import QFileDialog
        backup_file, _ = QFileDialog.getOpenFileName(
            self, 'Select Backup File', 'backups', 'JSON Files (*.json)'
        )
        
        if not backup_file:
            return  # User canceled
            
        try:
            # Read backup file
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
                
            # Verify backup format
            if not all(key in backup_data for key in ['username', 'created_at', 'passwords']):
                QMessageBox.critical(self, 'Invalid Backup', 
                                   'The selected file is not a valid backup file.')
                return
                
            # Verify username
            if backup_data['username'] != self.current_username:
                confirm = QMessageBox.question(
                    self, 'Username Mismatch',
                    f'This backup is for user "{backup_data["username"]}" but you are logged in as '
                    f'"{self.current_username}". Continue anyway?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirm == QMessageBox.StandardButton.No:
                    return
            
            # Get user ID
            user_id = get_user_id(self.current_username)
            if not user_id:
                QMessageBox.warning(self, 'Error', 'User not found in database.')
                return
                
            # Restore passwords
            conn = get_db_connection()
            cursor = conn.cursor()
            
            restored_count = 0
            skipped_count = 0
            
            for item in backup_data['passwords']:
                website = item['website']
                username = item['username']
                password = item['password']
                
                # Check if password already exists
                cursor.execute('''
                    SELECT id FROM passwords 
                    WHERE user_id = ? AND website = ? AND username = ?
                ''', (user_id, website, username))
                
                if cursor.fetchone():
                    skipped_count += 1
                    continue
                    
                # Encrypt and store password
                try:
                    encrypted_password = encrypt_password(password)
                    
                    cursor.execute('''
                        INSERT INTO passwords (website, username, password, user_id)
                        VALUES (?, ?, ?, ?)
                    ''', (website, username, encrypted_password, user_id))
                    
                    restored_count += 1
                except Exception as e:
                    QMessageBox.warning(self, 'Encryption Error',
                                      f'Could not encrypt password for {website}: {str(e)}')
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, 'Restore Complete',
                                  f'Restored {restored_count} passwords. '
                                  f'Skipped {skipped_count} existing passwords.')
            
        except json.JSONDecodeError:
            QMessageBox.critical(self, 'Invalid File', 'The selected file is not a valid JSON file.')
        except Exception as e:
            QMessageBox.critical(self, 'Restore Error', f'Error restoring passwords: {str(e)}')
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, 'About Password Manager',
                        'Password Manager v1.0\n\n'
                        'A secure application to store and manage your passwords.\n\n'
                        'Features:\n'
                        '- Secure password storage with encryption\n'
                        '- Password generation\n'
                        '- Password strength evaluation\n'
                        '- Search functionality\n'
                        '- Backup and restore')

    def close_window(self):
        self.close()

    def change_password(self):
        win = Change_passwd(self)
        win.show()

    def add_password(self):
        win = Add_Password(self.current_username, self)
        win.show()
    
    def search_password(self):
        if not self.current_username:
            QMessageBox.warning(self, 'Error', 'You must be logged in to search passwords.')
            return
            
        # Get search term
        search_term, ok = QInputDialog.getText(
            self, 'Search Passwords', 
            'Enter website or username to search:',
            QLineEdit.EchoMode.Normal
        )
        
        if not ok or not search_term.strip():
            return
            
        search_term = search_term.strip()
        
        # Get user ID first
        user_id = get_user_id(self.current_username)
        if not user_id:
            QMessageBox.warning(self, 'Error', 'User not found in database.')
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Search for passwords
            cursor.execute('''
                SELECT website, username, password FROM passwords
                WHERE user_id = ? AND (website LIKE ? OR username LIKE ?)
                ORDER BY website
            ''', (user_id, f'%{search_term}%', f'%{search_term}%'))
            
            passwords = cursor.fetchall()
            
            if not passwords:
                QMessageBox.information(self, 'No Results', 
                                       f'No passwords found matching "{search_term}".')
                return
                
            # Create a dialog to display search results
            dialog = QDialog(self)
            dialog.setWindowTitle('Search Results')
            dialog.setFixedSize(600, 400)
            
            layout = QVBoxLayout(dialog)
            
            # Create text area to display passwords
            text_area = QTextEdit()
            text_area.setReadOnly(True)
            
            # Format and display passwords
            text_content = f"<h2>Search Results for '{search_term}'</h2><hr>"
            
            for website, username, encrypted_password in passwords:
                try:
                    # Decrypt the password
                    decrypted_password = decrypt_password(encrypted_password)
                    text_content += f"<p><b>Website:</b> {website}<br>"
                    text_content += f"<b>Username:</b> {username}<br>"
                    text_content += f"<b>Password:</b> {decrypted_password}</p><hr>"
                except Exception as e:
                    text_content += f"<p><b>Website:</b> {website}<br>"
                    text_content += f"<b>Username:</b> {username}<br>"
                    text_content += f"<b>Password:</b> [Error decrypting: {str(e)}]</p><hr>"
            
            text_area.setHtml(text_content)
            layout.addWidget(text_area)
            
            # Add close button
            close_btn = QPushButton('Close')
            close_btn.clicked.connect(dialog.close)
            layout.addWidget(close_btn)
            
            dialog.exec()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', f'Error searching database: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()
    
    def view_passwords(self):
        if not self.current_username:
            QMessageBox.warning(self, 'Error', 'You must be logged in to view passwords.')
            return
        
        # Get user ID first
        user_id = get_user_id(self.current_username)
        if not user_id:
            QMessageBox.warning(self, 'Error', 'User not found in database.')
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch all passwords for this user
            cursor.execute('''
                SELECT website, username, password FROM passwords
                WHERE user_id = ?
                ORDER BY website
            ''', (user_id,))
            
            passwords = cursor.fetchall()
            
            if not passwords:
                QMessageBox.information(self, 'No Passwords', 'You have not saved any passwords yet.')
                return
                
            # Create a dialog to display passwords
            dialog = QDialog(self)
            dialog.setWindowTitle('Your Saved Passwords')
            dialog.setFixedSize(600, 400)
            
            layout = QVBoxLayout(dialog)
            
            # Create text area to display passwords
            text_area = QTextEdit()
            text_area.setReadOnly(True)
            
            # Format and display passwords
            text_content = "<h2>Your Saved Passwords</h2><hr>"
            
            for website, username, encrypted_password in passwords:
                try:
                    # Decrypt the password
                    decrypted_password = decrypt_password(encrypted_password)
                    text_content += f"<p><b>Website:</b> {website}<br>"
                    text_content += f"<b>Username:</b> {username}<br>"
                    text_content += f"<b>Password:</b> {decrypted_password}</p><hr>"
                except Exception as e:
                    text_content += f"<p><b>Website:</b> {website}<br>"
                    text_content += f"<b>Username:</b> {username}<br>"
                    text_content += f"<b>Password:</b> [Error decrypting: {str(e)}]</p><hr>"
            
            text_area.setHtml(text_content)
            layout.addWidget(text_area)
            
            # Add close button
            close_btn = QPushButton('Close')
            close_btn.clicked.connect(dialog.close)
            layout.addWidget(close_btn)
            
            dialog.exec()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', f'Error accessing database: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def delete_password(self):
        if not self.current_username:
            QMessageBox.warning(self, 'Error', 'You must be logged in to delete passwords.')
            return
            
        delete_dialog = Delete_Password(self.current_username, self)
        delete_dialog.exec()


    def setup_auth_system(self):
        # Create stacked widget for page management
        self.stack = QStackedWidget(self)

        # Create authentication pages
        self.login_page = LoginPage()
        self.register_page = RegisterPage()

        # Add pages to stack
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.original_central_widget)  # Main page

        # Connect successful login signal
        self.login_page.login_success.connect(self.on_login_success)

        # Set stacked widget as central widget
        self.setCentralWidget(self.stack)

    def on_login_success(self, username):
        self.current_username = username  # Store the username
        QMessageBox.information(self, 'Welcome', f'Hello {username}!\nYou have successfully logged in.')
        # Show main page and hide authentication pages
        self.original_central_widget.setVisible(True)
        self.stack.setCurrentIndex(2)  # Show main application page


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())