import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, 
    QDialog, QVBoxLayout, QTextEdit, QPushButton,
    QLabel, QFileDialog
)
from PyQt6.QtGui import QAction

from models.contact_manager import ContactManager
from ui.input_dialog import InputDialog
from utils.validators import Validators
from contact_manager import Ui_MainWindow
from resources.themes.theme_selector import ThemeSelectorDialog
from resources.themes.theme_loader import load_theme


class MainWindow(QMainWindow, Ui_MainWindow):
    """کلاس پنجره اصلی برنامه"""
    
    def __init__(self, parent=None):
        """
        سازنده کلاس پنجره اصلی
        
        Args:
            parent: والد ویجت
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        # مقداردهی اولیه مدیریت مخاطبین
        self.contact_manager = ContactManager()
        
        # تنظیم عنوان پنجره
        self.setWindowTitle("مدیریت مخاطبین")
        
        # اتصال دکمه‌ها به توابع مربوطه
        self.btn_1.clicked.connect(self.add_contact_dialog)
        self.btn_2.clicked.connect(self.edit_contact_dialog)
        self.btn_3.clicked.connect(self.search_contact_dialog)
        self.btn_4.clicked.connect(self.delete_contact_dialog)
        self.btn_5.clicked.connect(self.add_note_dialog)
        self.btn_6.clicked.connect(self.view_notes_dialog)
        self.btn_7.clicked.connect(self.delete_note_dialog)
        self.btn_8.clicked.connect(self.close)
        
        # اتصال گزینه‌های منو
        self.actionexport_to_csv.triggered.connect(self.export_to_csv)
        self.actionimport_from_csv.triggered.connect(self.import_from_csv)
        
        # اضافه کردن گزینه تغییر تم به منو
        self.actionchange_theme = QAction("تغییر تم برنامه", self)
        self.actionchange_theme.setObjectName("actionchange_theme")
        self.actionchange_theme.triggered.connect(self.change_theme_dialog)
        # اضافه کردن به منو (اگر منو وجود دارد)
        if hasattr(self, 'menuFile'):
            self.menuFile.addAction(self.actionchange_theme)
        
        # راه‌اندازی جدول
        self.setup_table()
        self.refresh_table()
        
        # نمایش پیام وضعیت
        self.show_status("برنامه مدیریت مخاطبین با موفقیت بارگذاری شد")
    
    def setup_table(self):
        """تنظیم جدول نمایش مخاطبین"""
        # تنظیم عرض ستون‌ها
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # فعال‌سازی مرتب‌سازی
        self.tableWidget.setSortingEnabled(True)
        
        # فعال‌سازی انتخاب سطرها
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    
    def refresh_table(self):
        """به‌روزرسانی جدول با اطلاعات جدید مخاطبین"""
        self.tableWidget.setSortingEnabled(False)  # غیرفعال‌سازی مرتب‌سازی هنگام به‌روزرسانی
        self.tableWidget.setRowCount(len(self.contact_manager.contacts))
        
        for i, contact in enumerate(self.contact_manager.contacts):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(contact.first_name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(contact.last_name))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(contact.phone))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(contact.email or ''))
            
            # نمایش یادداشت آخر در جدول
            note_text = contact.notes[-1]['text'] if contact.notes else ''
            self.tableWidget.setItem(i, 4, QTableWidgetItem(note_text))
        
        self.tableWidget.setSortingEnabled(True)  # فعال‌سازی مجدد مرتب‌سازی
    
    def show_status(self, message: str):
        """
        نمایش پیام وضعیت
        
        Args:
            message: پیام برای نمایش
        """
        self.textEdit.setText(message)
    
    def show_message(self, title: str, message: str, icon=QMessageBox.Icon.Information):
        """
        نمایش پیام در یک دیالوگ
        
        Args:
            title: عنوان پیام
            message: متن پیام
            icon: آیکون پیام
        """
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
    
    # عملیات مخاطبین
    def add_contact_dialog(self):
        """نمایش دیالوگ افزودن مخاطب جدید"""
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید"),
            ("شماره تلفن", "شماره تلفن را وارد کنید"),
            ("ایمیل", "ایمیل را وارد کنید (اختیاری)")
        ]
        
        dialog = InputDialog("افزودن مخاطب", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            # اعتبارسنجی ورودی‌ها
            if not inputs["نام"] or not inputs["نام خانوادگی"] or not inputs["شماره تلفن"]:
                self.show_message("خطا", "نام، نام خانوادگی و شماره تلفن ضروری هستند", 
                                 QMessageBox.Icon.Warning)
                return
            
            # اعتبارسنجی نام و نام خانوادگی
            if not Validators.validate_name(inputs["نام"]) or not Validators.validate_name(inputs["نام خانوادگی"]):
                self.show_message("خطا", "نام و نام خانوادگی باید فقط شامل حروف باشند", 
                                 QMessageBox.Icon.Warning)
                return
            
            # اعتبارسنجی شماره تلفن
            if not Validators.validate_phone(inputs["شماره تلفن"]):
                self.show_message("خطا", "شماره تلفن باید فقط شامل اعداد باشد", 
                                 QMessageBox.Icon.Warning)
                return
            
            # اعتبارسنجی ایمیل در صورت وجود
            if inputs["ایمیل"] and not Validators.validate_email(inputs["ایمیل"]):
                self.show_message("خطا", "فرمت ایمیل نامعتبر است", 
                                 QMessageBox.Icon.Warning)
                return
            
            # افزودن مخاطب
            success, message = self.contact_manager.add_contact(
                inputs["نام"], 
                inputs["نام خانوادگی"], 
                inputs["شماره تلفن"], 
                inputs["ایمیل"] if inputs["ایمیل"] else None
            )
            
            if success:
                self.refresh_table()
                self.show_status(message)
            else:
                self.show_message("خطا", message, QMessageBox.Icon.Warning)
    
    def edit_contact_dialog(self):
        """نمایش دیالوگ ویرایش مخاطب"""
        # ابتدا مخاطب مورد نظر را پیدا کنید
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید")
        ]
        
        dialog = InputDialog("یافتن مخاطب برای ویرایش", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            # یافتن مخاطب
            contact = self.contact_manager.find_contact(inputs["نام"], inputs["نام خانوادگی"])
            if not contact:
                self.show_message("خطا", f"مخاطب {inputs['نام']} {inputs['نام خانوادگی']} یافت نشد", 
                                 QMessageBox.Icon.Warning)
                return
            
            # نمایش دیالوگ ویرایش با مقادیر فعلی
            edit_fields = [
                ("نام جدید", f"فعلی: {contact.first_name}"),
                ("نام خانوادگی جدید", f"فعلی: {contact.last_name}"),
                ("شماره تلفن جدید", f"فعلی: {contact.phone}"),
                ("ایمیل جدید", f"فعلی: {contact.email or 'بدون ایمیل'}")
            ]
            
            edit_dialog = InputDialog("ویرایش مخاطب", edit_fields, self)
            if edit_dialog.exec():
                edit_inputs = edit_dialog.get_inputs()
                
                # اعتبارسنجی ورودی‌های جدید
                if edit_inputs["نام جدید"] and not Validators.validate_name(edit_inputs["نام جدید"]):
                    self.show_message("خطا", "نام باید فقط شامل حروف باشد", QMessageBox.Icon.Warning)
                    return
                    
                if edit_inputs["نام خانوادگی جدید"] and not Validators.validate_name(edit_inputs["نام خانوادگی جدید"]):
                    self.show_message("خطا", "نام خانوادگی باید فقط شامل حروف باشد", QMessageBox.Icon.Warning)
                    return
                    
                if edit_inputs["شماره تلفن جدید"] and not Validators.validate_phone(edit_inputs["شماره تلفن جدید"]):
                    self.show_message("خطا", "شماره تلفن باید فقط شامل اعداد باشد", QMessageBox.Icon.Warning)
                    return
                    
                if edit_inputs["ایمیل جدید"] and not Validators.validate_email(edit_inputs["ایمیل جدید"]):
                    self.show_message("خطا", "فرمت ایمیل نامعتبر است", QMessageBox.Icon.Warning)
                    return
                
                # به‌روزرسانی مخاطب
                success, message = self.contact_manager.update_contact(
                    inputs["نام"],
                    inputs["نام خانوادگی"],
                    edit_inputs["نام جدید"] if edit_inputs["نام جدید"] else None,
                    edit_inputs["نام خانوادگی جدید"] if edit_inputs["نام خانوادگی جدید"] else None,
                    edit_inputs["شماره تلفن جدید"] if edit_inputs["شماره تلفن جدید"] else None,
                    edit_inputs["ایمیل جدید"]  # رشته خالی برای حذف ایمیل معتبر است
                )
                
                if success:
                    self.refresh_table()
                    self.show_status(message)
                else:
                    self.show_message("خطا", message, QMessageBox.Icon.Warning)
    
    def search_contact_dialog(self):
        """نمایش دیالوگ جستجوی مخاطبین"""
        fields = [
            ("عبارت جستجو", "نام، نام خانوادگی، شماره تلفن یا ایمیل را وارد کنید")
        ]
        
        dialog = InputDialog("جستجوی مخاطبین", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            search_term = inputs["عبارت جستجو"]
            
            if not search_term:
                self.show_message("خطا", "لطفاً عبارت جستجو را وارد کنید", QMessageBox.Icon.Warning)
                return
            
            results = self.contact_manager.search_contacts(search_term)
            
            if results:
                # به‌روزرسانی جدول با نتایج جستجو
                self.tableWidget.setRowCount(len(results))
                for i, contact in enumerate(results):
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(contact.first_name))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(contact.last_name))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(contact.phone))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(contact.email or ''))
                    note_text = contact.notes[-1]['text'] if contact.notes else ''
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(note_text))
                
                self.show_status(f"{len(results)} مخاطب با عبارت '{search_term}' یافت شد")
            else:
                self.show_status(f"مخاطبی با عبارت '{search_term}' یافت نشد")
    
    def delete_contact_dialog(self):
        """نمایش دیالوگ حذف مخاطب"""
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید")
        ]
        
        dialog = InputDialog("حذف مخاطب", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            # تأیید حذف
            confirm = QMessageBox.question(
                self, 
                "تأیید حذف", 
                f"آیا از حذف مخاطب {inputs['نام']} {inputs['نام خانوادگی']} اطمینان دارید؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                success, message = self.contact_manager.delete_contact(
                    inputs["نام"], 
                    inputs["نام خانوادگی"]
                )
                
                if success:
                    self.refresh_table()
                    self.show_status(message)
                else:
                    self.show_message("خطا", message, QMessageBox.Icon.Warning)
    
    def add_note_dialog(self):
        """نمایش دیالوگ افزودن یادداشت به مخاطب"""
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید"),
            ("یادداشت", "متن یادداشت را وارد کنید")
        ]
        
        dialog = InputDialog("افزودن یادداشت", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            # اعتبارسنجی ورودی‌ها
            if not inputs["نام"] or not inputs["نام خانوادگی"] or not inputs["یادداشت"]:
                self.show_message("خطا", "تمام فیلدها ضروری هستند", QMessageBox.Icon.Warning)
                return
            
            success, message = self.contact_manager.add_note(
                inputs["نام"],
                inputs["نام خانوادگی"],
                inputs["یادداشت"]
            )
            
            if success:
                self.refresh_table()
                self.show_status(message)
            else:
                self.show_message("خطا", message, QMessageBox.Icon.Warning)
    
    def view_notes_dialog(self):
        """نمایش دیالوگ مشاهده یادداشت‌های مخاطب"""
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید")
        ]
        
        dialog = InputDialog("مشاهده یادداشت‌ها", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            success, message, notes = self.contact_manager.get_notes(
                inputs["نام"],
                inputs["نام خانوادگی"]
            )
            
            if success and notes:
                # ایجاد دیالوگ برای نمایش یادداشت‌ها
                notes_dialog = QDialog(self)
                notes_dialog.setWindowTitle(f"یادداشت‌های {inputs['نام']} {inputs['نام خانوادگی']}")
                notes_dialog.resize(500, 400)
                
                layout = QVBoxLayout()
                notes_text = QTextEdit()
                notes_text.setReadOnly(True)
                
                # قالب‌بندی یادداشت‌ها
                formatted_notes = ""
                for i, note in enumerate(notes, 1):
                    formatted_notes += f"{i}. [{note.get('timestamp', 'بدون تاریخ')}]\n{note.get('text', '')}\n\n"
                
                notes_text.setText(formatted_notes)
                layout.addWidget(notes_text)
                
                close_button = QPushButton("بستن")
                close_button.clicked.connect(notes_dialog.accept)
                layout.addWidget(close_button)
                
                notes_dialog.setLayout(layout)
                notes_dialog.exec()
            else:
                self.show_status(message)
    
    def delete_note_dialog(self):
        """نمایش دیالوگ حذف یادداشت مخاطب"""
        # ابتدا مخاطب را پیدا کنید
        fields = [
            ("نام", "نام را وارد کنید"),
            ("نام خانوادگی", "نام خانوادگی را وارد کنید")
        ]
        
        dialog = InputDialog("حذف یادداشت - مرحله 1", fields, self)
        if dialog.exec():
            inputs = dialog.get_inputs()
            
            success, message, notes = self.contact_manager.get_notes(
                inputs["نام"],
                inputs["نام خانوادگی"]
            )
            
            if success and notes:
                # نمایش یادداشت‌ها و درخواست شماره یادداشت برای حذف
                notes_text = "یادداشت‌های موجود:\n\n"
                for i, note in enumerate(notes, 1):
                    notes_text += f"{i}. [{note.get('timestamp', 'بدون تاریخ')}] {note.get('text', '')[:30]}...\n"
                
                index_dialog = InputDialog("حذف یادداشت - مرحله 2", [("شماره یادداشت", "شماره یادداشت برای حذف را وارد کنید")], self)
                
                # افزودن برچسب نمایش یادداشت‌های موجود
                notes_label = QLabel(notes_text)
                index_dialog.layout().insertWidget(0, notes_label)
                
                if index_dialog.exec():
                    index_input = index_dialog.get_inputs()["شماره یادداشت"]
                    
                    try:
                        note_index = int(index_input)
                        
                        # تأیید حذف
                        confirm = QMessageBox.question(
                            self, 
                            "تأیید حذف", 
                            f"آیا از حذف یادداشت شماره {note_index} اطمینان دارید؟",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        
                        if confirm == QMessageBox.StandardButton.Yes:
                            success, message = self.contact_manager.delete_note(
                                inputs["نام"],
                                inputs["نام خانوادگی"],
                                note_index
                            )
                            
                            if success:
                                self.refresh_table()
                                self.show_status(message)
                            else:
                                self.show_message("خطا", message, QMessageBox.Icon.Warning)
                    except ValueError:
                        self.show_message("خطا", "لطفاً یک عدد معتبر وارد کنید", QMessageBox.Icon.Warning)
            else:
                self.show_status(message)
    
    def export_to_csv(self):
        """صادرات مخاطبین به فایل CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "صادرات مخاطبین",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            success, message = self.contact_manager.export_to_csv(file_path)
            
            if success:
                self.show_status(message)
            else:
                self.show_message("خطا", message, QMessageBox.Icon.Warning)
    
    def import_from_csv(self):
        """واردات مخاطبین از فایل CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "واردات مخاطبین",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            success, message, count = self.contact_manager.import_from_csv(file_path)
            
            if success:
                self.refresh_table()
                self.show_status(message)
            else:
                self.show_message("خطا", message, QMessageBox.Icon.Warning) 
                
    def change_theme_dialog(self):
        """نمایش دیالوگ تغییر تم"""
        dialog = ThemeSelectorDialog(self)
        
        # تنظیم تم فعلی
        current_theme = self.get_current_theme()
        dialog.set_current_theme(current_theme)
        
        if dialog.exec():
            selected_theme = dialog.get_selected_theme()
            if selected_theme:
                # اعمال تم جدید
                app = QtWidgets.QApplication.instance()
                load_theme(app, selected_theme)
                self.show_status(f"تم '{selected_theme}' با موفقیت اعمال شد")
    
    def get_current_theme(self):
        """دریافت تم فعلی برنامه"""
        # در اینجا می‌توانید تم فعلی را از تنظیمات برنامه بخوانید
        # فعلاً به صورت پیش‌فرض تم اول را برمی‌گرداند
        return "premium_7_midnight_galaxy"