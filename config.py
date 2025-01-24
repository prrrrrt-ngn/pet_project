import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DB_CONFIG = {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "database": os.getenv('DB_NAME')
    }

    TELEGRAM = {
        "token": os.getenv('TELEGRAM_BOT_TOKEN'),
        "chat_id": os.getenv('TELEGRAM_CHAT_ID')
    }

    SECRET_KEY = os.getenv('SECRET_KEY')