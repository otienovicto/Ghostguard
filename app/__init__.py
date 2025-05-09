from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery
from app.config import config
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__, broker=config['development'].CELERY_BROKER_URL)

def create_app(config_name='development'):
    """
    Creates and configures the Flask app with the necessary settings.
    :param config_name: The configuration name (development, production, or testing)
    :return: The configured Flask app instance
    """
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Load the app's configuration from the selected config
    app.config.from_object(config[config_name])

    # Ensure necessary email configuration is set
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'otienovictor502@gmail.com')

    # Database configuration from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ghostguard.db')

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)

    # Register blueprints
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize the database before the app is returned (try to create tables if they don't exist)
    with app.app_context():
        db.create_all()

    return app
