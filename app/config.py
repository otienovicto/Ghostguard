import os

class Config:
    """Base configuration class with common settings."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', '2b84289c3b2646e9b32739b9290f7cbab26a3f9e6f1c7d5bc0cf3b8a893b642d')  # Use the provided SECRET_KEY from .env or fallback to a default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///ghostguard.db')  # SQLite for simplicity, change for production DB like PostgreSQL
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'otienovictor502@gmail.com')
    MAIL_DEFAULT_RECIPIENT = os.environ.get('MAIL_DEFAULT_RECIPIENT', 'admin@example.com')

    # Optional: Slack or Telegram bot configuration
    SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/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')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8161678080:AAEvPG5DhzcUwrCs1khyA0o1CnPihU37nPo')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '5890734431')

    # File storage configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Folder to store uploaded files temporarily
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}  # Allowed file extensions for upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size 16MB

    # Background job configuration (if using something like Celery)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Logs SQL queries in the console

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, use PostgreSQL or other robust databases and change the URI accordingly
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_ghostguard.db'  # Use a separate database for testing

# Dictionary to easily get configuration by environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
