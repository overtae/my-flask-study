# 홈페이지, 자기소개 페이지, 포스트 CRUD 페이지 관련 처리

from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html", name="홍길동", message="아버지를 아버지라 부르지 못하고...")


@views.route("/about")
def about():
    return "about me"

