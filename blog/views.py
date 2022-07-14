# 홈페이지, 자기소개 페이지, 포스트 CRUD 페이지 관련 처리

from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html", name="홍길동", message="아버지를 아버지라 부르지 못하고...")


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/categories-list")
def categories_list():
    return render_template("categories_list.html")


@views.route("/post-list")
def post_list():
    return render_template("post_list.html")


@views.route('posts/<int:id>')
def post_detail():
    return render_template("post_detail.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")
