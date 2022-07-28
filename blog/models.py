# 데이터베이스 모델에 관한 것을 정의

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)      # id : 유일 키, Integer
    # email : 같은 이메일을 가지고 있는 유저가 없도록 함, String
    email = db.Column(db.String(150), unique=True)
    # username : 같은 이름을 가지고 있는 유저가 없도록 함, String
    username = db.Column(db.String(150), unique=True)
    # password : 비밀번호, String
    password = db.Column(db.String(150))
    # 생성일자, 기본적으로 현재가 저장되도록 함
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
