from PyQt6 import QtCore, QtGui, QtWidgets


class BaseUIComponent:
    """کلاس پایه برای همه اجزای رابط کاربری"""
    
    def apply_style(self, widget, style):
        """اعمال استایل به ویجت"""
        widget.setStyleSheet(style)


class LabelComponent(BaseUIComponent):
    """کلاس مدیریت برچسب‌ها"""
    
    def create_title_label(self, parent, text, geometry):
        """ایجاد برچسب عنوان"""
        label = QtWidgets.QLabel(parent=parent)
        label.setGeometry(geometry)
        font = QtGui.QFont()
        font.setPointSize(18)
        label.setFont(font)
        label.setText(text)
        
        # استایل‌دهی به برچسب عنوان
        self.apply_style(label, """
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        return label
    
    def create_counter_label(self, parent, geometry):
        """ایجاد برچسب شمارنده"""
        label = QtWidgets.QLabel(parent=parent)
        label.setGeometry(geometry)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        label.setFont(font)
        label.setText("5")
        
        # استایل‌دهی به برچسب شمارنده
        self.apply_style(label, """
            QLabel {
                color: #27ae60;
                font-size: 22px;
                font-weight: bold;
                background-color: #f0fff0;
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        return label


class InputComponent(BaseUIComponent):
    """کلاس مدیریت ورودی‌ها"""
    
    def create_text_input(self, parent, placeholder):
        """ایجاد فیلد ورودی متن"""
        text_edit = QtWidgets.QTextEdit(parent=parent)
        text_edit.setPlaceholderText(placeholder)
        
        # استایل‌دهی به فیلد ورودی
        self.apply_style(text_edit, """
            QTextEdit {
                border: 2px solid #9b59b6;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 5px;
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
            }
            QTextEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        return text_edit
    
    def create_result_display(self, parent, placeholder):
        """ایجاد فیلد نمایش نتیجه"""
        text_edit = QtWidgets.QTextEdit(parent=parent)
        text_edit.setPlaceholderText(placeholder)
        text_edit.setReadOnly(True)
        
        # استایل‌دهی به فیلد نمایش نتیجه
        self.apply_style(text_edit, """
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: #f0f8ff;
                padding: 8px;
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        return text_edit
    
    def create_status_display(self, parent, placeholder):
        """ایجاد فیلد نمایش وضعیت"""
        text_edit = QtWidgets.QTextEdit(parent=parent)
        text_edit.setPlaceholderText(placeholder)
        text_edit.setReadOnly(True)
        
        # استایل‌دهی به فیلد نمایش وضعیت
        self.apply_style(text_edit, """
            QTextEdit {
                border: 2px solid #e74c3c;
                border-radius: 8px;
                background-color: #fff5f5;
                padding: 5px;
                font-size: 14px;
                color: #c0392b;
                font-weight: bold;
            }
        """)
        return text_edit


class ButtonComponent(BaseUIComponent):
    """کلاس مدیریت دکمه‌ها"""
    
    def create_standard_button(self, parent, text):
        """ایجاد دکمه استاندارد"""
        button = QtWidgets.QPushButton(parent=parent)
        button.setText(text)
        
        # استایل‌دهی به دکمه استاندارد
        self.apply_style(button, """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #2980b9, stop:1 #2471a3);
                border: 1px solid #1f618d;
            }
            QPushButton:pressed {
                background: #1f618d;
            }
        """)
        return button
    
    def create_primary_button(self, parent, text):
        """ایجاد دکمه اصلی"""
        button = QtWidgets.QPushButton(parent=parent)
        button.setText(text)
        
        # استایل‌دهی به دکمه اصلی
        self.apply_style(button, """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #27ae60, stop:1 #219952);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 40px;
                font-size: 17px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #219952, stop:1 #1e8449);
                border: 1px solid #1a7741;
            }
            QPushButton:pressed {
                background: #1a7741;
            }
        """)
        return button 