"""
Base UI classes for the Password Generator application.

Contains base window classes and common UI functionality.
"""

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication


class BaseWindow(QMainWindow):
    """Base window class with common functionality."""
    
    def __init__(self, title="Password Generator", width=1050, height=730):
        """Initialize the base window.
        
        Args:
            title (str): Window title
            width (int): Window width
            height (int): Window height
        """
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
    
    def show_status_message(self, message, timeout=3000):
        """Show a non-blocking status message.
        
        Args:
            message (str): Message to display
            timeout (int): Time in milliseconds to display the message
        """
        self.statusBar().showMessage(message, timeout)
    
    def show_error_message(self, message, title="خطا"):
        """Show an error message dialog.
        
        Args:
            message (str): Error message to display
            title (str): Dialog title
        """
        QMessageBox.critical(self, title, message)
    
    def show_info_message(self, message, title="اطلاعات"):
        """Show an information message dialog.
        
        Args:
            message (str): Information message to display
            title (str): Dialog title
        """
        QMessageBox.information(self, title, message)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard.
        
        Args:
            text (str): Text to copy to clipboard
            
        Returns:
            bool: True if text was copied, False if text was empty
        """
        if not text:
            self.show_status_message("هیچ متنی برای کپی وجود ندارد")
            return False
            
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.show_status_message("متن با موفقیت کپی شد")
        return True 