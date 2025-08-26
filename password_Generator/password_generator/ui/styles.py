"""
UI Styling module for the Password Generator application.

Contains style definitions and management classes.
"""


class StyleManager:
    """Manager for application styles."""
    
    # Define color palette
    PRIMARY_BG = "#FFFFFF"  # White background
    SECONDARY_BG = "#F0F0F0"  # Light gray for contrast
    PRIMARY_GREEN = "#4CAF50"  # Vibrant green
    PRIMARY_BLUE = "#2196F3"  # Bright blue
    PRIMARY_RED = "#F44336"  # Bright red
    PRIMARY_PURPLE = "#9C27B0"  # Rich purple
    TEXT_DARK = "#212121"  # Dark text for light backgrounds
    TEXT_LIGHT = "#FFFFFF"  # White text for dark backgrounds
    
    @staticmethod
    def get_main_window_style():
        """Get the main window style.
        
        Returns:
            str: CSS style for the main window.
        """
        return f"background-color: {StyleManager.PRIMARY_BG};"
    
    @staticmethod
    def get_frame_style():
        """Get the frame style.
        
        Returns:
            str: CSS style for frames.
        """
        return f"background-color: {StyleManager.SECONDARY_BG}; border-radius: 15px; border: 2px solid {StyleManager.PRIMARY_PURPLE};"
    
    @staticmethod
    def get_title_label_style():
        """Get the title label style.
        
        Returns:
            str: CSS style for title labels.
        """
        return f"""
            QLabel {{
                color: {StyleManager.TEXT_LIGHT}; 
                font-weight: bold; 
                font-size: 20px; 
                background-color: {StyleManager.PRIMARY_PURPLE}; 
                border-radius: 10px; 
                padding: 12px; 
                border: 2px solid {StyleManager.PRIMARY_BLUE}; 
                margin: 5px;
                qproperty-alignment: AlignCenter;
                min-height: 45px;
                max-width: 250px;
            }}
        """
    
    @staticmethod
    def get_regular_label_style():
        """Get the regular label style.
        
        Returns:
            str: CSS style for regular labels.
        """
        return f"color: {StyleManager.TEXT_DARK}; font-weight: bold; font-size: 16px;"
    
    @staticmethod
    def get_text_edit_style():
        """Get the text edit style.
        
        Returns:
            str: CSS style for text edits.
        """
        return f"""
            QTextEdit {{
                background-color: {StyleManager.PRIMARY_BG}; 
                color: {StyleManager.TEXT_DARK}; 
                border-radius: 8px; 
                border: 2px solid {StyleManager.PRIMARY_BLUE}; 
                padding: 10px; 
                font-size: 18px; 
                font-family: 'Courier New'; 
                font-weight: bold;
                letter-spacing: 1px;
                selection-background-color: {StyleManager.PRIMARY_GREEN};
                selection-color: {StyleManager.TEXT_LIGHT};
            }}
            QTextEdit:focus {{
                border: 3px solid {StyleManager.PRIMARY_PURPLE};
            }}
        """
    
    @staticmethod
    def get_generate_button_style():
        """Get the generate button style.
        
        Returns:
            str: CSS style for generate buttons.
        """
        return f"""
            QPushButton {{
                background-color: {StyleManager.PRIMARY_GREEN}; 
                color: {StyleManager.TEXT_LIGHT}; 
                border-radius: 10px; 
                font-weight: bold; 
                font-size: 14px; 
                padding: 8px; 
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #388E3C;
                border: 2px solid {StyleManager.PRIMARY_BLUE};
            }}
            QPushButton:pressed {{
                background-color: #2E7D32;
            }}
        """
    
    @staticmethod
    def get_copy_button_style():
        """Get the copy button style.
        
        Returns:
            str: CSS style for copy buttons.
        """
        return f"""
            QPushButton {{
                background-color: {StyleManager.PRIMARY_BLUE}; 
                color: {StyleManager.TEXT_LIGHT}; 
                border-radius: 10px; 
                font-weight: bold; 
                font-size: 14px; 
                padding: 8px; 
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
                border: 2px solid {StyleManager.PRIMARY_PURPLE};
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """
    
    @staticmethod
    def get_combo_box_style():
        """Get the combo box style.
        
        Returns:
            str: CSS style for combo boxes.
        """
        return f"""
            QComboBox {{
                background-color: {StyleManager.PRIMARY_BG}; 
                color: {StyleManager.TEXT_DARK}; 
                border-radius: 8px; 
                border: 2px solid {StyleManager.PRIMARY_BLUE}; 
                padding: 4px; 
                min-height: 30px; 
                font-weight: bold;
                font-size: 14px;
            }}
            QComboBox:hover {{
                border: 2px solid {StyleManager.PRIMARY_PURPLE};
            }}
            QComboBox QAbstractItemView {{
                background-color: {StyleManager.PRIMARY_BG};
                color: {StyleManager.TEXT_DARK};
                selection-background-color: {StyleManager.PRIMARY_BLUE};
                selection-color: {StyleManager.TEXT_LIGHT};
                border: 1px solid {StyleManager.PRIMARY_PURPLE};
            }}
        """
    
    @staticmethod
    def get_spin_box_style():
        """Get the spin box style.
        
        Returns:
            str: CSS style for spin boxes.
        """
        return f"""
            QSpinBox {{
                background-color: {StyleManager.PRIMARY_BG}; 
                color: {StyleManager.TEXT_DARK}; 
                border-radius: 8px; 
                border: 2px solid {StyleManager.PRIMARY_BLUE}; 
                padding: 4px; 
                min-height: 30px; 
                min-width: 70px;
                font-weight: bold;
                font-size: 16px;
            }}
            QSpinBox:hover {{
                border: 2px solid {StyleManager.PRIMARY_PURPLE};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {StyleManager.PRIMARY_BLUE};
                border-radius: 4px;
                width: 20px;
                height: 14px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {StyleManager.PRIMARY_PURPLE};
            }}
        """
    
    @staticmethod
    def get_status_bar_style():
        """Get the status bar style.
        
        Returns:
            str: CSS style for the status bar.
        """
        return f"""
            QStatusBar {{
                background-color: {StyleManager.SECONDARY_BG};
                color: {StyleManager.TEXT_DARK};
                font-weight: bold;
                padding: 5px;
                border-top: 1px solid {StyleManager.PRIMARY_PURPLE};
            }}
        """
        
    @staticmethod
    def get_menu_bar_style():
        """Get the menu bar style.
        
        Returns:
            str: CSS style for the menu bar.
        """
        return f"""
            QMenuBar {{
                background-color: {StyleManager.PRIMARY_PURPLE};
                color: {StyleManager.TEXT_LIGHT};
                font-weight: bold;
                font-size: 16px;
                padding: 8px;
                border-bottom: 2px solid {StyleManager.PRIMARY_BLUE};
            }}
            QMenuBar::item {{
                background-color: {StyleManager.PRIMARY_PURPLE};
                color: {StyleManager.TEXT_LIGHT};
                padding: 8px 15px;
                margin: 0px 5px;
                border-radius: 8px;
            }}
            QMenuBar::item:selected {{
                background-color: #7B1FA2;
                border: 2px solid {StyleManager.TEXT_LIGHT};
            }}
            QMenu {{
                background-color: {StyleManager.PRIMARY_BG};
                color: {StyleManager.TEXT_DARK};
                font-size: 14px;
                font-weight: bold;
                border: 2px solid {StyleManager.PRIMARY_PURPLE};
                padding: 5px;
                min-width: 150px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                margin: 2px 5px;
            }}
            QMenu::item:selected {{
                background-color: {StyleManager.PRIMARY_BLUE};
                color: {StyleManager.TEXT_LIGHT};
                border-radius: 5px;
            }}
        """
        
    @staticmethod
    def get_progress_bar_style():
        """Get the progress bar style.
        
        Returns:
            str: CSS style for progress bars.
        """
        return f"""
            QProgressBar {{
                border: 2px solid {StyleManager.PRIMARY_BLUE};
                border-radius: 5px;
                text-align: center;
                background-color: {StyleManager.PRIMARY_BG};
            }}
            QProgressBar::chunk {{
                background-color: {StyleManager.PRIMARY_GREEN};
                width: 10px;
                margin: 0.5px;
            }}
        """ 