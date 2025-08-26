from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from notepad import Ui_MainWindow
import sys
import os


class NotepadMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Notepad++")
        
        # Set application icon
        icon_path = os.path.join("images", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Apply stylesheet for modern look
        self.apply_stylesheet()
        
        # Set default font for text editor
        editor_font = QFont("Segoe UI", 11)
        self.textEdit.setFont(editor_font)
        
        # Remove opacity setting (make it fully opaque)
        self.setWindowOpacity(1.0)
        
        # Make sure text is visible with dark color
        self.textEdit.setStyleSheet("color: black; background-color: white;")
        
        # Show the window
        self.show()

    def apply_stylesheet(self):
        # Set modern color scheme with visible text
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 250))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 250))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 245))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        # Apply stylesheet with explicit text colors
        style = """
        QMainWindow {
            border: none;
        }
        
        QTextEdit {
            border: 1px solid #aaaaaa;
            border-radius: 4px;
            padding: 8px;
            background-color: #ffffff;
            color: #000000;
            selection-background-color: #4a90e2;
            selection-color: #ffffff;
            font-size: 11pt;
        }
        
        QMenuBar {
            background-color: #f0f0f5;
            border-bottom: 1px solid #cccccc;
            color: #000000;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            background: transparent;
            color: #000000;
        }
        
        QMenuBar::item:selected {
            background-color: #4a90e2;
            color: #ffffff;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px 0px;
            color: #000000;
        }
        
        QMenu::item {
            padding: 6px 25px 6px 20px;
            color: #000000;
        }
        
        QMenu::item:selected {
            background-color: #4a90e2;
            color: #ffffff;
        }
        
        QToolBar {
            background-color: #f5f5fa;
            border-bottom: 1px solid #cccccc;
            spacing: 3px;
            padding: 3px;
        }
        
        QToolBar::separator {
            width: 1px;
            background-color: #cccccc;
            margin: 0px 5px;
        }
        
        QStatusBar {
            background-color: #f5f5fa;
            border-top: 1px solid #cccccc;
            color: #000000;
        }
        
        QToolButton {
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 2px;
            background-color: transparent;
        }
        
        QToolButton:hover {
            background-color: #e0e0e5;
            border: 1px solid #cccccc;
        }
        
        QToolButton:pressed {
            background-color: #d0d0d5;
        }
        
        QLabel {
            color: #000000;
        }
        
        QDialog {
            background-color: #f5f5fa;
            color: #000000;
        }
        
        QPushButton {
            background-color: #f0f0f5;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px 15px;
            color: #000000;
        }
        
        QPushButton:hover {
            background-color: #e5e5ea;
        }
        
        QPushButton:pressed {
            background-color: #d0d0d5;
        }
        """
        self.setStyleSheet(style)


# --------------------------------------------------------------------------------------------



        self.actionsave_file.triggered.connect(self.save_file)
        self.actionnew.triggered.connect(self.new_file)
        self.actionopen.triggered.connect(self.open_file)
        self.actionprint_file.triggered.connect(self.print_file)
        self.actionprint_preview.triggered.connect(self.preview_dialog)
        self.actionExport_pdf.triggered.connect(self.export_pdf)

        self.actionredo.triggered.connect(self.textEdit.redo)
        self.actionundo.triggered.connect(self.textEdit.undo)
        self.actioncopy.triggered.connect(self.textEdit.copy)
        self.actionpast.triggered.connect(self.textEdit.paste)
        self.actioncut.triggered.connect(self.textEdit.cut)
        self.actionclose_app.triggered.connect(self.close_program)

        self.actiontext_left.triggered.connect(self.text_left)
        self.actiontext_right.triggered.connect(self.text_right)
        self.actiontext_center.triggered.connect(self.text_center)
        self.actiontext_justify.triggered.connect(self.text_justify)
        self.actionset_font.triggered.connect(self.set_font)
        self.actionset_colo.triggered.connect(self.set_color)
        self.actionabout.triggered.connect(self.about)

        self.actiontext_bold.triggered.connect(self.set_bold)
        self.actiontext_italic.triggered.connect(self.set_italic)
        self.actiontext_underline.triggered.connect(self.set_underline)
        
        # Add word count display in status bar
        self.statusbar.showMessage("Ready")
        self.textEdit.textChanged.connect(self.update_status)



    # method --->>>

    #-----------------------------------
    
    def update_status(self):
        """Update status bar with document statistics"""
        text = self.textEdit.toPlainText()
        words = len(text.split()) if text else 0
        chars = len(text)
        self.statusbar.showMessage(f"Words: {words} | Characters: {chars}")

    #-----------------------------------

    def save_file(self):
        """ذخیره محتوای فعلی در یک فایل جدید"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            'ذخیره فایل...',
            '',  # مسیر پیش‌فرض
            'Text Files (*.txt);;All Files (*)'  # فیلتر فایل‌ها
        )

        if not file_name:
            return False  # کاربر عملیات را لغو کرده

        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                text = self.textEdit.toPlainText()
                file.write(text)

                # به روزرسانی وضعیت modified و عنوان پنجره
                self.textEdit.document().setModified(False)
                self.setWindowTitle(f"Text Editor - {file_name}")
                self.current_file = file_name  # ذخیره مسیر فایل فعلی

                QMessageBox.information(self, "ذخیره موفق", f"فایل با موفقیت در {file_name} ذخیره شد")
                return True

        except Exception as e:
            QMessageBox.critical(self, "خطا در ذخیره", f"خطا در ذخیره فایل:\n{str(e)}")
            return False

    def maybe_save_file(self):
        """بررسی نیاز به ذخیره قبل از عملیات حساس"""
        if not self.textEdit.document().isModified():
            return True

        ret = QMessageBox.warning(
            self,
            "ذخیره تغییرات",
            "محتوا تغییر کرده است. آیا می‌خواهید تغییرات را ذخیره کنید؟",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )

        if ret == QMessageBox.StandardButton.Yes:
            return self.save_file()  # ذخیره و بازگشت نتیجه
        elif ret == QMessageBox.StandardButton.No:
            return True  # ادامه بدون ذخیره
        else:  # Cancel
            return False  # لغو عملیات

    def new_file(self):
        """ایجاد یک سند جدید"""
        if not self.maybe_save_file():
            return  # کاربر عملیات را لغو کرده

        self.textEdit.clear()
        self.setWindowTitle("Text Editor - Untitled")
        self.current_file = None
        self.textEdit.document().setModified(False)

    #-----------------------------------

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self , 'Open File ...')
        if file_name[0]:
            with open(file_name[0], "r") as file:
                self.textEdit.setText(file.read())

    #-----------------------------------

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        # print(printer)
        dialog = QPrintDialog(printer)
        # print(dialog)

        if dialog.exec() == QFileDialog.DialogCode.Accepted :
            self.textEdit.print(printer)

    #-----------------------------------

    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintPreviewDialog(printer , self)

        dialog.paintRequested.connect(self.preview_file)
        dialog.exec()

    def preview_file(self , printer):
        self.textEdit.print(printer)

    #-----------------------------------

    def export_pdf(self):
        fn , _ = QFileDialog.getSaveFileName(self , 'Export PDF' , 'output.pdf')
        print(fn)
        if fn:
            if QFileInfo(fn).suffix() == '' : fn = f'{fn}.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)

    #-----------------------------------

    def set_bold (self):
        font = self.textEdit.currentFont()
        font.setBold(not font.bold())
        self.textEdit.setCurrentFont(font)

    #-----------------------------------

    def set_italic (self):
        font = self.textEdit.currentFont()
        font.setItalic(not font.italic())
        self.textEdit.setCurrentFont(font)

    #-----------------------------------

    def set_underline (self):
        font = self.textEdit.currentFont()
        font.setUnderline(not font.underline())
        self.textEdit.setCurrentFont(font)

    #-----------------------------------

    def close_program (self):
        self.close()

    #-----------------------------------

    def text_left (self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    #-----------------------------------

    def text_right (self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    #-----------------------------------

    def text_center (self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #-----------------------------------

    def text_justify (self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    #-----------------------------------

    def set_font (self):
        font , ok = QFontDialog.getFont()
        if ok :
            self.textEdit.setFont(font)

    #-----------------------------------

    def set_color (self):
        color = QColorDialog.getColor()
        if color :
            self.textEdit.setTextColor(color)

    #-----------------------------------

    def about (self):
        QMessageBox.about(self , 'About Notepad++' ,
                         '<h3>Notepad++</h3>'
                         '<p>A modern text editor with rich formatting capabilities.</p>'
                         '<p>Version 1.0</p>')










# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    ui = NotepadMain()
    sys.exit(app.exec())
