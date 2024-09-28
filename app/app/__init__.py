from flask import Flask
from .models import engine, Base

def create_app():
    app = Flask(__name__)

    # Настройка конфигурации
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Создание базы данных и таблиц
    Base.metadata.create_all(engine)

    # Импорт маршрутов
    from .routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
