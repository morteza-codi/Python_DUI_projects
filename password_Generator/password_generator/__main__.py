"""
Main entry point for the Password Generator application.

Run this module to start the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from password_generator.ui.main_window import MainWindow
from password_generator.ui.styles import StyleManager


def main():
    """Main entry point for the application."""
    # Create application
    app = QApplication(sys.argv)
    
    # Apply global styles
    app.setStyleSheet(StyleManager.get_status_bar_style())
    
    # Create and show main window
    window = MainWindow()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 