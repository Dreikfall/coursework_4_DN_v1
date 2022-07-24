from flask import Flask
from flask_restx import Api

from app.config import Config
from app.views.auth import auth_ns
from app.setup_db import db
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from app.views.users import user_ns
from load_data import all_data_load


# функция создания основного объекта app

def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    return application


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(application):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(application, db)


# функция создания новой таблицы с добавлением записей
def create_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
        all_data_load()


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    app.run()
