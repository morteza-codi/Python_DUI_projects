class MessageHandler:
    """کلاس مدیریت پیام‌های برنامه و نمایش محتوای HTML"""
    
    def __init__(self, status_text_edit, result_text_edit):
        """مقداردهی اولیه با ویجت‌های نمایش پیام"""
        self.status_text_edit = status_text_edit
        self.result_text_edit = result_text_edit
    
    def show_welcome_message(self):
        """نمایش پیام خوش‌آمدگویی جذاب"""
        welcome_html = """
        <div style='text-align: center; color: #2980b9;'>
            <span style='font-size: 14pt; font-weight: bold;'>به بازی حدس عدد خوش آمدید!</span><br>
            <span style='color: #2c3e50; font-size: 10pt;'>برای شروع، بازه‌های عددی را وارد کنید</span>
        </div>
        """
        self.status_text_edit.setHtml(welcome_html)
    
    def show_result_welcome(self):
        """نمایش پیام خوش‌آمدگویی در بخش نتیجه"""
        welcome_html = """
        <div style='text-align: center;'>
            <span style='font-size: 14pt; color: #e67e22; font-weight: bold;'>🎮 بازی حدس عدد</span><br>
            <span style='color: #2c3e50; font-size: 11pt; font-weight: bold;'>
                یک عدد در محدوده تعیین شده حدس بزنید.<br>
                آیا می‌توانید عدد مخفی را پیدا کنید؟
            </span><br>
            <span style='color: #34495e; font-size: 10pt;'>
                راهنمایی: ابتدا بازه‌های عددی را تعیین کنید، سپس حدس خود را وارد کنید!
            </span>
        </div>
        """
        self.result_text_edit.setHtml(welcome_html)

    def show_about_message(self):
        """نمایش اطلاعات درباره بازی"""
        about_html = """
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 18pt; color: #3498db; font-weight: bold; margin-bottom: 10px;'>
                🎲 بازی حدس عدد
            </div>
            <div style='font-size: 12pt; color: #2c3e50; margin: 15px 0;'>
                نسخه 2.0
            </div>
            <div style='font-size: 12pt; color: #2c3e50; margin-bottom: 10px;'>
                این بازی با استفاده از PyQt6 طراحی شده است
            </div>
            <div style='font-size: 11pt; color: #7f8c8d; margin-top: 20px;'>
                © تمامی حقوق محفوظ است
            </div>
        </div>
        """
        self.result_text_edit.setHtml(about_html)
        self.status_text_edit.setHtml("""
        <div style='text-align: center; color: #3498db;'>
            <span style='font-size: 12pt; font-weight: bold;'>ℹ️ درباره بازی</span>
        </div>
        """)

    def show_error_message(self, message):
        """نمایش پیام خطا با استایل قرمز"""
        error_html = f"""
        <div style='text-align: center; color: #c0392b;'>
            <span style='font-size: 12pt; font-weight: bold;'>⚠️ {message}</span>
        </div>
        """
        self.status_text_edit.setHtml(error_html)
        
    def show_success_message(self, message):
        """نمایش پیام موفقیت با استایل سبز"""
        success_html = f"""
        <div style='text-align: center; color: #27ae60;'>
            <span style='font-size: 12pt; font-weight: bold;'>✅ {message}</span>
        </div>
        """
        self.status_text_edit.setHtml(success_html)
        
    def show_info_message(self, message):
        """نمایش پیام اطلاعات با استایل آبی"""
        info_html = f"""
        <div style='text-align: center; color: #2980b9;'>
            <span style='font-size: 12pt; font-weight: bold;'>ℹ️ {message}</span>
        </div>
        """
        self.status_text_edit.setHtml(info_html)
        
    def show_hint_message(self, message, is_higher):
        """نمایش پیام راهنما برای بزرگتر/کوچکتر بودن"""
        icon = "📈" if is_higher else "📉"
        color = "#8e44ad" if is_higher else "#d35400"
        
        hint_html = f"""
        <div style='text-align: center; color: {color};'>
            <span style='font-size: 12pt; font-weight: bold;'>{icon} {message}</span>
        </div>
        """
        self.status_text_edit.setHtml(hint_html)
        
    def show_button_message(self, button_name):
        """نمایش پیام ثبت دکمه با استایل‌دهی"""
        button_html = f"""
        <div style='text-align: center; color: #2980b9;'>
            <span style='font-size: 12pt; font-weight: bold;'>🔘 دکمه {button_name} ثبت شد</span>
        </div>
        """
        self.status_text_edit.setHtml(button_html)
    
    def show_win_result(self):
        """نمایش پیام برد جذاب در بخش نتیجه"""
        win_html = """
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 18pt; color: #27ae60; font-weight: bold; margin-bottom: 10px;'>
                🎉 تبریک! شما برنده شدید 🎉
            </div>
            <div style='font-size: 12pt; color: #16a085; font-weight: bold;'>
                عدد مخفی را به درستی حدس زدید
            </div>
            <div style='margin-top: 20px; font-size: 10pt; color: #34495e;'>
                برای شروع مجدد بازی، محدوده و حدس جدیدی وارد کنید
            </div>
        </div>
        """
        self.result_text_edit.setHtml(win_html)
    
    def show_lose_result(self, correct_number):
        """نمایش پیام باخت جذاب در بخش نتیجه"""
        lose_html = f"""
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 18pt; color: #c0392b; font-weight: bold; margin-bottom: 10px;'>
                😢 متأسفانه شما باختید! 
            </div>
            <div style='font-size: 12pt; color: #e74c3c; font-weight: bold;'>
                شانس‌های شما تمام شد
            </div>
            <div style='font-size: 16pt; color: #2c3e50; margin: 15px 0; font-weight: bold;'>
                عدد مخفی <span style='color: #d35400; font-weight: bold;'>{correct_number}</span> بود
            </div>
            <div style='margin-top: 20px; font-size: 10pt; color: #34495e;'>
                برای شروع مجدد بازی، محدوده و حدس جدیدی وارد کنید
            </div>
        </div>
        """
        self.result_text_edit.setHtml(lose_html)
    
    def show_incorrect_result(self, remaining_chances, is_higher):
        """نمایش نتیجه حدس نادرست با استایل جذاب"""
        direction = "بزرگتر" if is_higher else "کوچکتر"
        icon = "📈" if is_higher else "📉"
        color = "#8e44ad" if is_higher else "#d35400"
        
        incorrect_html = f"""
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 16pt; color: #c0392b; font-weight: bold; margin-bottom: 10px;'>
                ❌ حدس اشتباه بود!
            </div>
            <div style='font-size: 14pt; color: {color}; margin: 10px 0; font-weight: bold;'>
                {icon} عدد شما <span style='font-weight: bold;'>{direction}</span> از عدد مخفی است
            </div>
            <div style='font-size: 12pt; color: #2c3e50; margin-top: 15px; font-weight: bold;'>
                فرصت‌های باقیمانده: <span style='color: #e74c3c; font-weight: bold;'>{remaining_chances}</span>
            </div>
            <div style='margin-top: 15px; font-size: 10pt; color: #34495e;'>
                دوباره تلاش کنید!
            </div>
        </div>
        """
        self.result_text_edit.setHtml(incorrect_html) 