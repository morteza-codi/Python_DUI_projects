from PyQt6 import QtCore, QtGui, QtWidgets
from ui_components import LabelComponent, InputComponent, ButtonComponent


class CustomUI:
    """کلاس رابط کاربری سفارشی‌شده برای بازی حدس عدد"""
    
    def __init__(self):
        """مقداردهی اولیه اجزای رابط کاربری"""
        self.label_component = LabelComponent()
        self.input_component = InputComponent()
        self.button_component = ButtonComponent()
    
    def setup_ui(self, main_window):
        """راه‌اندازی رابط کاربری"""
        main_window.setObjectName("MainWindow")
        main_window.resize(564, 746)
        font = QtGui.QFont()
        font.setPointSize(18)
        main_window.setFont(font)
        
        # تنظیم آیکون برنامه
        icon = QtGui.QIcon()
        icon.addFile("icon.png", QtCore.QSize(64, 64))
        main_window.setWindowIcon(icon)
        
        # تنظیم گرادیان رنگی پس‌زمینه برنامه
        main_window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #f5f7fa, stop:1 #e6eef8);
            }
        """)
        main_window.setWindowOpacity(0.95)
        main_window.setWindowTitle("بازی حدس عدد")
        
        # ایجاد ویجت مرکزی
        self.centralwidget = QtWidgets.QWidget(parent=main_window)
        self.centralwidget.setObjectName("centralwidget")
        
        # استایل‌دهی به کانتینر اصلی بازی
        self.centralwidget.setStyleSheet("""
            QWidget {
                border-radius: 10px;
            }
        """)
        
        # ایجاد برچسب‌ها
        self.label_1 = self.label_component.create_title_label(
            self.centralwidget, 
            " تعداد شانس :",
            QtCore.QRect(255, 20, 161, 31)
        )
        self.label_1.setObjectName("label_1")
        
        self.label_2 = self.label_component.create_counter_label(
            self.centralwidget,
            QtCore.QRect(180, 10, 81, 51)
        )
        self.label_2.setObjectName("label_2")
        
        # خط افقی تقسیم کننده
        self.horizontal_line = QtWidgets.QFrame(parent=self.centralwidget)
        self.horizontal_line.setGeometry(QtCore.QRect(50, 400, 464, 20))
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.horizontal_line.setLineWidth(2)
        self.horizontal_line.setStyleSheet("color: #3498db; border: 2px solid #3498db;")
        self.horizontal_line.setObjectName("horizontal_line")
        
        # ایجاد ویجت‌های ورودی
        # ویجت ورودی بازه اول
        self.widget4 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget4.setGeometry(QtCore.QRect(150, 101, 291, 61))
        self.widget4.setObjectName("widget4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.textEdit_1 = self.input_component.create_text_input(
            self.widget4,
            "عدد ابتدای بازه را وارد کنید..."
        )
        self.textEdit_1.setObjectName("textEdit_1")
        self.horizontalLayout.addWidget(self.textEdit_1)
        
        self.btn_1 = self.button_component.create_standard_button(
            self.widget4,
            "ثبت"
        )
        self.btn_1.setObjectName("btn_1")
        self.btn_1.setShortcut("Ctrl+1")  # کلید میانبر
        self.btn_1.setToolTip("ثبت بازه اول (Ctrl+1)")
        self.horizontalLayout.addWidget(self.btn_1)
        
        # ویجت ورودی بازه دوم
        self.widget3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(150, 170, 291, 61))
        self.widget3.setObjectName("widget3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.textEdit_2 = self.input_component.create_text_input(
            self.widget3,
            "عدد انتهای بازه را وارد کنید..."
        )
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_2.addWidget(self.textEdit_2)
        
        self.btn_2 = self.button_component.create_standard_button(
            self.widget3,
            "ثبت"
        )
        self.btn_2.setObjectName("btn_2")
        self.btn_2.setShortcut("Ctrl+2")  # کلید میانبر
        self.btn_2.setToolTip("ثبت بازه دوم (Ctrl+2)")
        self.horizontalLayout_2.addWidget(self.btn_2)
        
        # ویجت ورودی تعداد شانس
        self.widget2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(150, 240, 291, 61))
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
        self.textEdit_3 = self.input_component.create_text_input(
            self.widget2,
            "تعداد شانس‌ها را وارد کنید..."
        )
        self.textEdit_3.setObjectName("textEdit_3")
        self.horizontalLayout_3.addWidget(self.textEdit_3)
        
        self.btn_3 = self.button_component.create_standard_button(
            self.widget2,
            "ثبت"
        )
        self.btn_3.setObjectName("btn_3")
        self.btn_3.setShortcut("Ctrl+3")  # کلید میانبر
        self.btn_3.setToolTip("ثبت تعداد شانس (Ctrl+3)")
        self.horizontalLayout_3.addWidget(self.btn_3)
        
        # ویجت ورودی حدس کاربر
        self.widget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(100, 341, 371, 61))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.textEdit_4 = self.input_component.create_text_input(
            self.widget1,
            "حدس خود را وارد کنید..."
        )
        self.textEdit_4.setObjectName("textEdit_4")
        self.horizontalLayout_4.addWidget(self.textEdit_4)
        
        self.btn_4 = self.button_component.create_standard_button(
            self.widget1,
            "ثبت"
        )
        self.btn_4.setObjectName("btn_4")
        self.btn_4.setShortcut("Ctrl+4")  # کلید میانبر
        self.btn_4.setToolTip("ثبت حدس (Ctrl+4)")
        self.horizontalLayout_4.addWidget(self.btn_4)
        
        # ویجت نمایش نتیجه و دکمه بررسی
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(70, 450, 431, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        
        self.textEdit_5 = self.input_component.create_result_display(
            self.widget,
            "نتیجه بازی اینجا نمایش داده می‌شود..."
        )
        self.textEdit_5.setObjectName("textEdit_5")
        self.horizontalLayout_6.addWidget(self.textEdit_5)
        
        self.btn_5 = self.button_component.create_primary_button(
            self.widget,
            "بررسی"
        )
        self.btn_5.setObjectName("btn_5")
        self.btn_5.setShortcut("Return")  # کلید میانبر Enter
        self.btn_5.setToolTip("بررسی حدس (Enter)")
        self.horizontalLayout_6.addWidget(self.btn_5)
        
        # ویجت نمایش پیام‌های خطا و وضعیت
        self.widget_status = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_status.setGeometry(QtCore.QRect(70, 560, 431, 72))
        self.widget_status.setObjectName("widget_status")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_status)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        
        self.textEdit_6 = self.input_component.create_status_display(
            self.widget_status,
            "مشکلات"
        )
        self.textEdit_6.setObjectName("textEdit_6")
        self.horizontalLayout_5.addWidget(self.textEdit_6)
        
        self.label_3 = QtWidgets.QLabel(parent=self.widget_status)
        self.label_3.setText("مدیریت خطا : ")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        
        # دکمه راهنما
        self.help_button = self.button_component.create_standard_button(
            self.centralwidget,
            "راهنما"
        )
        self.help_button.setGeometry(QtCore.QRect(70, 640, 100, 30))
        self.help_button.setObjectName("help_button")
        self.help_button.setShortcut("F1")  # کلید میانبر F1
        self.help_button.setToolTip("نمایش راهنما (F1)")
        
        # دکمه شروع مجدد
        self.restart_button = self.button_component.create_standard_button(
            self.centralwidget,
            "شروع مجدد"
        )
        self.restart_button.setGeometry(QtCore.QRect(400, 640, 100, 30))
        self.restart_button.setObjectName("restart_button")
        self.restart_button.setShortcut("F5")  # کلید میانبر F5
        self.restart_button.setToolTip("شروع مجدد بازی (F5)")
        
        # تنظیم منوی برنامه
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 564, 35))
        self.menubar.setObjectName("menubar")
        
        self.menuabout = QtWidgets.QMenu(parent=self.menubar)
        self.menuabout.setTitle("درباره")
        self.menuabout.setObjectName("menuabout")
        
        self.menu_game = QtWidgets.QMenu(parent=self.menubar)
        self.menu_game.setTitle("بازی")
        self.menu_game.setObjectName("menu_game")
        
        main_window.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        
        # اکشن‌های منو
        self.actionabout = QtGui.QAction(parent=main_window)
        self.actionabout.setText("درباره بازی")
        self.actionabout.setObjectName("actionabout")
        self.actionabout.setShortcut("Ctrl+I")
        
        self.action_restart = QtGui.QAction(parent=main_window)
        self.action_restart.setText("شروع مجدد")
        self.action_restart.setObjectName("action_restart")
        self.action_restart.setShortcut("F5")
        
        self.action_exit = QtGui.QAction(parent=main_window)
        self.action_exit.setText("خروج")
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setShortcut("Alt+F4")
        
        # اضافه کردن اکشن‌ها به منو
        self.menuabout.addAction(self.actionabout)
        self.menu_game.addAction(self.action_restart)
        self.menu_game.addSeparator()
        self.menu_game.addAction(self.action_exit)
        
        self.menubar.addAction(self.menu_game.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())
        
        # اتصال سیگنال‌ها به اسلات‌ها در کلاس اصلی
        QtCore.QMetaObject.connectSlotsByName(main_window) 