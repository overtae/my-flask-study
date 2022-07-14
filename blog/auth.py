# auth.py : 로그인, 로그아웃 등의 로그인 관련 기능 처리

from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "login"

@auth.route("/sign-up")
def signup():
    return "sign up"
