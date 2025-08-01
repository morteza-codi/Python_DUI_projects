import secrets
import sqlite3
import string
import sys
from getpass import getpass

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QDialog, QHBoxLayout, QLabel, \
    QLineEdit, QTextEdit, QVBoxLayout, QPushButton
from cryptography.fernet import Fernet
from passwd import Ui_MainWindow  # فرض کنید فایل UI را ذخیره کردید به نام passwd_ui.py


# ----------------------------------------------------------

# encryption_key = Fernet.generate_key()
encryption_key = b'Ke3NG7IWYBOdv42RPxPRhdQcK0WRVY-cGnGvpHyTVvM='
cipher_suite = Fernet(encryption_key)

conn = sqlite3.connect('passwd_manager.db')
cursor = conn.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS passwords(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	website TEXT NOT NULL,
	username TEXT NOT NULL,
	password TEXT NOT NULL
	)
''')

conn.commit()

cursor.execute('''
	CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL
	)
''')

conn.commit()


def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+<>?"
    strong_password = ''.join(secrets.choice(characters) for _ in range(length))
    return strong_password
# -----------------------------------------------------

class Register(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Register ...')
        self.setFont(QFont('Arial', 20))
        self.setFixedSize(400, 200)

        self.vbox = QVBoxLayout(self)

        # Username Section
        self.hbox_1 = QHBoxLayout()
        self.label_1 = QLabel(self)
        self.label_1.setText('Username:')
        self.input_1 = QLineEdit(self)
        self.input_1.setPlaceholderText('Enter username')
        self.hbox_1.addWidget(self.label_1)
        self.hbox_1.addWidget(self.input_1)

        # Password Section
        self.hbox_2 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.label_2.setText('Password:')
        self.input_2 = QLineEdit(self)
        self.input_2.setPlaceholderText('Enter password')
        self.input_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.hbox_2.addWidget(self.label_2)
        self.hbox_2.addWidget(self.input_2)

        # Register Button
        self.btn = QPushButton(self)
        self.btn.setText('Register')
        self.btn.clicked.connect(self.register)

        # Add widgets to layout
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addWidget(self.btn)

    def register(self):
        # Get input values
        username = self.input_1.text().strip()
        password = self.input_2.text().strip()

        # Input validation
        if not username or not password:
            QMessageBox.warning(self, 'Input Error', "Username and password cannot be empty!")
            return

        if len(username) < 8:
            QMessageBox.warning(self, 'Input Error', "Username must be at least 8 characters long!")
            self.input_1.clear()
            return

        try:
            # Check if username already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone() is not None:
                QMessageBox.warning(self, 'Registration Error', "Username already exists!")
                self.input_1.clear()
                return

            # Encrypt password and store user
            encrypted_password = cipher_suite.encrypt(password.encode()).decode()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, encrypted_password))
            conn.commit()

            # Show success message and clean up
            QMessageBox.information(self, 'Success', "User registration successful!")
            self.input_1.clear()
            self.input_2.clear()
            self.close()

        except Exception as e:
            # Handle any database or encryption errors
            conn.rollback()
            QMessageBox.critical(self, 'Error', f"Registration failed: {str(e)}")

# -----------------------------------------------------

class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Login ...')
        self.setFont(QFont('Arial', 20))
        self.setFixedSize(400, 200)

        self.vbox = QVBoxLayout(self)

        # Username Section
        self.hbox_1 = QHBoxLayout()
        self.label_1 = QLabel(self)
        self.label_1.setText('Username:')
        self.input_1 = QLineEdit(self)
        self.input_1.setPlaceholderText('Enter username')
        self.hbox_1.addWidget(self.label_1)
        self.hbox_1.addWidget(self.input_1)

        # Password Section
        self.hbox_2 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.label_2.setText('Password:')
        self.input_2 = QLineEdit(self)
        self.input_2.setPlaceholderText('Enter password')
        self.input_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.hbox_2.addWidget(self.label_2)
        self.hbox_2.addWidget(self.input_2)

        # Register Button
        self.btn = QPushButton(self)
        self.btn.setText('login')
        self.btn.clicked.connect(self.login)

        # Add widgets to layout
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addWidget(self.btn)

    def login(self):
        global username
        # Get and clean input values
        username = self.input_1.text().strip()
        password = self.input_2.text().strip()

        # Input validation
        if not username or not password:
            QMessageBox.warning(self, 'Input Error', "Both username and password are required!")
            self.input_1.clear()
            self.input_2.clear()
            return False

        try:
            # Check if user exists
            cursor.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            if not user:
                # Don't reveal whether username exists (security)
                QMessageBox.warning(self, 'Login Failed', "Invalid credentials")
                self.input_1.clear()
                self.input_2.clear()
                return False

            # Verify password
            stored_password = user[2]
            decrypted_password = cipher_suite.decrypt(stored_password.encode()).decode()

            # Use constant-time comparison to prevent timing attacks
            if not secrets.compare_digest(password, decrypted_password):
                QMessageBox.warning(self, 'Login Failed', "Invalid credentials")
                self.input_1.clear()
                self.input_2.clear()
                return False

            # Login successful
            global current_user
            current_user = {
                'id': user[0],
                'username': user[1]
            }

            QMessageBox.information(self, 'Success', "Login successful!")
            if QMessageBox.StandardButton.Ok:
                win = Change_passwd(self)
                win.show()
            self.close()
            return True

        except Exception as e:
            # Log the error (you should have a logging mechanism)
            print(f"Login error: {str(e)}")
            QMessageBox.critical(self, 'Error', "An error occurred during login")
            self.input_1.clear()
            self.input_2.clear()
            return False

# --------------------------------------------------------

class Change_passwd(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Change password ...')
        self.setFont(QFont('Arial', 20))
        self.setFixedSize(400, 200)

        self.vbox = QVBoxLayout(self)

        # Username Section
        self.hbox_1 = QHBoxLayout()
        self.label_1 = QLabel(self)
        self.label_1.setText('new password :')
        self.input_1 = QLineEdit(self)
        self.input_1.setPlaceholderText('new password')
        self.hbox_1.addWidget(self.label_1)
        self.hbox_1.addWidget(self.input_1)

        # Register Button
        self.btn = QPushButton(self)
        self.btn.setText('change password')
        self.btn.clicked.connect(self.change_password)

        # Add widgets to layout
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addWidget(self.btn)

    def change_password(self):
        try:
            # Get the new password from input
            new_password = self.input_1.text()

            # If no password was entered, generate a strong one
            if not new_password:
                new_password = generate_strong_password()
                QMessageBox.information(self, 'Generated Password',
                                        f"Your new generated password is: {new_password}")

            # Encrypt the new password
            encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()

            # Update the password in the database
            cursor.execute("UPDATE users SET password=? WHERE username=?",
                           (encrypted_password, username))
            conn.commit()

            # Clear the input field after successful change
            self.input_1.clear()

            QMessageBox.information(self, 'Success',
                                    "Your password has been changed successfully!")
            self.close()

        except Exception as e:
            # Handle any potential errors
            QMessageBox.warning(self, 'Error',
                                f"An error occurred while changing the password: {str(e)}")
            conn.rollback()  # Rollback in case of error


# ----------------------------------------------------------

class Add_Password(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Add Password')
        self.setFont(QFont('Arial', 12))  # Reduced font size for better fit
        self.setFixedSize(500, 400)  # Increased height to accommodate all fields

        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(15)  # Add spacing between widgets

        # Website field
        self.hbox_1 = QHBoxLayout()
        self.label_1 = QLabel('Website:')
        self.input_1 = QLineEdit()
        self.input_1.setPlaceholderText('Enter website or app name')
        self.hbox_1.addWidget(self.label_1)
        self.hbox_1.addWidget(self.input_1)

        # Username/Email field
        self.hbox_2 = QHBoxLayout()
        self.label_2 = QLabel('Username/Email:')
        self.input_2 = QLineEdit()
        self.input_2.setPlaceholderText('Enter your username or email')
        self.hbox_2.addWidget(self.label_2)
        self.hbox_2.addWidget(self.input_2)

        # Password field (only visible when not generating)
        self.hbox_3 = QHBoxLayout()
        self.label_3 = QLabel('Password:')
        self.input_3 = QLineEdit()
        self.input_3.setPlaceholderText('Enter your password')
        self.hbox_3.addWidget(self.label_3)
        self.hbox_3.addWidget(self.input_3)

        # Add Password Button
        self.btn = QPushButton('Add Password')
        self.btn.clicked.connect(self.add_password)

        # Add widgets to layout
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addWidget(self.btn)

    def add_password(self):
        try:
            # Get input values with trimming
            website = self.input_1.text().strip()
            username = self.input_2.text().strip()
            password = self.input_3.text().strip()

            # Validate inputs
            if not website:
                QMessageBox.warning(self, 'Missing Information',
                                    'Website/App name cannot be empty!')
                self.input_1.setFocus()
                return

            if not username:
                QMessageBox.warning(self, 'Missing Information',
                                    'Username/Email cannot be empty!')
                self.input_2.setFocus()
                return

            if not password:
                QMessageBox.warning(self, 'Missing Information',
                                    'Password cannot be empty!')
                self.input_3.setFocus()
                return
            # Encrypt the password
            try:
                encrypted_password = cipher_suite.encrypt(password.encode()).decode()
            except Exception as encrypt_error:
                QMessageBox.critical(self, 'Encryption Error',
                                     f'Failed to encrypt password: {str(encrypt_error)}')
                return

            # Save to database
            try:
                cursor.execute("""
                    INSERT INTO passwords (website, username, password) 
                    VALUES (?, ?, ?)
                """, (website, username, encrypted_password))
                conn.commit()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Duplicate Entry',
                                    'This website/username combination already exists!')
                conn.rollback()
                return
            except sqlite3.Error as db_error:
                QMessageBox.critical(self, 'Database Error',
                                     f'Failed to save password: {str(db_error)}')
                conn.rollback()
                return

            # Clear fields and show success
            self.input_1.clear()
            self.input_2.clear()
            self.input_3.clear()

            QMessageBox.information(self, 'Success',
                                    'Password has been added successfully!')
            self.close()

            # Optional: Close the dialog or reset for new entry
            # self.close()  # Uncomment if you want to close after adding

        except Exception as unexpected_error:
            QMessageBox.critical(self, 'Unexpected Error',
                                 f'An unexpected error occurred: {str(unexpected_error)}')
            conn.rollback()

# -------------------------------------------------------------


class PasswordManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # اتصال دکمه‌ها به توابع
        self.btn_1.clicked.connect(self.register)
        self.btn_2.clicked.connect(self.change_password)
        self.btn_3.clicked.connect(self.add_password)
        self.btn_4.clicked.connect(self.view_passwords)
        self.btn_5.clicked.connect(self.delete_password)
        self.btn_6.clicked.connect(self.close_window)

    def register(self):
        win = Register(self)
        win.show()

    def change_password(self):
        win = Login(self)
        win.show()

    def add_password(self):
        win = (self)
        win.show()

    def view_passwords(self):
        pass

    def delete_password(self):
        pass

    def close_window(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())