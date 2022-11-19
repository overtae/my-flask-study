import unittest
from api.db import db
import api
import json
from dotenv import load_dotenv
from api.models.post import PostModel
from api.models.user import UserModel


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
        self.ctx = self.app.app_context()
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


from . import *


class PostListTestCase(CommonTestCaseSettings):
    """
    /posts 에 대한 GET, POST 요청을 테스트한다.

    GET /posts -> 모든 게시물의 목록을 반환
    get_json() 응답 예시: 딕셔너리를 요소로 가지는 리스트
    [
    {
    'author_name': 'test_user',
    'id': 100,
    'title': '100번째 테스트 게시물입니다.',
    'content': '100번째 테스트 게시물의 내용입니다.',
    'created_at': '2022-10-13T11:55:38',
    'updated_at': '2022-10-13T11:55:38'
    },
    {
    'author_name': 'test_user',
    'id': 100,
    'title': '100번째 테스트 게시물입니다.',
    'content': '100번째 테스트 게시물의 내용입니다.',
    'created_at': '2022-10-13T11:55:38',
    'updated_at': '2022-10-13T11:55:38'
    },
    ]

    POST /posts -> 새로운 게시물을 하나 생성
    성공 시 : 201 CREATED
    """

    def test_get_post_list(self):
        """
        1. 임의의 게시물 100개를 생성하고, /posts 에 요청을 보냄
        2. 임의의 게시물의 형태는 (제목:1번째 테스트 게시물입니다. / 내용:1번째 테스트 게시물의 내용입니다) 와 같은 형태가 될 것임
        3. /posts 에 요청을 보내면, 게시물의 목록이 나타나야 함
        4. 게시물의 목록은 10개씩, 역 pk 순으로 페이지네이션 처리되어야 함
        5. 고로, 첫 번째 게시물의 id 는 100이어야 함
        6. 첫 번째 페이지의 마지막 게시물의 id는 91이어야 함
        """

        # 임의의 게시물 100개 생성
        dummy_posts = []
        for i in range(100):
            dummy_posts.append(
                PostModel(
                    title=f"{i+1}번째 테스트 게시물입니다.",
                    content=f"{i+1}번째 테스트 게시물의 내용입니다.",
                    author_id=1,
                )
            )
        db.session.bulk_save_objects(dummy_posts)
        db.session.commit()

        # 게시물의 첫 번째 페이지로 요청을 보낸다.
        response = self.client.get("http://127.0.0.1:5000/posts/").get_json()

        # 게시물 목록의 맨 첫 번째 게시물의 id 는 100이어야 한다.
        self.assertEqual(100, response[0]["id"])

        # 게시물 목록의 맨 마지막 게시물의 id 는 91 이어야 한다.
        self.assertEqual(91, response[-1]["id"])

        # 게시물의 두 번째 페이지로 요청을 보낸다.
        response = self.client.get("http://127.0.0.1:5000/posts/?page=2").get_json()

        # 게시물 목록의 두 번째 페이지의 맨 첫 번째 게시물의 id 는 90이어야 한다.
        self.assertEqual(90, response[0]["id"])

        # 게시물 목록의 맨 마지막 게시물의 id 는 81 이어야 한다.
        self.assertEqual(81, response[-1]["id"])

    def test_post_post_list(self):
        """
        1. 게시물이 없는 상태이므로, /posts 에 GET 요청을 보낸다면 응답은 비어 있어야 한다.
        2. /posts 에 적절한 데이터를 보냈지만 access token 을 첨부하지 않았다면, 응답 상태 코드는 401이어야 한다.
        토큰 정보가 없음 : 401
        토큰 정보가 있고 유저임이 증명되었지만, 권한이 없음 : 403
        3. /posts 에 적절한 데이터, 토큰과 함께 POST 요청을 보냈고 성공했다면, 응답 상태 코드는 201이어야 한다.
        4. 게시물 생성에 성공했다면, 데이터베이스에 있는 게시물의 총 수는 한 개여야 한다.
        5. 게시물 생성에 성공했다면, /posts 에 GET 요청을 보낸다면 응답은 게시물 한 개가 반환되어야 한다.
        """
        # 게시물이 없는 상태에 /posts 의 응답은 게시물 0개여야 함
        response = self.client.get("http://127.0.0.1:5000/posts/").get_json()
        self.assertEqual(0, len(response))

        # /posts 에 access token 없이 새로운 게시물을 생성해 달라고 요청
        data = json.dumps(
            {
                "title": "안녕하세요. 액세스 토큰을 첨부하지 않았으므로, 이 요청은 실패해야 합니다!",
                "content": "제발, 실패했으면 좋겠네요. :)",
            }
        )

        # 토큰 정보가 첨부되지 않았으므로, 해당 응답의 상태 코드는 401이어야 함
        response = self.client.post("http://127.0.0.1:5000/posts/", data=data)
        self.assertEqual(401, response.status_code)

        # 토큰 정보를 첨부하기 위해, 로그인을 수행, CommonTestCaseSetup 클래스에 정의된
        # test_user 로 로그인 후 access token, refresh token 발급
        data = json.dumps({"email": "test@example.com", "password": "12345"})
        response = self.client.post(
            "http://127.0.0.1:5000/login/",
            data=data,
            content_type="application/json",
        ).get_json()
        access_token, refresh_token = (
            response["access_token"],
            response["refresh_token"],
        )

        # /posts 에 access token 없이 새로운 게시물을 생성해 달라고 요청
        data = json.dumps(
            {
                "title": "안녕하세요. 액세스 토큰을 첨부했으므로, 이 요청은 성공해야 합니다!",
                "content": "제발, 성공으면 좋겠네요...ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ)",
            }
        )

        # access token, body 와 함께 게시물을 생성해 달라고 요청
        response = self.client.post(
            "http://127.0.0.1:5000/posts/",
            content_type="application/json",
            data=data,
            headers={"Authorization": "Bearer " + access_token},
        )

        # 정상적으로 게시물을 생성했고, 상태 코드로서 201을 응답해주는지 확인
        self.assertEqual(201, response.status_code)

        # 게시물을 성공적으로 생성했다면(status code 201), 데이터베이스에 남아 있는 게시물의 수는 한 개여야 함
        self.assertEqual(1, len(PostModel.query.all()))

        # 첨부한 토큰의 identity 인 username 이 게시물의 저자로서 잘 저장되었는지 확인
        # /posts/ 로 GET 요청을 보낸 후, 해당 요청의 "author_name" 값을 확인
        response = self.client.get("http://127.0.0.1:5000/posts/").get_json()
        self.assertEqual("test_user", response[0]["author_name"])


class PostDetailTestCase(CommonTestCaseSettings):
    def test_post_post_detail(self):
        """
        1. 임의의 게시물 한 개를 생성한다.
        2. 해당 게시물은 id가 1로 들어갈 것이다.
        3. posts/1 에 접속하면 게시물의 내용이 같아야 한다.
        4. posts/2 와 같이 없는 게시물에 접속하면 상태 코드가 404여야 한다.
        """
        PostModel(
            title="상세조회를 위한 테스트 게시물입니다.",
            content=f"상세조회를 위한 테스트 게시물의 내용입니다.",
            author_id=1,
        ).save_to_db()
        response = self.client.get("http://127.0.0.1:5000/posts/1").get_json()
        self.assertEqual("상세조회를 위한 테스트 게시물입니다.", response["title"])
        response = self.client.get("http://127.0.0.1:5000/posts/2")
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    unittest.main()
