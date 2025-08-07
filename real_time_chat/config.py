#!/usr/bin/env python
"""
Configuration settings for Real-Time Chat Application
"""
import os
import secrets
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Application settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'mp3', 'mp4', 'zip'}
    
    # Database settings
    DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chat_data.json')
    
    # Rate limiting settings
    RATE_LIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_HEADERS_ENABLED = True
    
    # Session settings
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Chat settings
    MAX_MESSAGE_LENGTH = 1000
    MAX_USERNAME_LENGTH = 20
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 100
    MAX_STATUS_LENGTH = 100
    MAX_BIO_LENGTH = 500
    MAX_ROOM_NAME_LENGTH = 50
    
    # Rate limits
    MESSAGE_RATE_LIMIT = 30  # messages per minute
    UPLOAD_RATE_LIMIT = 5    # uploads per 5 minutes
    LOGIN_RATE_LIMIT = 5     # login attempts per 5 minutes
    
    # Cleanup settings
    SESSION_CLEANUP_INTERVAL = timedelta(hours=1)
    SESSION_EXPIRY = timedelta(hours=24)
    MAX_MESSAGE_HISTORY = 1000
    
    # Security settings
    SANITIZE_HTML = True
    VALIDATE_FILE_TYPES = True
    LOG_SECURITY_EVENTS = True
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOST = '127.0.0.1'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # Enhanced security for production
    WTF_CSRF_ENABLED = True
    SANITIZE_HTML = True
    VALIDATE_FILE_TYPES = True
    LOG_SECURITY_EVENTS = True
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATA_FILE = ':memory:'  # Use in-memory storage for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
