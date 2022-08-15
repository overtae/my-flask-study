# 홈페이지, 자기소개 페이지, 포스트 CRUD 페이지 관련 처리

from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from .models import db, get_category_model, get_post_model, get_comment_model
from .forms import PostForm, CommentForm

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
    # 모든 카테고리 가져오기
    categories = get_category_model().query.all()
    return render_template("categories_list.html", user=current_user, categories=categories)


@views.route("/post-list/<int:id>")
def post_list(id):
    current_category = get_category_model().query.filter_by(id=id).first()
    posts = get_post_model().query.filter_by(category_id=id)
    return render_template("post_list.html", user=current_user, posts=posts, current_category=current_category)


@views.route('/posts/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    comment_form = CommentForm()
    post = get_post_model().query.filter_by(id=id).first()
    comments = get_post_model().query.filter_by(id=id).first().comments
    return render_template("post_detail.html", user=current_user, post=post, comments=comments, form=comment_form)


@views.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)


@views.route("/create-post", methods=['POST'])
@login_required
def create_post():
    if current_user.is_staff == True:
        form = PostForm()
        if request.method == "POST" and form.validate_on_submit():
            post = get_post_model()(
                title=form.title.data,
                content=form.content.data,
                category_id=form.category.data,
                author_id=current_user.id,
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("views.home"))
        else:
            # 모든 카테고리 가져오기
            categories = get_category_model().query.all()
            return render_template("post_create.html", form=form, user=current_user, categories=categories)
    else:
        return abort(403)


@views.route("/edit-post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = get_post_model().query.filter_by(id=id).first()
    form = PostForm()
    categories = get_category_model().query.all()

    if (current_user.is_staff == True) and (current_user.username == post.user.username):
        if request.method == "GET":
            # 원래 게시물 내용
            return render_template("post_edit.html", user=current_user, post=post, categories=categories, form=form)
        elif request.method == "POST" and form.validate_on_submit():
            # 수정 작업 완료 코드
            post.title = form.title.data
            post.content = form.content.data
            post.category_id = int(form.category.data)
            db.session.commit()
            return redirect(url_for("views.home"))
    else:
        abort(403)


@login_required
@views.route("/delete-post/<int:id>")
def delete_post(id):
    post = get_post_model().query.filter_by(id=id).first()
    # 작성자인 경우 > 게시물 삭제
    if current_user.username == post.user.username:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("views.categories_list", id=id))
    # 작성자가 아닌 경우 > 403 에러
    else:
        return abort(403)


@login_required
@views.route("/create-comment/<int:id>", methods=['POST'])
def create_comment(id):
    form = CommentForm()
    print(1)
    if request.method == "POST" and form.validate_on_submit():
        print(1)
        comment = get_comment_model()(
            content=form.content.data,
            author_id=current_user.id,
            post_id=id,
        )
        print(1)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("views.post_detail", id=id))


@login_required
@views.route("/edit-comment/<int:post_id>/<int:comment_id>", methods=["POST"])
def edit_comment(post_id, comment_id):
    comment = get_comment_model().query.filter_by(id=comment_id).first()
    form = CommentForm()
    if current_user.username == comment.user.username:
        if form.validate_on_submit():
            comment.content = form.content.data
            db.session.commit()
            return redirect(url_for("views.post_detail", id=post_id))
        else:
            print("validation failed")
    else:
        return abort(403)


@login_required
@views.route("/delete-comment/<int:post_id>/<int:id>")
def delete_comment(post_id, id):
    comment = get_comment_model().query.filter_by(post_id=post_id, id=id).first()

    # 작성자인 경우 > 댓글 삭제
    if current_user.username == comment.user.username:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for("views.post_detail", id=post_id))
    # 작성자가 아닌 경우 > 403 에러
    else:
        return abort(403)
