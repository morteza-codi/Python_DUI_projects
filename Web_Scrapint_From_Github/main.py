import sys
import requests
import webbrowser
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, QTextEdit, QHBoxLayout,
    QPushButton, QMessageBox, QProgressDialog, QLabel, QLineEdit, QFormLayout,
    QWidget, QCheckBox, QMenuBar, QMenu, QStatusBar, QFileDialog
)
from PyQt6.QtGui import QClipboard, QIntValidator, QTextCursor, QTextCharFormat, QColor, QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='github_finder.log'
)


class GitHubSearchWorker(QThread):
    """Thread class for fetching GitHub repositories"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    rate_limit = pyqtSignal(int)

    def __init__(self, language, num_repositories, min_stars=None):
        super().__init__()
        self.language = language
        self.num_repositories = num_repositories
        self.min_stars = min_stars
        self.stop_requested = False

    def run(self):
        try:
            logging.info(f"Starting search for {self.language} (min stars: {self.min_stars})")

            base_query = f"language:{self.language}"
            if self.min_stars:
                base_query += f" stars:>={self.min_stars}"

            url = f"https://api.github.com/search/repositories?q={base_query}&sort=stars&order=desc"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "PyQt6-GitHub-Trending-App"
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Check rate limit
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                self.rate_limit.emit(remaining)
                if remaining < 5:
                    logging.warning(f"API rate limit is almost reached. Remaining: {remaining}")

            data = response.json()
            if not data.get('items'):
                self.error.emit("No repositories found matching your criteria")
                return

            repositories = data.get('items', [])[:self.num_repositories]
            if not repositories:
                self.error.emit("No repositories found matching your criteria")
                return

            self.finished.emit(repositories)

        except requests.exceptions.Timeout:
            error_msg = "Request timed out. Please try again later."
            logging.error(error_msg)
            self.error.emit(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logging.error(error_msg)
            self.error.emit(error_msg)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            logging.error(error_msg)
            self.error.emit(error_msg)


class GitHubSearchDialog(QDialog):
    def __init__(self, language, num_repositories, min_stars=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'GitHub Trending {language} Repositories')
        self.language = language
        self.num_repositories = num_repositories
        self.min_stars = min_stars
        self.current_results = None
        self.selected_repo_url = None

        self.init_ui()
        self.start_search()

    def init_ui(self):
        """Initialize the user interface"""
        self.setMinimumSize(800, 600)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # Header with search criteria
        criteria_text = f"<b>Top {self.num_repositories} {self.language} Repositories</b>"
        if self.min_stars:
            criteria_text += f" <i>(with at least {self.min_stars} stars)</i>"
        self.header_label = QLabel(criteria_text)
        self.header_label.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.header_label)

        # Rate limit label
        self.rate_limit_label = QLabel("API rate limit: checking...")
        self.rate_limit_label.setStyleSheet("color: #666; font-size: 10px;")
        self.layout.addWidget(self.rate_limit_label)

        # Text area for displaying results
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_area.setPlaceholderText("Loading trending repositories...")
        self.text_area.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, Courier New, monospace;
                font-size: 12px;
            }
        """)
        self.text_area.cursorPositionChanged.connect(self.highlight_url)
        self.layout.addWidget(self.text_area)

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)

        # Copy button
        self.copy_button = QPushButton("📋 Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setToolTip("Copy the repository list to clipboard")
        self.copy_button.setEnabled(False)

        # Save button
        self.save_button = QPushButton("💾 Save As...")
        self.save_button.clicked.connect(self.save_to_file)
        self.save_button.setToolTip("Save the repository list to a text file")
        self.save_button.setEnabled(False)

        # Open button
        self.open_button = QPushButton("🌐 Open")
        self.open_button.clicked.connect(self.open_in_browser)
        self.open_button.setToolTip("Open selected repository in browser")
        self.open_button.setEnabled(False)

        # Exit button
        self.exit_button = QPushButton("❌ Exit")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white;")

        # Add buttons to layout
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.open_button)
        self.button_layout.addWidget(self.exit_button)
        self.button_layout.addStretch()

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def start_search(self):
        """Start the repository search process"""
        self.progress = QProgressDialog("Fetching trending repositories...", None, 0, 0, self)
        self.progress.setWindowTitle("Loading")
        self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress.setCancelButton(None)
        self.progress.show()

        # Create and start worker thread
        self.worker = GitHubSearchWorker(self.language, self.num_repositories, self.min_stars)
        self.worker.finished.connect(self.display_results)
        self.worker.error.connect(self.show_error)
        self.worker.rate_limit.connect(self.update_rate_limit)
        self.worker.start()

    def update_rate_limit(self, remaining):
        """Update the rate limit display"""
        self.rate_limit_label.setText(f"GitHub API rate limit: {remaining} requests remaining")

    def display_results(self, repositories):
        """Display the fetched repositories in the text area"""
        self.progress.close()
        self.current_results = repositories

        if not repositories:
            self.text_area.setPlainText(f"No trending {self.language} repositories found matching your criteria.")
            return

        result_text = f"🔥 Top {len(repositories)} {self.language} Repositories on GitHub\n"
        if self.min_stars:
            result_text += f"⭐ Minimum stars: {self.min_stars}\n"
        result_text += "=" * 80 + "\n\n"

        for idx, repo in enumerate(repositories, 1):
            result_text += (
                    f"🏆 #{idx}: {repo['name']}\n"
                    f"⭐ Stars: {repo['stargazers_count']:,}\n"
                    f"📝 Description: {repo['description'] or 'No description'}\n"
                    f"🔗 URL: {repo['html_url']}\n"
                    f"👤 Author: {repo['owner']['login']}\n"
                    f"🔄 Last updated: {repo['updated_at'][:10]}\n"
                    f"📊 Size: {repo['size']:,} KB | 🍴 Forks: {repo['forks_count']:,}\n"
                    f"-" * 80 + "\n\n"
            )

        self.text_area.setPlainText(result_text)
        self.copy_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def highlight_url(self):
        """Highlight URLs when cursor is on them"""
        cursor = self.text_area.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        text = cursor.selectedText()

        if text.startswith("http"):
            self.selected_repo_url = text
            self.open_button.setEnabled(True)

            # Highlight the URL
            format = QTextCharFormat()
            format.setForeground(QColor(3, 102, 214))  # GitHub link color
            format.setFontUnderline(True)
            cursor.mergeCharFormat(format)
        else:
            self.open_button.setEnabled(False)
            self.selected_repo_url = None

    def open_in_browser(self):
        """Open selected repository in default browser"""
        if self.selected_repo_url:
            webbrowser.open(self.selected_repo_url)

    def show_error(self, error_msg):
        """Show error message"""
        self.progress.close()
        QMessageBox.critical(self, "Error", error_msg)
        self.close()

    def copy_to_clipboard(self):
        """Copy the repository list to clipboard"""
        text_to_copy = self.text_area.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)
        QMessageBox.information(self, "Success", "Copied to clipboard!", QMessageBox.StandardButton.Ok)

    def save_to_file(self):
        """Save the repository list to a file"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File",
            f"github_trending_{self.language.lower()}_repos.txt",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.toPlainText())
                QMessageBox.information(self, "Success", f"Saved to {filename}", QMessageBox.StandardButton.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def closeEvent(self, event):
        """Clean up when closing the dialog"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GitHub Repository Finder')
        self.setMinimumSize(500, 300)

        # Load settings
        self.settings = QSettings("GitHubFinder", "AppSettings")

        # Initialize UI
        self.init_ui()

        # Load saved settings
        self.load_settings()

    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(layout)

        # Title label
        title_label = QLabel("GitHub Trending Repository Finder")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #24292e;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Language input
        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("e.g., Python, JavaScript")
        form_layout.addRow("Programming Language:", self.language_input)

        # Number of repositories input
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("e.g., 10 (max 100)")
        self.count_input.setValidator(QIntValidator(1, 100))
        form_layout.addRow("Number of Repositories:", self.count_input)

        # Advanced search checkbox
        self.advanced_checkbox = QCheckBox("Advanced Search Options")
        self.advanced_checkbox.toggled.connect(self.toggle_advanced_options)
        form_layout.addRow(self.advanced_checkbox)

        # Advanced options (initially hidden)
        self.min_stars_input = QLineEdit()
        self.min_stars_input.setPlaceholderText("Minimum stars (optional)")
        self.min_stars_input.setValidator(QIntValidator(0, 1000000))
        self.min_stars_input.setVisible(False)
        form_layout.addRow("Minimum Stars:", self.min_stars_input)

        layout.addLayout(form_layout)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Search button
        self.search_button = QPushButton("🔍 Search")
        self.search_button.clicked.connect(self.start_search)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        # Exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)

        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        # Create menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Recent searches submenu
        self.recent_menu = file_menu.addMenu("&Recent Searches")

        # Load recent searches
        recent_searches = self.settings.value("recent_searches", [])
        for search in recent_searches[:5]:  # Show last 5 searches
            action = QAction(search, self)
            action.triggered.connect(lambda _, s=search: self.load_recent_search(s))
            self.recent_menu.addAction(action)

        file_menu.addSeparator()

        # Settings action
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def load_recent_search(self, search_str):
        """Load parameters from a recent search"""
        # This is a simplified version - you'll need to parse the search_str
        # and populate the fields accordingly
        QMessageBox.information(self, "Info", f"Loading search: {search_str}")

    def toggle_advanced_options(self, checked):
        """Toggle visibility of advanced options"""
        self.min_stars_input.setVisible(checked)
        if not checked:
            self.min_stars_input.clear()

    def load_settings(self):
        """Load saved settings"""
        last_language = str(self.settings.value("last_language", ""))
        last_count = str(self.settings.value("last_count", "10"))
        last_min_stars = str(self.settings.value("last_min_stars", ""))
        advanced_enabled = bool(self.settings.value("advanced_enabled", False, type=bool))

        self.language_input.setText(last_language)
        self.count_input.setText(last_count)

        if advanced_enabled:
            self.advanced_checkbox.setChecked(True)
            self.min_stars_input.setText(last_min_stars)

    def save_settings(self):
        """Save current settings"""
        self.settings.setValue("last_language", self.language_input.text())
        self.settings.setValue("last_count", self.count_input.text())
        self.settings.setValue("last_min_stars", self.min_stars_input.text())
        self.settings.setValue("advanced_enabled", self.advanced_checkbox.isChecked())

    def start_search(self):
        """Start the search process"""
        language = self.language_input.text().strip()
        count_text = self.count_input.text().strip()
        min_stars = self.min_stars_input.text().strip() if self.advanced_checkbox.isChecked() else None

        if not language:
            QMessageBox.warning(self, "Input Error", "Please enter a programming language")
            return

        try:
            count = int(count_text) if count_text else 10
            if count < 1 or count > 100:
                raise ValueError("Number must be between 1 and 100")

            if min_stars:
                min_stars = int(min_stars)
                if min_stars < 0:
                    raise ValueError("Minimum stars cannot be negative")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Invalid input: {str(e)}")
            return

        # Save to recent searches
        recent_searches = self.settings.value("recent_searches", [])
        search_str = f"{language} ({count} repos)"
        if min_stars:
            search_str += f" with {min_stars}+ stars"

        # Add to beginning and keep only unique items
        recent_searches = [search_str] + [s for s in recent_searches if s != search_str]
        self.settings.setValue("recent_searches", recent_searches[:10])  # Keep last 10

        # Save current settings
        self.save_settings()

        # Open search dialog
        search_dialog = GitHubSearchDialog(
            language,
            count,
            int(min_stars) if min_stars else None,
            self
        )
        search_dialog.exec()

    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", "Application settings are automatically saved.")

    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>GitHub Repository Finder</h2>
        <p>Version 1.0</p>
        <p>This application helps you find trending repositories on GitHub.</p>
        <p>Developed with Python and PyQt6</p>
        """
        QMessageBox.about(self, "About", about_text)

    def closeEvent(self, event):
        """Save settings when closing"""
        self.save_settings()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style and font
    app.setStyle('Fusion')

    # Dark theme
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(palette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(palette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)

    # Set font
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())