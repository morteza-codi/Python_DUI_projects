import random

class GameLogic:
    """کلاس مدیریت منطق بازی حدس عدد"""
    
    def __init__(self, message_handler, ui):
        """مقداردهی اولیه با مدیریت پیام و رابط کاربری"""
        self.message_handler = message_handler
        self.ui = ui
        
        # مقادیر پیش‌فرض بازی
        self.range_start = 0  # بازه شروع
        self.range_end = 0    # بازه پایان
        self.chances = 5      # تعداد شانس‌ها
        self.guess = 0        # حدس کاربر
        self.target_number = 0  # عدد مخفی
        self.game_initialized = False  # وضعیت شروع بازی
        
        # فعال‌سازی دکمه‌ها
        self.connect_buttons()
        
        # نمایش پیام خوش‌آمدگویی
        self.message_handler.show_welcome_message()
        self.message_handler.show_result_welcome()
    
    def connect_buttons(self):
        """اتصال دکمه‌ها به توابع مربوطه"""
        self.ui.btn_1.clicked.connect(self.set_range_start)
        self.ui.btn_2.clicked.connect(self.set_range_end)
        self.ui.btn_3.clicked.connect(self.set_chances)
        self.ui.btn_4.clicked.connect(self.set_guess)
        self.ui.btn_5.clicked.connect(self.check_guess)
        
        # اتصال منوی درباره
        if hasattr(self.ui, 'actionabout'):
            self.ui.actionabout.triggered.connect(self.show_about)
    
    def show_about(self):
        """نمایش اطلاعات درباره بازی"""
        self.message_handler.show_about_message()
    
    def initialize_game(self):
        """آماده‌سازی بازی با تولید عدد تصادفی"""
        if self.range_start > 0 and self.range_end > 0 and self.range_start < self.range_end:
            self.target_number = random.randint(self.range_start, self.range_end)
            self.game_initialized = True
            self.message_handler.show_info_message(f"بازی آماده شد! عدد مخفی بین {self.range_start} و {self.range_end} انتخاب شد")
            return True
        return False
    
    def set_range_start(self):
        """تنظیم عدد ابتدای بازه"""
        self.message_handler.show_button_message("بازه اول")
        
        text = self.ui.textEdit_1.toPlainText()
        if text == "":
            self.message_handler.show_error_message("بازه اول رو وارد کنید")
            return
            
        if not text.isnumeric():
            self.message_handler.show_error_message("لطفا در بازه اول عدد وارد کنید")
            return
            
        self.range_start = int(text)
        self.message_handler.show_success_message("بازه اول ثبت شد")
        
        # آماده‌سازی مجدد بازی در صورت تغییر بازه
        self.game_initialized = False
        
        # افزودن افکت هایلایت به ورودی
        self.ui.textEdit_1.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2ecc71;
                border-radius: 8px;
                background-color: #f0fff0;
                padding: 5px;
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        
        # تلاش برای راه‌اندازی خودکار بازی
        self.try_initialize_game()
    
    def set_range_end(self):
        """تنظیم عدد انتهای بازه"""
        self.message_handler.show_button_message("بازه دوم")
        
        text = self.ui.textEdit_2.toPlainText()
        if text == "":
            self.message_handler.show_error_message("بازه دوم رو وارد کنید")
            return
            
        if not text.isnumeric():
            self.message_handler.show_error_message("لطفا در بازه دوم عدد وارد کنید")
            return
            
        if int(text) <= self.range_start:
            self.message_handler.show_error_message("عدد بزرگتر از بازه اول وارد کنید")
            # نمایش هایلایت خطا روی ورودی
            self.ui.textEdit_2.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                    background-color: #fff0f0;
                    padding: 5px;
                    font-size: 14px;
                    color: #c0392b;
                    font-weight: bold;
                }
            """)
            return
            
        self.range_end = int(text)
        self.message_handler.show_success_message("بازه دوم ثبت شد")
        
        # آماده‌سازی مجدد بازی در صورت تغییر بازه
        self.game_initialized = False
        
        # افزودن افکت هایلایت به ورودی
        self.ui.textEdit_2.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2ecc71;
                border-radius: 8px;
                background-color: #f0fff0;
                padding: 5px;
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        
        # تلاش برای راه‌اندازی خودکار بازی
        self.try_initialize_game()
    
    def try_initialize_game(self):
        """تلاش برای راه‌اندازی خودکار بازی اگر همه شرایط مهیا باشد"""
        if not self.game_initialized and self.range_start > 0 and self.range_end > 0:
            self.initialize_game()
    
    def set_chances(self):
        """تنظیم تعداد شانس‌ها"""
        self.message_handler.show_button_message("تعداد شانس")
        
        text = self.ui.textEdit_3.toPlainText()
        if text == "":
            self.ui.label_2.setText(str(self.chances))
            return
            
        if not text.isnumeric():
            self.message_handler.show_error_message("برای تعداد شانس عدد وارد کنید")
            # نمایش هایلایت خطا روی ورودی
            self.ui.textEdit_3.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                    background-color: #fff0f0;
                    padding: 5px;
                    font-size: 14px;
                    color: #c0392b;
                    font-weight: bold;
                }
            """)
            return
            
        # بررسی ورودی صحیح برای تعداد شانس
        chance_value = int(text)
        if chance_value <= 0:
            self.message_handler.show_error_message("تعداد شانس باید حداقل 1 باشد")
            return
            
        if chance_value > 20:
            self.message_handler.show_error_message("حداکثر تعداد شانس 20 است")
            return
        
        self.chances = chance_value
        self.ui.label_2.setText(str(self.chances))
        self.message_handler.show_success_message("تعداد شانس ثبت شد")
        
        # افزودن افکت هایلایت به ورودی
        self.ui.textEdit_3.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2ecc71;
                border-radius: 8px;
                background-color: #f0fff0;
                padding: 5px;
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        
        # به‌روزرسانی نشانگر شانس با انیمیشن
        self.ui.label_2.setStyleSheet("""
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
    
    def set_guess(self):
        """تنظیم حدس کاربر"""
        self.message_handler.show_button_message("عدد حدس")
        
        # بررسی آماده بودن بازی
        if not self.game_initialized:
            if not self.initialize_game():
                self.message_handler.show_error_message("لطفا ابتدا بازه‌های عددی را مشخص کنید")
                return
        
        text = self.ui.textEdit_4.toPlainText()
        if text == "":
            self.message_handler.show_error_message("عدد مدنظرتون رو وارد کنید")
            return
            
        if not text.isnumeric():
            self.message_handler.show_error_message("عدد مدنظرتون باید عدد باشه")
            # نمایش هایلایت خطا روی ورودی
            self.ui.textEdit_4.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                    background-color: #fff0f0;
                    padding: 5px;
                    font-size: 14px;
                    color: #c0392b;
                    font-weight: bold;
                }
            """)
            return
            
        user_num = int(text)
        if user_num < self.range_start or user_num > self.range_end:
            self.message_handler.show_error_message(f"عدد باید بین {self.range_start} و {self.range_end} باشه")
            # نمایش هایلایت خطا روی ورودی
            self.ui.textEdit_4.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                    background-color: #fff0f0;
                    padding: 5px;
                    font-size: 14px;
                    color: #c0392b;
                    font-weight: bold;
                }
            """)
            return
            
        self.guess = user_num
        self.message_handler.show_success_message("عدد ثبت شد")
        
        # افزودن افکت هایلایت به ورودی
        self.ui.textEdit_4.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2ecc71;
                border-radius: 8px;
                background-color: #f0fff0;
                padding: 5px;
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        
        # هایلایت دکمه بررسی با افکت انیمیشن
        self.ui.btn_5.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #f39c12, stop:1 #e67e22);
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
                                         stop:0 #e67e22, stop:1 #d35400);
            }
        """)
    
    def check_guess(self):
        """بررسی حدس کاربر و مقایسه با عدد مخفی"""
        self.message_handler.show_button_message("بررسی حدس")
        
        # بررسی آماده بودن بازی
        if not self.game_initialized:
            if not self.initialize_game():
                self.message_handler.show_error_message("لطفا ابتدا بازه‌های عددی را مشخص کنید")
                return
                
        if self.guess == 0:
            self.message_handler.show_error_message("لطفا ابتدا حدس خود را وارد کنید")
            return

        # مقایسه با عدد هدف
        if self.target_number == self.guess:
            self.handle_correct_guess()
        else:
            self.handle_incorrect_guess()
    
    def handle_correct_guess(self):
        """مدیریت حالت حدس صحیح"""
        self.message_handler.show_win_result()
        self.reset_game()
        self.message_handler.show_success_message("تبریک! شما برنده شدید")
    
    def handle_incorrect_guess(self):
        """مدیریت حالت حدس اشتباه"""
        is_higher = self.guess > self.target_number
        
        if is_higher:
            self.message_handler.show_hint_message("عدد شما بزرگتر از عدد مخفی است", True)
        else:
            self.message_handler.show_hint_message("عدد شما کوچکتر از عدد مخفی است", False)
            
        self.chances -= 1
        self.ui.label_2.setText(str(self.chances))
        
        # به‌روزرسانی استایل نشانگر شانس بر اساس شانس‌های باقیمانده
        self.update_chances_indicator()
        
        self.message_handler.show_incorrect_result(self.chances, is_higher)
        self.ui.textEdit_4.clear()
        self.reset_button_style()
        
        # بازگرداندن استایل پیش‌فرض برای فیلد حدس
        self.ui.textEdit_4.setStyleSheet("""
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
        
        if self.chances <= 0:
            self.handle_game_over()
    
    def handle_game_over(self):
        """مدیریت حالت پایان بازی (اتمام شانس‌ها)"""
        self.message_handler.show_lose_result(self.target_number)
        self.reset_game()
        self.message_handler.show_error_message(f"بازی تمام شد. عدد درست {self.target_number} بود")
        
        # بازنشانی استایل نشانگر شانس
        self.ui.label_2.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                font-size: 22px;
                font-weight: bold;
                background-color: #f9f9f9;
                border: 2px solid #e74c3c;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
    
    def update_chances_indicator(self):
        """به‌روزرسانی نشانگر شانس‌های باقیمانده"""
        if self.chances <= 2:
            self.ui.label_2.setStyleSheet("""
                QLabel {
                    color: #c0392b;
                    font-size: 22px;
                    font-weight: bold;
                    background-color: #ffebee;
                    border: 2px solid #c0392b;
                    border-radius: 10px;
                    padding: 3px 10px;
                }
            """)
        else:
            self.ui.label_2.setStyleSheet("""
                QLabel {
                    color: #e67e22;
                    font-size: 22px;
                    font-weight: bold;
                    background-color: #fff8e1;
                    border: 2px solid #e67e22;
                    border-radius: 10px;
                    padding: 3px 10px;
                }
            """)
    
    def reset_button_style(self):
        """بازنشانی استایل دکمه به حالت پیش‌فرض"""
        self.ui.btn_5.setStyleSheet("""
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
    
    def reset_game(self):
        """بازنشانی بازی به حالت اولیه"""
        self.ui.textEdit_1.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()
        self.ui.textEdit_4.clear()
        self.range_start = 0
        self.range_end = 0
        self.chances = 5
        self.game_initialized = False
        self.ui.label_2.setText(str(self.chances))
        self.reset_input_styles()
    
    def reset_input_styles(self):
        """بازنشانی استایل همه ورودی‌ها به حالت پیش‌فرض"""
        input_style = """
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
        """
        self.ui.textEdit_1.setStyleSheet(input_style)
        self.ui.textEdit_2.setStyleSheet(input_style)
        self.ui.textEdit_3.setStyleSheet(input_style)
        self.ui.textEdit_4.setStyleSheet(input_style) 