import sys
import shutil
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QTextEdit,
    QPushButton, QInputDialog, QFileDialog
)

from file import Ui_MainWindow


# File selection dialog using PyQt6
def file_open_dialog():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    if dialog.exec():
        return dialog.selectedFiles()[0]
    return None


# Directory selection dialog using PyQt6
def directory_open_dialog():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    if dialog.exec():
        return dialog.selectedFiles()[0]
    return None


class FilesListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Files List')
        self.setFixedSize(500, 500)

        self.vbox = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.btn = QPushButton('Close')
        self.btn.clicked.connect(self.accept)

        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)

        self.list_files()

    def list_files(self):
        path = directory_open_dialog()
        if not path:
            self.text.setText("No directory selected.")
            return
            
        try:
            file_list = sorted(os.listdir(path))
            self.text.append(f"Directory: {path}\n")
            self.text.append("Files and folders:\n")
            for i in file_list:
                item_path = os.path.join(path, i)
                if os.path.isdir(item_path):
                    self.text.append(f"📁 {i}")
                else:
                    size = os.path.getsize(item_path)
                    size_str = self.format_size(size)
                    self.text.append(f"📄 {i} ({size_str})")
        except PermissionError:
            self.text.append("Error: Permission denied accessing this directory.")
        except Exception as e:
            self.text.append(f"Error: {str(e)}")
            
    def format_size(self, size_bytes):
        """Format file size in a human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.1f} GB"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("File Manager")

        # Connect buttons to their respective functions
        self.btn_1.clicked.connect(self.open_file)
        self.btn_2.clicked.connect(self.copy_file)
        self.btn_3.clicked.connect(self.delete_file)
        self.btn_4.clicked.connect(self.rename_file)
        self.btn_5.clicked.connect(self.move_file)
        self.btn_6.clicked.connect(self.make_directory)
        self.btn_7.clicked.connect(self.remove_directory)
        self.btn_8.clicked.connect(self.list_files)
        self.btn_9.clicked.connect(self.close)
        
        # Connect about menu action
        self.actionA_program_for_managing_files.triggered.connect(self.show_about)
        
        # Status message
        self.textEdit.setReadOnly(True)
        self.textEdit.setText("Welcome to File Manager! Select an operation from the buttons.")

    def open_file(self):
        path = file_open_dialog()
        if not path:
            self.textEdit.setText("No file selected.")
            return
            
        try:
            os.startfile(path)
            self.textEdit.setText(f"Success -> Opened file: {path}")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not open file: {str(e)}')
            self.textEdit.setText(f"Error -> Could not open file: {str(e)}")

    def copy_file(self):
        source = file_open_dialog()
        if not source:
            self.textEdit.setText("No source file selected.")
            return
            
        destination = directory_open_dialog()
        if not destination:
            self.textEdit.setText("No destination directory selected.")
            return
            
        try:
            dest_file = os.path.join(destination, os.path.basename(source))
            shutil.copy2(source, destination)
            QMessageBox.information(self, 'Success', 'File copied successfully!')
            self.textEdit.setText(f"Success -> File copied from {source} to {dest_file}")
        except PermissionError:
            QMessageBox.warning(self, 'Error', 'Permission denied. Cannot copy file!')
            self.textEdit.setText('Error -> Permission denied. Cannot copy file!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not copy file: {str(e)}')
            self.textEdit.setText(f'Error -> Could not copy file: {str(e)}')

    def delete_file(self):
        path = file_open_dialog()
        if not path:
            self.textEdit.setText("No file selected.")
            return
            
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                     f'Are you sure you want to delete "{os.path.basename(path)}"?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                                     
        if reply == QMessageBox.StandardButton.No:
            self.textEdit.setText("Delete operation cancelled.")
            return
            
        try:
            os.remove(path)
            QMessageBox.information(self, 'Success', 'File deleted successfully!')
            self.textEdit.setText(f'Success -> File deleted: {path}')
        except PermissionError:
            QMessageBox.warning(self, 'Error', 'Permission denied. Cannot delete file!')
            self.textEdit.setText('Error -> Permission denied. Cannot delete file!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not delete file: {str(e)}')
            self.textEdit.setText(f'Error -> Could not delete file: {str(e)}')

    def rename_file(self):
        file_path = file_open_dialog()
        if not file_path:
            self.textEdit.setText("No file selected.")
            return
            
        try:
            dir_path = os.path.dirname(file_path)
            old_name = os.path.basename(file_path)
            extension = os.path.splitext(file_path)[1]
            name_without_ext = os.path.splitext(old_name)[0]
            
            new_name, ok = QInputDialog.getText(self, 'Rename File', 
                                              'Enter new name (without extension):',
                                              text=name_without_ext)
            
            if ok and new_name:
                new_path = os.path.join(dir_path, new_name + extension)
                
                if os.path.exists(new_path):
                    QMessageBox.warning(self, 'Error', f'A file named "{new_name + extension}" already exists!')
                    self.textEdit.setText(f'Error -> A file named "{new_name + extension}" already exists!')
                    return
                    
                os.rename(file_path, new_path)
                QMessageBox.information(self, 'Success', 'File renamed successfully!')
                self.textEdit.setText(f'Success -> File renamed from "{old_name}" to "{new_name + extension}"')
            else:
                self.textEdit.setText("Rename operation cancelled.")
                
        except PermissionError:
            QMessageBox.warning(self, 'Error', 'Permission denied. Cannot rename file!')
            self.textEdit.setText('Error -> Permission denied. Cannot rename file!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not rename file: {str(e)}')
            self.textEdit.setText(f'Error -> Could not rename file: {str(e)}')

    def move_file(self):
        source = file_open_dialog()
        if not source:
            self.textEdit.setText("No source file selected.")
            return
            
        destination = directory_open_dialog()
        if not destination:
            self.textEdit.setText("No destination directory selected.")
            return
            
        source_dir = os.path.dirname(source)
        if os.path.normpath(source_dir) == os.path.normpath(destination):
            QMessageBox.warning(self, 'Error', 'Source and destination directories are the same.')
            self.textEdit.setText('Error -> Source and destination directories are the same.')
            return
            
        try:
            dest_file = os.path.join(destination, os.path.basename(source))
            if os.path.exists(dest_file):
                reply = QMessageBox.question(self, 'File Exists', 
                                           f'File "{os.path.basename(source)}" already exists in destination. Overwrite?',
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    self.textEdit.setText("Move operation cancelled.")
                    return
                    
            shutil.move(source, destination)
            QMessageBox.information(self, 'Success', 'File moved successfully!')
            self.textEdit.setText(f'Success -> File moved from {source} to {dest_file}')
        except PermissionError:
            QMessageBox.warning(self, 'Error', 'Permission denied. Cannot move file!')
            self.textEdit.setText('Error -> Permission denied. Cannot move file!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not move file: {str(e)}')
            self.textEdit.setText(f'Error -> Could not move file: {str(e)}')

    def make_directory(self):
        path = directory_open_dialog()
        if not path:
            self.textEdit.setText("No directory selected.")
            return
            
        name, ok = QInputDialog.getText(self, 'Create Directory', 'Enter directory name:')
        
        if ok and name:
            new_dir_path = os.path.join(path, name)
            
            if os.path.exists(new_dir_path):
                QMessageBox.warning(self, 'Error', f'A directory named "{name}" already exists!')
                self.textEdit.setText(f'Error -> A directory named "{name}" already exists!')
                return
                
            try:
                os.mkdir(new_dir_path)
                QMessageBox.information(self, 'Success', 'Directory created successfully!')
                self.textEdit.setText(f'Success -> Directory created: {new_dir_path}')
            except PermissionError:
                QMessageBox.warning(self, 'Error', 'Permission denied. Cannot create directory!')
                self.textEdit.setText('Error -> Permission denied. Cannot create directory!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Could not create directory: {str(e)}')
                self.textEdit.setText(f'Error -> Could not create directory: {str(e)}')
        else:
            self.textEdit.setText("Directory creation cancelled.")

    def remove_directory(self):
        path = directory_open_dialog()
        if not path:
            self.textEdit.setText("No directory selected.")
            return
            
        try:
            # Check if directory is empty
            if os.listdir(path):
                reply = QMessageBox.question(self, 'Directory Not Empty', 
                                           'Directory is not empty. Remove all contents?',
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    shutil.rmtree(path)
                else:
                    self.textEdit.setText("Directory removal cancelled.")
                    return
            else:
                os.rmdir(path)
                
            QMessageBox.information(self, 'Success', 'Directory removed successfully!')
            self.textEdit.setText(f'Success -> Directory removed: {path}')
        except PermissionError:
            QMessageBox.warning(self, 'Error', 'Permission denied. Cannot remove directory!')
            self.textEdit.setText('Error -> Permission denied. Cannot remove directory!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not remove directory: {str(e)}')
            self.textEdit.setText(f'Error -> Could not remove directory: {str(e)}')

    def list_files(self):
        dialog = FilesListDialog(self)
        dialog.exec()
        
    def show_about(self):
        QMessageBox.information(self, 'About', 'File Manager\n\nA program for managing files and directories.\nVersion 1.0')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())