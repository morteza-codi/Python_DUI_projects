from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton
)


class InputDialog(QDialog):
    """کلاس دیالوگ ورودی برای دریافت اطلاعات از کاربر"""
    
    def __init__(self, title: str, fields: list, parent=None):
        """
        سازنده کلاس دیالوگ ورودی
        
        Args:
            title: عنوان دیالوگ
            fields: لیستی از فیلدها به صورت (نام، متن راهنما)
            parent: والد ویجت
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 200)
        
        self.fields = {}
        layout = QVBoxLayout()
        
        for field_name, placeholder in fields:
            label = QLabel(field_name)
            input_field = QLineEdit()
            input_field.setPlaceholderText(placeholder)
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.fields[field_name] = input_field
        
        buttons = QHBoxLayout()
        self.ok_button = QPushButton("تأیید")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("انصراف")
        self.cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(self.ok_button)
        buttons.addWidget(self.cancel_button)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
    
    def get_inputs(self) -> dict:
        """
        دریافت مقادیر وارد شده در فیلدها
        
        Returns:
            دیکشنری از مقادیر وارد شده
        """
        return {name: field.text() for name, field in self.fields.items()} 