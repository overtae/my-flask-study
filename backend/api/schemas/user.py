from api.ma import ma
from marshmallow.fields import String
from marshmallow import validates_schema, post_dump
from marshmallow.exceptions import ValidationError
from api.models.user import UserModel
from marshmallow import fields

fields.Field.default_error_messages["required"] = "해당 필드를 입력해 주세요."
fields.Field.default_error_messages["validator_failed"] = "해당 필드에 대한 검증이 실패했습니다."
fields.Field.default_error_messages["null"] = "해당 필드는 null 이 될 수 없습니다."


class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    password_confirm = String(required=True)

    class Meta:
        load_instance = True
        model = UserModel
        load_only = [
            "username",
            "email",
            "password",
            "password_confirm",
        ]

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            raise ValidationError("비밀번호가 일치하지 않습니다.", "password_confirm")


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    @post_dump
    def set_default_image(self, data, **kwargs):
        if data["image"] == "" or data["image"] == None:
            data["image"] = "default/default_profile_img.png"
        return data
    class Meta:
        model = UserModel
        exclude = (
            "password",
            "created_at",
            "email",
        )


class UserSchema(ma.SQLAlchemyAutoSchema):
    image = String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d")
    
    @post_dump
    def set_default_image(self, data, **kwargs):
        if data["image"] == "" or data["image"] == None:
            data["image"] = "default/default_profile_img.png"
        return data

    class Meta:
        model = UserModel
        exclude = ("password",)
        # 읽기 전용
        dump_only = ("email", "username")
