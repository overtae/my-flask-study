from api.ma import ma, Method
from marshmallow import fields
from api.models.post import PostModel
from api.models.user import UserModel
from api.schemas.user import AuthorSchema


class PostSchema(ma.SQLAlchemyAutoSchema):
    image = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    author = fields.Nested(AuthorSchema)
    author_name = Method("get_author_name")
    liker_count = Method("get_liker_count")
    is_like = Method("get_is_like")

    def get_author_name(self, obj):
        return obj.author.username

    def get_liker_count(self, obj):
        return obj.get_liker_count()

    def get_is_like(self, obj):
        if self.context.get("user"):
            return obj.is_like(self.context["user"])

    class Meta:
        model = PostModel

        dump_only = [
            "author_name",
            "is_like",
        ]

        # load_only = [
        #     "author_id",
        # ]

        exclude = ("author_id",)
        load_instance = True
        include_fk = True
        ordered = True
