from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# app을 만들어주는 함수를 지정해 주자.


def create_app():
    app = Flask(__name__)  # Flask app 만들기
    app.config['SECRET_KEY'] = 'IFP'

    from .views import views
    # blueprint 등록, '/blog' 를 기본으로 한다.
    app.register_blueprint(views, url_prefix='/blog')

    from .auth import auth
    # blueprint 등록, '/auth' 를 기본으로 한다.
    app.register_blueprint(auth, url_prefix='/auth')

    return app  # app 반환
