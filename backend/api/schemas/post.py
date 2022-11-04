from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel


class PostSchema(ma.SQLAlchemyAutoSchema):
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
