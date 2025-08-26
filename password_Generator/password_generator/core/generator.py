"""
Password Generator Core Module.

Contains the core functionality for password generation.
"""

import random
import string
from abc import ABC, abstractmethod


class PasswordGenerator(ABC):
    """Abstract base class for password generators."""
    
    @abstractmethod
    def generate(self):
        """Generate a password.
        
        Returns:
            str: The generated password.
        """
        pass


class DifficultyPasswordGenerator(PasswordGenerator):
    """Generate passwords based on difficulty level."""
    
    DIFFICULTY_LENGTHS = {
        "Hard": 32,
        "Medium": 16,
        "Easy": 8
    }
    
    def __init__(self, difficulty="Medium"):
        """Initialize with difficulty level.
        
        Args:
            difficulty (str): Difficulty level ('Easy', 'Medium', 'Hard')
        """
        self.difficulty = difficulty
        self.char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
    def generate(self):
        """Generate a password based on difficulty level.
        
        Returns:
            str: The generated password.
        """
        length = self.DIFFICULTY_LENGTHS.get(self.difficulty, 16)  # Default to Medium if not found
        result = random.choices(self.char_set, k=length)
        return "".join(result)


class CustomLengthPasswordGenerator(PasswordGenerator):
    """Generate passwords with custom length."""
    
    def __init__(self, length=16):
        """Initialize with desired password length.
        
        Args:
            length (int): Desired password length.
        """
        self.length = length
        self.char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
    def generate(self):
        """Generate a password with custom length.
        
        Returns:
            str: The generated password.
        
        Raises:
            ValueError: If length is less than or equal to 0.
        """
        if self.length <= 0:
            raise ValueError("Password length must be greater than 0")
            
        result = random.choices(self.char_set, k=self.length)
        return "".join(result)


class CustomCharSetPasswordGenerator(PasswordGenerator):
    """Generate passwords with custom character set."""
    
    def __init__(self, char_set, length=16):
        """Initialize with custom character set and length.
        
        Args:
            char_set (str): Custom character set to use.
            length (int): Desired password length.
        """
        self.char_set = char_set
        self.length = length
    
    def generate(self):
        """Generate a password with custom character set and length.
        
        Returns:
            str: The generated password.
        
        Raises:
            ValueError: If length is less than or equal to 0 or char_set is empty.
        """
        if self.length <= 0:
            raise ValueError("Password length must be greater than 0")
            
        if not self.char_set:
            raise ValueError("Character set cannot be empty")
            
        result = random.choices(self.char_set, k=self.length)
        return "".join(result) 