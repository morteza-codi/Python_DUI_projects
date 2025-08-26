import re
from typing import Optional


class Validators:
    """کلاس اعتبارسنجی ورودی‌ها"""
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        اعتبارسنجی نام
        
        Args:
            name: نام برای اعتبارسنجی
            
        Returns:
            نتیجه اعتبارسنجی
        """
        if not name or not name.strip():
            return False
        return name.isalpha()
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        اعتبارسنجی شماره تلفن
        
        Args:
            phone: شماره تلفن برای اعتبارسنجی
            
        Returns:
            نتیجه اعتبارسنجی
        """
        if not phone or not phone.strip():
            return False
        return phone.isnumeric()
    
    @staticmethod
    def validate_email(email: Optional[str]) -> bool:
        """
        اعتبارسنجی ایمیل
        
        Args:
            email: ایمیل برای اعتبارسنجی
            
        Returns:
            نتیجه اعتبارسنجی
        """
        if not email:
            return True  # ایمیل اختیاری است
            
        # الگوی ساده برای اعتبارسنجی ایمیل
        return email.endswith('@gmail.com') or email.endswith('@yahoo.com')
    
    @staticmethod
    def validate_note(note: str) -> bool:
        """
        اعتبارسنجی یادداشت
        
        Args:
            note: یادداشت برای اعتبارسنجی
            
        Returns:
            نتیجه اعتبارسنجی
        """
        return bool(note and note.strip()) 