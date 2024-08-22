import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig

def create_app():
    app = Flask(__name__)

    flask_env = os.getenv('FLASK_ENV')
    print(f'переменная окружения {flask_env}')
    
    if flask_env == 'production':
        app.config.from_object(ProductionConfig)
        print('production')
    elif flask_env == 'development':
        app.config.from_object(DevelopmentConfig)
        print('development')
    else:
        print(f'неизвестная переменная окружения {flask_env}')

    import app.mainmodule.controllers as mainmodule
    app.register_blueprint(mainmodule.main_module)
    return app