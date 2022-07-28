# auth.py : 로그인, 로그아웃 등의 로그인 관련 기능 처리

import logging

from flask_login import login_user, logout_user, current_user, login_required

from . import db
from .forms import SignupForm, LoginForm
from .models import User
from flask import Blueprint, render_template, request, url_for, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])  # 로그인에서 POST 요청을 처리해야 함.
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        # 폼으로부터 검증된 데이터 받아오기
        password = form.password.data

        # 폼에서 받아온 이메일로 유저 찾기
        user = User.query.filter_by(email=form.email.data).first()

        # 로그인 폼에서 입력된 이메일이 존재한다면,
        if user:
            if check_password_hash(user.password, password):
                flash("로그인하였습니다.", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect!", category='error')
        # 로그인 폼에서 입력된 이메일이 존재하지 않는다면,
        else:
            flash("Email does not exist...", category='error')

    return render_template("login.html", form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # 로그아웃하면 views의 blog/home으로 리다이렉트됨
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])  # 회원가입에서 POST 요청을 처리해야 함.
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 폼으로부터 검증된 데이터 받아오기
        signup_user = User(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(form.password1.data)
        )

        # 폼에서 받아온 데이터가 데이터베이스에 이미 존재하는지 확인
        email_exists = User.query.filter_by(email=form.email.data).first()
        username_exists = User.query.filter_by(
            username=form.username.data).first()

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
            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('views.home'))  # 저장이 완료된 후 home으로 리다이렉트
    # GET요청을 보낸다면 회원가입 템플릿을 보여줌
    return render_template('signup.html', form=form, user=current_user)
