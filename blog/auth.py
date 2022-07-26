# auth.py : 로그인, 로그아웃 등의 로그인 관련 기능 처리

from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from blog import db
from blog.forms import SignupForm
from blog.models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])  # 로그인에서 POST 요청을 처리해야 함.
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return redirect("views.blog_home")  # 로그아웃하면 views의 blog_home으로 리다이렉트됨


@auth.route("/sign-up", methods=['GET', 'POST'])  # 회원가입에서 POST 요청을 처리해야 함.
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        # 폼으로부터 검증된 데이터 받아오기
        signup_user = User(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(form.password1.data),
        )

        # 폼에서 받아온 데이터가 데이터베이스에 이미 존재하는지 확인
        email_exists = User.query.filter_by(email=form.email.data).first()
        username_exists = User.query.filter_by(username=form.username.data).first()

        # 이메일 중복 검사
        if email_exists:
            flash('Email is already in use...', category='error')
        # 유저네임 중복 검사
        elif username_exists:
            flash('Username is already in use...', category='error')
        # 위의 모든 과정을 통과한다면, 폼에서 받아온 데이터를 새로운 유저로서 저장
        else:
            db.session.add(signup_user)
            db.session.commit()
            flash("User created!!!")
            return redirect(url_for("views.home")) # 저장이 완료된 후 home으로 리다이렉트
    # GET요청을 보낸다면 회원가입 템플릿을 보여줌
    return render_template("signup.html", form=form)
