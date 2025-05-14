from flask import Flask
from config import Config
from threading import Thread
from app.telegram_bot.bot import start_bot
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Запуск бота в отдельном потоке
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        bot_thread = Thread(target=start_bot, daemon=True)
        bot_thread.start()

    # Регистрация блюпринта
    import app.mainmodule.controllers as mainmodule
    app.register_blueprint(mainmodule.main_module)
    
    return app