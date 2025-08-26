import json
import os
from typing import List, Dict, Any, Optional, Tuple, Union
from models.contact import Contact


class ContactManager:
    """کلاس مدیریت مخاطبین"""
    
    def __init__(self, file_path: str = './Contact.json'):
        """
        سازنده کلاس مدیریت مخاطبین
        
        Args:
            file_path: مسیر فایل ذخیره‌سازی مخاطبین
        """
        self.contacts: List[Contact] = []
        self.file_path = file_path
        self.load_contacts()
    
    def load_contacts(self) -> bool:
        """
        بارگذاری مخاطبین از فایل
        
        Returns:
            نتیجه عملیات
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    data = file.read()
                    if data:
                        contacts_data = json.loads(data)
                        self.contacts = [Contact.from_dict(contact_data) for contact_data in contacts_data]
            else:
                with open(self.file_path, 'w') as file:
                    file.write(json.dumps([]))
            return True
        except Exception as e:
            print(f"Error loading contacts: {str(e)}")
            self.contacts = []
            return False
    
    def save_contacts(self) -> bool:
        """
        ذخیره‌سازی مخاطبین در فایل
        
        Returns:
            نتیجه عملیات
        """
        try:
            contacts_data = [contact.to_dict() for contact in self.contacts]
            with open(self.file_path, 'w') as file:
                file.write(json.dumps(contacts_data, indent=4))
            return True
        except Exception as e:
            print(f"Error saving contacts: {str(e)}")
            return False
    
    def add_contact(self, first_name: str, last_name: str, phone: str, email: str = None) -> Tuple[bool, str]:
        """
        افزودن مخاطب جدید
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            phone: شماره تلفن
            email: ایمیل (اختیاری)
            
        Returns:
            نتیجه عملیات و پیام
        """
        # اعتبارسنجی ورودی‌ها
        if not first_name or not last_name or not phone:
            return False, "فیلدهای ضروری خالی هستند"
        
        # بررسی وجود مخاطب تکراری
        if self.find_contact(first_name, last_name, phone):
            return False, f"مخاطب {first_name} {last_name} قبلاً وجود دارد"
        
        # ایجاد مخاطب جدید
        new_contact = Contact(first_name, last_name, phone, email)
        
        # افزودن به لیست و ذخیره‌سازی
        self.contacts.append(new_contact)
        if self.save_contacts():
            return True, f"مخاطب {first_name} {last_name} با موفقیت اضافه شد"
        return False, "خطا در ذخیره‌سازی مخاطب"
    
    def update_contact(self, first_name: str, last_name: str, 
                       new_first_name: str = None, new_last_name: str = None,
                       new_phone: str = None, new_email: str = None) -> Tuple[bool, str]:
        """
        به‌روزرسانی اطلاعات مخاطب
        
        Args:
            first_name: نام فعلی
            last_name: نام خانوادگی فعلی
            new_first_name: نام جدید (اختیاری)
            new_last_name: نام خانوادگی جدید (اختیاری)
            new_phone: شماره تلفن جدید (اختیاری)
            new_email: ایمیل جدید (اختیاری)
            
        Returns:
            نتیجه عملیات و پیام
        """
        contact = self.find_contact(first_name, last_name)
        if not contact:
            return False, f"مخاطب {first_name} {last_name} یافت نشد"
        
        # به‌روزرسانی فیلدها در صورت وجود
        if new_first_name:
            contact.first_name = new_first_name
        if new_last_name:
            contact.last_name = new_last_name
        if new_phone:
            contact.phone = new_phone
        if new_email is not None:  # چون ممکن است رشته خالی باشد
            contact.email = new_email if new_email else None
        
        # ذخیره‌سازی تغییرات
        if self.save_contacts():
            return True, f"اطلاعات مخاطب با موفقیت به‌روز شد"
        return False, "خطا در ذخیره‌سازی تغییرات"
    
    def delete_contact(self, first_name: str, last_name: str) -> Tuple[bool, str]:
        """
        حذف مخاطب
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            
        Returns:
            نتیجه عملیات و پیام
        """
        for i, contact in enumerate(self.contacts):
            if (contact.first_name.lower() == first_name.lower() and
                    contact.last_name.lower() == last_name.lower()):
                del self.contacts[i]
                if self.save_contacts():
                    return True, f"مخاطب {first_name} {last_name} با موفقیت حذف شد"
                return False, "خطا در ذخیره‌سازی تغییرات"
        return False, f"مخاطب {first_name} {last_name} یافت نشد"
    
    def find_contact(self, first_name: str, last_name: str, phone: str = None) -> Optional[Contact]:
        """
        یافتن مخاطب بر اساس نام و نام خانوادگی
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            phone: شماره تلفن (اختیاری)
            
        Returns:
            مخاطب یافت شده یا None
        """
        for contact in self.contacts:
            if (contact.first_name.lower() == first_name.lower() and
                    contact.last_name.lower() == last_name.lower()):
                if phone is None or contact.phone == phone:
                    return contact
        return None
    
    def search_contacts(self, search_term: str) -> List[Contact]:
        """
        جستجوی مخاطبین بر اساس عبارت جستجو
        
        Args:
            search_term: عبارت جستجو
            
        Returns:
            لیست مخاطبین یافت شده
        """
        if not search_term:
            return []
            
        search_term = search_term.lower()
        results = []
        
        for contact in self.contacts:
            # جستجو در تمام فیلدها
            if (search_term in contact.first_name.lower() or
                    search_term in contact.last_name.lower() or
                    search_term in contact.phone):
                results.append(contact)
            elif contact.email and search_term in contact.email.lower():
                results.append(contact)
        
        return results
    
    def add_note(self, first_name: str, last_name: str, note_text: str) -> Tuple[bool, str]:
        """
        افزودن یادداشت به مخاطب
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            note_text: متن یادداشت
            
        Returns:
            نتیجه عملیات و پیام
        """
        contact = self.find_contact(first_name, last_name)
        if not contact:
            return False, f"مخاطب {first_name} {last_name} یافت نشد"
        
        # افزودن یادداشت
        contact.add_note(note_text)
        
        # ذخیره‌سازی تغییرات
        if self.save_contacts():
            return True, f"یادداشت با موفقیت به مخاطب {first_name} {last_name} اضافه شد"
        return False, "خطا در ذخیره‌سازی یادداشت"
    
    def get_notes(self, first_name: str, last_name: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        """
        دریافت یادداشت‌های مخاطب
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            
        Returns:
            نتیجه عملیات، پیام و لیست یادداشت‌ها
        """
        contact = self.find_contact(first_name, last_name)
        if not contact:
            return False, f"مخاطب {first_name} {last_name} یافت نشد", []
        
        if contact.notes:
            return True, f"{len(contact.notes)} یادداشت یافت شد", contact.notes
        return True, "یادداشتی یافت نشد", []
    
    def delete_note(self, first_name: str, last_name: str, note_index: int) -> Tuple[bool, str]:
        """
        حذف یادداشت مخاطب
        
        Args:
            first_name: نام
            last_name: نام خانوادگی
            note_index: شماره یادداشت (از 1)
            
        Returns:
            نتیجه عملیات و پیام
        """
        contact = self.find_contact(first_name, last_name)
        if not contact:
            return False, f"مخاطب {first_name} {last_name} یافت نشد"
        
        # تبدیل از شماره‌گذاری 1 به 0
        index = note_index - 1
        
        if not contact.notes:
            return False, "مخاطب یادداشتی ندارد"
            
        if 0 <= index < len(contact.notes):
            # حذف یادداشت
            contact.delete_note(index)
            
            # ذخیره‌سازی تغییرات
            if self.save_contacts():
                return True, "یادداشت با موفقیت حذف شد"
            return False, "خطا در ذخیره‌سازی تغییرات"
        return False, f"شماره یادداشت {note_index} نامعتبر است"
    
    def export_to_csv(self, file_path: str) -> Tuple[bool, str]:
        """
        صادرات مخاطبین به فایل CSV
        
        Args:
            file_path: مسیر فایل خروجی
            
        Returns:
            نتیجه عملیات و پیام
        """
        try:
            with open(file_path, 'w') as file:
                # نوشتن سرصفحه
                file.write("First Name,Last Name,Phone,Email,Note\n")
                
                # نوشتن مخاطبین
                for contact in self.contacts:
                    first_name = contact.first_name
                    last_name = contact.last_name
                    phone = contact.phone
                    email = contact.email or ''
                    note = contact.notes[-1]['text'] if contact.notes else ''
                    
                    # اسکیپ کردن کاما در فیلدها
                    first_name = f'"{first_name}"' if ',' in first_name else first_name
                    last_name = f'"{last_name}"' if ',' in last_name else last_name
                    phone = f'"{phone}"' if ',' in phone else phone
                    email = f'"{email}"' if ',' in email else email
                    note = f'"{note}"' if ',' in note else note
                    
                    file.write(f"{first_name},{last_name},{phone},{email},{note}\n")
                    
            return True, f"{len(self.contacts)} مخاطب با موفقیت به {file_path} صادر شد"
        except Exception as e:
            return False, f"خطا در صادرات: {str(e)}"
    
    def import_from_csv(self, file_path: str) -> Tuple[bool, str, int]:
        """
        واردات مخاطبین از فایل CSV
        
        Args:
            file_path: مسیر فایل ورودی
            
        Returns:
            نتیجه عملیات، پیام و تعداد مخاطبین وارد شده
        """
        try:
            imported_count = 0
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                # رد کردن سرصفحه
                for i in range(1, len(lines)):
                    line = lines[i].strip()
                    if not line:
                        continue
                        
                    # پردازش فیلدهای دارای کاما
                    fields = []
                    in_quotes = False
                    current_field = ""
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            fields.append(current_field)
                            current_field = ""
                        else:
                            current_field += char
                    
                    # اضافه کردن آخرین فیلد
                    fields.append(current_field)
                    
                    # اطمینان از وجود حداقل 3 فیلد
                    if len(fields) < 3:
                        continue
                        
                    first_name = fields[0].strip()
                    last_name = fields[1].strip()
                    phone = fields[2].strip()
                    
                    # فیلدهای اختیاری
                    email = fields[3].strip() if len(fields) > 3 else None
                    note = fields[4].strip() if len(fields) > 4 else None
                    
                    # رد کردن مخاطبین تکراری
                    if self.find_contact(first_name, last_name, phone):
                        continue
                        
                    # ایجاد مخاطب جدید
                    new_contact = Contact(first_name, last_name, phone, email)
                    if note:
                        new_contact.add_note(note)
                        
                    self.contacts.append(new_contact)
                    imported_count += 1
            
            if imported_count > 0 and self.save_contacts():
                return True, f"{imported_count} مخاطب با موفقیت وارد شد", imported_count
            return False, "مخاطب جدیدی وارد نشد", 0
        except Exception as e:
            return False, f"خطا در واردات: {str(e)}", 0 