from api.models.user import UserModel, RefreshTokenModel
from flask_restful import Resource, request
from api.schemas.user import UserRegisterSchema, UserSchema
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask.views import MethodView
from werkzeug.security import check_password_hash

register_schema = UserRegisterSchema()
user_schema = UserSchema()


class UserRegister(Resource):
    """
    회원가입을 처리합니다.
    username, email 은 데이터베이스에서 유일한 값이어야 하므로,
    사용자가 데이터베이스에 존재하는 email 이나 username 으로 회원가입을 시도한다면,
    적절한 에러 메시지와 함께 "잘못된 요청을 보냈어!" 라는 400 상태 코드를 응답합니다.

    비밀번호는 데이터베이스에 직접 저장되면 안 되므로,
    저장 시 SHA256 알고리즘을 사용하여 해싱하여 저장합니다.
    """

    def post(self):
        data = request.get_json()
        validate_result = register_schema.validate(data)
        if validate_result:
            return validate_result, 400
        else:
            if UserModel.find_by_username(data["username"]):
                return {"bad request": "중복된 사용자 이름입니다."}, 400
            elif UserModel.find_by_email(data["email"]):
                return {"message": "중복된 이메일입니다."}, 400
            else:
                password = generate_password_hash(data["password"])
                user = register_schema.load(
                    {
                        "username": data["username"],
                        "email": data["email"],
                        "password": password,
                        "password_confirm": password,
                    }
                )

            user.save_to_db()
            return {"success": f"{user.username} 님, 가입을 환영합니다!"}, 201


class UserLogin(MethodView):
    def post(self):
        data = request.get_json()
        user = UserModel.find_by_email(data["email"])

        additional_claims = {"user_id": user.id}

        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity=user.username, fresh=True, additional_claims=additional_claims
            )
            refresh_token = create_refresh_token(
                identity=user.username, additional_claims=additional_claims
            )

            if user.token:
                token = user.token[0]
                token.refresh_token_value = refresh_token
                token.save_to_db()
            else:
                new_token = RefreshTokenModel(
                    user_id=user.id, refresh_token_value=refresh_token
                )
                new_token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"Unauthorized": "이메일과 비밀번호를 확인하세요."}, 401


class RefreshToken(MethodView):
    """
    Refresh Token 을 받아 검증하고,
    새로운 Refresh Token, Access token 을 발급합니다.
    Refresh Token 은 일회용이므로, 새로운 Refresh Token 이 발급되면
    데이터베이스에 그 값을 저장합니다.
    """

    @jwt_required(refresh=True)
    def post(self):
        """
        -> refresh token 은 이미 검증된 상태라고 가정 (틀린 토큰, 만료된 토큰 X)
        -> 해당 유저가 데이터베이스에서 가지고 있는 refresh token 과 요청으로 들어온 refresh token이 다르다면,
        -> access token 발급은 실패해야 함
        """
        identity = get_jwt_identity()
        token = dict(request.headers)["Authorization"][7:]
        user = RefreshTokenModel.get_user_by_token(token)

        if not user:
            return {"Unauthorized": "Refresh Token은 2회 이상 사용될 수 없습니다."}, 401

        # access token, refresh token 발급
        additional_claims = {"user_id": user.id}

        access_token = create_access_token(
            identity=identity, fresh=True, additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=user.username, additional_claims=additional_claims
        )

        if user:
            token = user.token[0]
            token.refresh_token_value = refresh_token
            token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200


class MyPage(Resource):
    """
    마이페이지
    나의 마이페이지는 나만 접근 가능
    """

    @classmethod
    @jwt_required()
    def get(cls, id):
        username = get_jwt_identity()
        user = UserModel.find_by_username(username=username)
        if not user:
            return {"Error": "사용자를 찾을 수 없습니다."}, 404
        if id == user.id:
            return user_schema.dump(user), 200
        return {"Error": "잘못된 접근입니다."}, 403

    @classmethod
    @jwt_required()
    def put(cls, id):
        user_json = request.get_json()
        validate_result = user_schema.validate(user_json)
        if validate_result:
            return validate_result, 400
        user = UserModel.find_by_username(get_jwt_identity())

        # 사용자의 존재 여부
        if not user:
            return {"Error": "사용자를 찾을 수 없습니다."}, 404

        request_user = UserModel.find_by_username(get_jwt_identity())
        if id == request_user.id:
            user.update_to_db(user_json)
            return user_schema.dump(user)
        else:
            return {"Error": "잘못된 접근입니다."}, 403
