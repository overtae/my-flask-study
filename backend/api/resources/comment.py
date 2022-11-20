from flask_restful import Resource, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models.post import PostModel
from api.models.comment import CommentModel
from api.models.user import UserModel
from api.schemas.comment import CommentSchema

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)


class CommentList(Resource):
    @classmethod
    def get(cls, post_id):
        post = PostModel.find_by_id(post_id)
        ordered_comment_list = post.comment_set.order_by(CommentModel.id.desc())
        return comment_list_schema.dump(ordered_comment_list)

    @classmethod
    @jwt_required()
    def post(cls, post_id):
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id

        try:
            new_comment = comment_schema.load(comment_json)
            new_comment.author_id = author_id
            new_comment.post_id = post_id
        except ValidationError as err:
            return err.messages, 400

        try:
            new_comment.save_to_db()
        except:
            return {"Error": "저장에 실패하였습니다."}, 500

        return comment_schema.dump(new_comment), 201


class CommentDetail(Resource):
    @classmethod
    @jwt_required()
    def put(cls, post_id, comment_id):
        """
        특정 게시물의 특정 댓글 수정
        게시물과 댓글이 모두 존재해야 함
        작성자 본인만 수정이 가능해야 함
        """
        comment_json = request.get_json()

        # 입력 데이터 검증
        validate_result = comment_schema.validate(comment_json)
        if validate_result:
            return validate_result, 400

        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id

        post = PostModel.find_by_id(post_id)
        comment = CommentModel.find_by_id(comment_id)

        # 게시물의 존재 여부 체크
        if not post:
            return {"Error": "게시물을 찾을 수 없습니다."}, 404

        # 댓글의 존재 여부 체크
        if not comment:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404

        # 댓글의 작성자와, 요청을 보낸 사용자가 같다면 수정
        if comment.author_id == author_id:
            comment.update_to_db(comment_json)
        else:
            return {"Error": "댓글은 작성자만 수정할 수 있습니다."}, 403

        return comment_schema.dump(comment), 200

    @classmethod
    def delete(cls, post_id, comment_id):
        pass
