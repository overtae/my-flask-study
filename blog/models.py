# 데이터베이스 모델에 관한 것을 정의

from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


# DB 설정하기
db = SQLAlchemy()
DB_NAME = "blog_db"


class User(db.Model, UserMixin):
    # id : 유일 키, Integer
    id = db.Column(db.Integer, primary_key=True)
    # email : 같은 이메일을 가지고 있는 유저가 없도록 함, String
    email = db.Column(db.String(150), unique=True)
    # username : 같은 이름을 가지고 있는 유저가 없도록 함, String
    username = db.Column(db.String(150), unique=True)
    # password : 비밀번호, String
    password = db.Column(db.String(150))
    # 생성일자, 기본적으로 현재가 저장되도록 함
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    # 스태프 권한이 있는 유저인지 아닌지를 판별, Boolean
    is_staff = db.Column(db.Boolean, default=False)


def get_user_model():
    return User


class Post(db.Model):
    # id : 유일 키, Integer
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    # user 테이블의 id를 참조
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    # 역참조
    user = db.relationship(
        'User', backref=db.backref('posts', cascade='delete'))
    # 역참조, category 컬럼의 id를 참조
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete='CASCADE'))
    category = db.relationship(
        'Category', backref=db.backref('category', cascade='delete'))


def get_post_model():
    return Post


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}(name={self.name})>'


def get_category_model():
    return Category
