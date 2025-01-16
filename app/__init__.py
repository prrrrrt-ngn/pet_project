from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    #Регистрация блюпринта
    import app.mainmodule.controllers as mainmodule
    app.register_blueprint(mainmodule.main_module)
    return app