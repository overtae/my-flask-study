from api.ma import ma, Method
from marshmallow import fields
from api.models.post import PostModel
from api.models.user import UserModel


class PostSchema(ma.SQLAlchemyAutoSchema):
    image = fields.String(required=True)

    created_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")

    author_name = Method("get_author_name")

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = PostModel

        dump_only = [
            "author_name",
        ]

        # load_only = [
        #     "author_id",
        # ]

        exclude = ("author_id",)
        load_instance = True
        include_fk = True
        ordered = True
