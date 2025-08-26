"""
Password strength evaluation utilities.

Contains functions to evaluate password strength.
"""

import re
import math


def evaluate_password_strength(password):
    """Evaluate the strength of a password.
    
    Args:
        password (str): The password to evaluate
        
    Returns:
        tuple: (score, rating, message) where:
            - score is an integer from 0-100
            - rating is one of 'ضعیف', 'متوسط', 'خوب', 'عالی'
            - message is a user-friendly message describing the strength
    """
    if not password:
        return 0, "ضعیف", "رمز عبور خالی است"
    
    # Calculate base score
    score = 0
    feedback = []
    
    # Length score (up to 40 points)
    length = len(password)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 10
    else:
        feedback.append("رمز عبور باید حداقل 8 کاراکتر باشد")
    
    # Complexity score (up to 60 points)
    # Check for different character types
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digits = bool(re.search(r'\d', password))
    has_symbols = bool(re.search(r'[^a-zA-Z0-9\s]', password))
    
    # Calculate complexity score
    complexity_score = 0
    if has_lowercase:
        complexity_score += 10
    else:
        feedback.append("استفاده از حروف کوچک توصیه می‌شود")
        
    if has_uppercase:
        complexity_score += 10
    else:
        feedback.append("استفاده از حروف بزرگ توصیه می‌شود")
        
    if has_digits:
        complexity_score += 10
    else:
        feedback.append("استفاده از اعداد توصیه می‌شود")
        
    if has_symbols:
        complexity_score += 15
    else:
        feedback.append("استفاده از کاراکترهای خاص توصیه می‌شود")
    
    # Check for variety (entropy)
    char_set_size = sum([has_lowercase * 26, has_uppercase * 26, has_digits * 10, has_symbols * 30])
    if char_set_size > 0:
        entropy = length * math.log2(char_set_size)
        if entropy > 80:
            complexity_score += 15
        elif entropy > 60:
            complexity_score += 10
        elif entropy > 40:
            complexity_score += 5
    
    score += complexity_score
    
    # Determine rating
    if score >= 80:
        rating = "عالی"
    elif score >= 60:
        rating = "خوب"
    elif score >= 40:
        rating = "متوسط"
    else:
        rating = "ضعیف"
    
    # Create message
    if feedback:
        message = f"امتیاز: {score}/100 - {' '.join(feedback[:2])}"
    else:
        message = f"امتیاز: {score}/100 - رمز عبور قوی است!"
    
    return score, rating, message 