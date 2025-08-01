import sys

import shutil
import os
from tkinter import filedialog

import easygui

from file import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QTextEdit, \
    QPushButton


#  انتخاب فایل
def file_open_box(self):
    path = easygui.fileopenbox()
    return path


# انتخاب پوشه
def directory_open_box(self):
    path = filedialog.askdirectory()
    return path


class new_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle('list files ... !')
        self.setFixedSize(400 , 400)

        self.vbox = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.btn = QPushButton()
        self.btn.setText('close')
        self.btn.clicked.connect(self.close_window)

        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)

        self.list_files()

    def list_files(self):
        path = directory_open_box(self)
        file_list = sorted(os.listdir(path))
        for i in file_list:
            self.text.append(i)

    def close_window(self):
        self.close()

app = QApplication(sys.argv)

class MainWindow(QMainWindow , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_1.clicked.connect(self.open_file)
        self.btn_2.clicked.connect(self.copy_file)
        self.btn_3.clicked.connect(self.delete_file)
        self.btn_4.clicked.connect(self.rename_file)
        self.btn_5.clicked.connect(self.move_file)
        self.btn_6.clicked.connect(self.make_directory)
        self.btn_7.clicked.connect(self.remove_directory)
        self.btn_8.clicked.connect(self.list_files)
        self.btn_9.clicked.connect(self.close_window)

    def open_file(self):
        path = file_open_box(self)
        try:
            os.startfile(path)
        except TypeError:
            QMessageBox.warning(self, 'Error', 'File not found!')
            self.textEdit.setText('Error -> File not found!')

    def copy_file(self):
        source = file_open_box(self)
        destination = directory_open_box(self)
        try:
            shutil.copy(source, destination)
            QMessageBox.information(self, 'Success', 'file copied!')
            self.textEdit.setText('Success -> file copied!')
        except:
            QMessageBox.warning(self, 'Error', 'Could not copy file!')
            self.textEdit.setText('Error -> Could not copy file!')

    def delete_file(self):
        path = file_open_box(self)
        try:
            os.remove(path)
            QMessageBox.information(self, 'Success', 'file deleted!')
            self.textEdit.setText('Success -> file deleted!')

        except:
            QMessageBox.warning(self, 'Error', 'Could not delete file!')
            self.textEdit.setText('Error -> Could not delete file!')


    def rename_file(self):
        try:
            file = file_open_box(self)
            path1 = os.path.dirname(file)
            extension = os.path.splitext(file)[1]
            new_name = input("new name: ")
            path2 = os.path.join(path1, new_name + extension)
            os.rename(file, path2)
            QMessageBox.information(self, 'Success', 'file renamed!')
            self.textEdit.setText('Success -> file renamed!')

        except:
            QMessageBox.warning(self, 'Error', 'Could not rename file!')
            self.textEdit.setText('Error -> Could not rename file!')


    def move_file(self):
        source = file_open_box(self)
        destination = directory_open_box(self)
        if source == destination:
            QMessageBox.warning(self, 'Error', 'The transmission path has not changed. ')
            self.textEdit.setText('Error -> The transmission path has not changed. ')

        else:
            try:
                shutil.move(source, destination)
                QMessageBox.information(self, 'Success', 'file moved!')
                self.textEdit.setText('Success -> file moved!')

            except:
                QMessageBox.warning(self, 'Error', 'Could not move file!')
                self.textEdit.setText('Error -> Could not move file!')


    def make_directory(self):
        path = directory_open_box(self)
        name = input("name: ")
        path = os.path.join(path, name)
        try:
            os.mkdir(path)
            QMessageBox.information(self, 'Success', 'directory created!')
            self.textEdit.setText('Success -> directory created!')

        except:
            QMessageBox.warning(self, 'Error', 'Could not create directory!')
            self.textEdit.setText('Error -> Could not create directory!')

    def remove_directory(self):
        path = directory_open_box(self)
        try:
            os.rmdir(path)
        except:
            QMessageBox.warning(self, 'Error', 'Could not remove directory!')
            self.textEdit.setText('Error -> Could not remove directory!')


    def list_files(self):
        # path = directory_open_box(self)
        # file_list = sorted(os.listdir(path))
        # for i in file_list:
        #     print(i)
        win = new_window()
        win.exec()

    def close_window(self):
        self.close()









window = MainWindow()
window.show()

sys.exit(app.exec())