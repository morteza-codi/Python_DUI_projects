from typing import List, Dict, Any, Optional
from datetime import datetime


class Contact:
    """کلاس مدل برای نگهداری اطلاعات یک مخاطب"""
    
    def __init__(self, first_name: str, last_name: str, phone: str, email: str = None):
        """
        سازنده کلاس مخاطب
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            phone: شماره تلفن
            email: ایمیل (اختیاری)
        """
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.notes: List[Dict[str, str]] = []
    
    def add_note(self, text: str) -> Dict[str, str]:
        """
        افزودن یادداشت به مخاطب
        
        Args:
            text: متن یادداشت
            
        Returns:
            یادداشت اضافه شده
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = {
            'text': text,
            'timestamp': timestamp
        }
        self.notes.append(note)
        return note
    
    def delete_note(self, index: int) -> bool:
        """
        حذف یادداشت با شماره مشخص
        
        Args:
            index: شماره یادداشت (از 0)
            
        Returns:
            نتیجه عملیات
        """
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تبدیل مخاطب به دیکشنری برای ذخیره‌سازی
        
        Returns:
            دیکشنری حاوی اطلاعات مخاطب
        """
        result = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'number': self.phone
        }
        
        if self.email:
            result['email'] = self.email
            
        if self.notes:
            result['notes'] = self.notes
            # برای سازگاری با نسخه قبلی، یادداشت آخر را در فیلد note هم ذخیره می‌کنیم
            result['note'] = self.notes[-1]['text']
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        """
        ساخت مخاطب از دیکشنری
        
        Args:
            data: دیکشنری حاوی اطلاعات مخاطب
            
        Returns:
            شیء مخاطب ساخته شده
        """
        contact = cls(
            data['first_name'],
            data['last_name'],
            data['number'],
            data.get('email')
        )
        
        # بازیابی یادداشت‌ها
        if 'notes' in data:
            contact.notes = data['notes']
        elif 'note' in data:
            # تبدیل یادداشت تکی به فرمت آرایه
            contact.add_note(data['note'])
            
        return contact
    
    def __str__(self) -> str:
        """نمایش رشته‌ای مخاطب"""
        email_str = f", Email: {self.email}" if self.email else ""
        notes_count = f", {len(self.notes)} notes" if self.notes else ""
        return f"{self.first_name} {self.last_name} (Phone: {self.phone}{email_str}{notes_count})" 