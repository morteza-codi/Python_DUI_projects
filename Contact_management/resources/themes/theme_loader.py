"""
ابزار بارگذاری تم‌های مختلف برای برنامه مدیریت مخاطبین
"""

from PyQt6.QtCore import QFile, QTextStream


def load_theme(app, theme_name):
    """
    بارگذاری یک تم بر روی برنامه
    
    Args:
        app: نمونه QApplication برنامه
        theme_name: نام تم (بدون پسوند .qss)
    
    Returns:
        bool: True اگر بارگذاری موفق بود، False در غیر این صورت
    """
    # بررسی آیا تم از دسته premium است
    if theme_name.startswith("premium_"):
        theme_path = f"resources/themes/premium/{theme_name[8:]}.qss"
    else:
        theme_path = f"resources/themes/{theme_name}.qss"
    
    # بررسی وجود فایل
    style_file = QFile(theme_path)
    if not style_file.exists():
        print(f"خطا: فایل تم '{theme_path}' یافت نشد.")
        return False
    
    # باز کردن فایل و خواندن محتوا
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        stylesheet = stream.readAll()
        app.setStyleSheet(stylesheet)
        style_file.close()
        print(f"تم '{theme_name}' با موفقیت اعمال شد.")
        return True
    else:
        print(f"خطا: نمی‌توان فایل تم '{theme_path}' را باز کرد.")
        return False


def get_available_themes():
    """
    دریافت لیست تم‌های موجود
    
    Returns:
        list: لیست نام تم‌های موجود
    """
    return [
        # تم‌های استاندارد
        "1_dark_blue",
        "2_light_blue",
        "3_dark_red",
        "4_light_red",
        "5_dark_green",
        "6_light_green",
        "7_dark_purple",
        "8_light_purple",
        "9_dark_orange",
        "10_light_orange",
        "11_dark_teal",
        "12_light_teal",
        "13_dark_pink",
        "14_light_pink",
        "15_dark_yellow",
        "16_light_yellow",
        "17_dark_gray",
        "18_light_gray",
        "19_dark_brown",
        "20_light_brown",
        
        # تم‌های پریمیوم
        "premium_1_sunset_gradient",
        "premium_2_neon_city",
        "premium_3_material_ocean",
        "premium_4_neomorphic_light",
        "premium_5_vintage_paper",
        "premium_6_forest_dreams",
        "premium_7_midnight_galaxy",
        "premium_8_candy_crush",
        "premium_9_desert_winds",
        "premium_10_deep_ocean",
        "premium_11_autumn_leaves",
        "premium_12_electric_neon",
        "premium_13_marble_gold",
        "premium_14_tropical_paradise",
        "premium_15_winter_frost",
        "premium_16_cherry_blossom",
        "premium_17_retro_wave",
        "premium_18_coffee_cream",
        "premium_19_emerald_city",
        "premium_20_cosmic_void"
    ] 