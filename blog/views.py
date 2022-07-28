# 홈페이지, 자기소개 페이지, 포스트 CRUD 페이지 관련 처리

from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("index.html", user=current_user)


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)


@views.route("/categories-list")
def categories_list():
    return render_template("categories_list.html", user=current_user)


@views.route("/post-list")
def post_list():
    return render_template("post_list.html", user=current_user)


@views.route('posts/<int:id>')
def post_detail():
    return render_template("post_detail.html", user=current_user)


@views.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)
