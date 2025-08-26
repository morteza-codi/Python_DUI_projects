"""
Configuration settings for the Password Generator application.

Contains various defaults and predefined settings.
"""

import string


class Config:
    """Application configuration settings."""
    
    APP_NAME = "Persian Password Generator"
    APP_VERSION = "1.0.0"
    
    # Default window dimensions
    DEFAULT_WIDTH = 1050
    DEFAULT_HEIGHT = 730
    
    # Default password lengths
    DEFAULT_PASSWORD_LENGTH = 16
    MIN_PASSWORD_LENGTH = 1
    MAX_PASSWORD_LENGTH = 100
    
    # Difficulty levels
    DIFFICULTY_LEVELS = ["Hard", "Medium", "Easy"]
    
    # Predefined character sets
    PREDEFINED_CHAR_SETS = {
        "All Characters": string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation,
        "Letters & Numbers": string.ascii_lowercase + string.ascii_uppercase + string.digits,
        "Letters Only": string.ascii_lowercase + string.ascii_uppercase,
        "Numbers Only": string.digits,
        "Lowercase Letters Only": string.ascii_lowercase,
        "Uppercase Letters Only": string.ascii_uppercase,
        "Special Characters": string.punctuation
    }
    
    # Default settings
    DEFAULT_DIFFICULTY = "Medium"
    DEFAULT_CHAR_SET = "All Characters" 