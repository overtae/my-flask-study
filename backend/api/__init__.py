from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from utils.flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError

from .db import db
from .ma import ma

from .models import user, post, comment
from .utils.image_upload import IMAGE_SET
from .resources.post import Post, PostList, PostLike
from .resources.user import (
    RefreshToken,
    UserRegister,
    UserLogin,
    MyPage,
    Follow,
    Recommend,
)
from .resources.image import PostImageUpload, ProfileImageUpload, Image
from .resources.comment import CommentList, CommentDetail


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    load_dotenv(".env", verbose=True)
    app.config.from_object("config.dev")
    app.config.from_envvar("APPLICATION_SETTINGS")

    configure_uploads(app, IMAGE_SET)

    api = Api(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    def create_tables():
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        토큰이 만료되었을 때의 에러 메시지를 지정합니다.
        """
        return (
            jsonify({"Error": "토큰이 만료되었습니다."}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        토큰이 잘못된 값일 때의 에러 메시지를 지정합니다.
        """
        return (
            jsonify({"Error": "잘못된 토큰입니다."}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """ """
        return (
            jsonify(
                {
                    "Error": "토큰 정보가 필요합니다.",
                }
            ),
            401,
        )

    api.add_resource(Follow, "/users/<int:id>/followers/")

    api.add_resource(PostList, "/posts/")
    api.add_resource(Post, "/posts/<int:id>")
    api.add_resource(PostLike, "/posts/<int:id>/likes/")

    api.add_resource(UserRegister, "/register/")
    api.add_resource(UserLogin, "/login/")
    api.add_resource(RefreshToken, "/refresh/")

    api.add_resource(PostImageUpload, "/upload/post/image/")
    api.add_resource(ProfileImageUpload, "/upload/profile/image/")
    api.add_resource(Image, "/statics/<path:path>")

    api.add_resource(CommentList, "/posts/<int:post_id>/comments/")
    api.add_resource(CommentDetail, "/posts/<int:post_id>/comments/<int:comment_id>/")

    api.add_resource(MyPage, "/mypage/<int:id>/")

    api.add_resource(Recommend, "/users/recommend-followers/")

    return app
