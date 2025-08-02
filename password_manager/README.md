# Password Manager

A secure and user-friendly password manager application built with Python and PyQt6.

## Features

- **User Authentication**: Secure login and registration system
- **Password Management**: Store, view, edit, and delete passwords
- **Password Generation**: Create strong random passwords
- **Password Strength Evaluation**: Check how secure your passwords are
- **Search Functionality**: Find stored passwords by website or username
- **Encryption**: All passwords are encrypted using Fernet symmetric encryption
- **Backup and Restore**: Export and import your password database

## Screenshots

*Screenshots would be placed here*

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/password_manager.git
   cd password_manager
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python test.py
   ```

## Usage

### First-time Setup

1. Register a new account with a strong master password
2. Log in with your credentials

### Managing Passwords

- **Add Password**: Store credentials for a website or application
- **View Passwords**: See all your saved passwords
- **Search Passwords**: Find specific passwords
- **Delete Password**: Remove credentials you no longer need
- **Change Password**: Update your master password

### Backup and Restore

- **Backup**: Export your encrypted passwords to a JSON file
- **Restore**: Import passwords from a previously created backup

## Security

- All passwords are encrypted using Fernet symmetric encryption
- Master password is hashed using SHA-256
- No plaintext passwords are stored in the database
- Encryption key is required to decrypt passwords

## Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: PyQt6
- **Database**: SQLite
- **Encryption**: cryptography.fernet
- **Password Hashing**: hashlib.sha256

## Project Structure

- `test.py`: Main application file
- `passwd.py`: UI definition file
- `users.db`: SQLite database file
- `requirements.txt`: Project dependencies

## Future Improvements

- Password categories/folders
- Password expiration notifications
- Two-factor authentication
- Cloud synchronization
- Browser extension integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt6 for the GUI framework
- cryptography for secure encryption
- All contributors to the project 