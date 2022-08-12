from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    # email : 필수 입력 항목이며, 이메일의 형식을 유지해야 함.
    email = EmailField('email', validators=[DataRequired(), Email()])
    # username : 필수 입력 항목이며, 최소 5글자부터 최대 30글자까지 허용됨.
    username = StringField('username', validators=[
                           DataRequired(), Length(4, 30)])
    # password1 : 필수 입력 항목이며, 최소 8글자부터 최대 30글자까지 허용됨, password2와 값이 같아야 함.
    password1 = PasswordField('password', validators=[DataRequired(), Length(
        8, 30), EqualTo("password2", message="Password must match...")])
    password2 = PasswordField('password again', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()])
