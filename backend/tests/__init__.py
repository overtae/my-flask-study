import unittest
from api.db import db
import api
import json
from dotenv import load_dotenv
from api.models.post import PostModel
from api.models.user import UserModel
from flask import g


class CommonTestCaseSettings(unittest.TestCase):
    """
    테스트를 위한 공통 셋업
    """

    def setUp(self):
        """
        테스트를 위한 사전 준비
        backend/config/test.py 를 사용
        .env 파일의 APPLICATION_SETTINGS_FOR_TEST 환경 변수 사용
        app.test_client() 로 테스트를 위한 클라이언트 생성
        테스트를 위한 임의의 유저 한 명 생성 (회원가입)
        """
        self.app = api.create_app()
        # g.app_context = self.app.app_context()
        # g.app_context()
        self.ctx = self.app.app_context()
        # self.ctx = self.app_ctx()
        self.ctx.push()
        load_dotenv(".env", verbose=True)
        self.app.config.from_object("config.test")
        self.app.config.from_envvar("APPLICATION_SETTINGS_FOR_TEST")
        self.client = self.app.test_client()
        db.create_all()

        # 테스트를 위한 유저 생성 (회원가입)
        data = {
            "email": "test@example.com",
            "username": "test_user",
            "password": "12345",
            "password_confirm": "12345",
        }
        # 회원가입 진행
        self.client.post(
            "http://127.0.0.1:5000/register/",
            data=json.dumps(data),
            content_type="application/json",
        )

    def tearDown(self):
        """
        테스트가 끝나고 수행되는 메서드, 데이터베이스 초기화
        """
        db.session.remove()
        db.drop_all()
