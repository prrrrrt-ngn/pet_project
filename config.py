import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

class DevelopmentConfig(Config):
    FLASK_DEBUG = 1

class ProductionConfig(Config):
    FLASK_DEBUG = 0