import unittest
from os import path

from flask_login import current_user, FlaskLoginClient
from bs4 import BeautifulSoup  # pip install BeautifulSoup4

from blog import create_app
import os

from blog.models import db, get_user_model, get_category_model, get_post_model, get_comment_model

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
app.testing = True


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists('tests/' + 'test_db'):
            db.create_all(app=app)
        db.session.close()

    # 다른 테스트들에 영향을 줄 수 있기 때문에 테스트 후 데이터베이스 삭제
    def tearDown(self):
        os.remove('tests/test.db')
        self.ctx.pop()

    def test_signup_by_datebase(self):
        self.user_test_1 = get_user_model()(
            email='testemail1@test.com',
            username='testUser01',
            password='qwerasdf',
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()

        self.user_test_2 = get_user_model()(
            email='testemail2@test.com',
            username='testUser02',
            password='qwerasdf'
        )
        db.session.add(self.user_test_2)
        db.session.commit()

        self.assertEqual(get_user_model().query.count(), 2)
        db.session.close()

    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up', data=dict(
            email="testemail@test.com", username="testUser00", password1="qwerasdf", password2="qwerasdf"))
        self.assertEqual(get_user_model().query.count(), 1)
        db.session.close()

    def test_before_login(self):
        # 로그인 전의 네비게이션 바 크롤링
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        navbar_before_login = soup.nav

        # 로그인과 회원가입 버튼이 있는지, 로그아웃 버튼이 없는지 확인
        self.assertIn("Login", navbar_before_login.text)
        self.assertIn("Sign Up", navbar_before_login.text, )
        self.assertNotIn("Logout", navbar_before_login.text, )

        # 회원가입 후,
        response = self.client.post('/auth/sign-up', data=dict(
            email="testemail@test.com", username="testUser00", password1="qwerasdf", password2="qwerasdf"))

        with self.client:
            # 로그인
            response = self.client.post('/auth/login', data=dict(
                email="testemail@test.com", username="testUser00", password="qwerasdf"),
                follow_redirects=True)
            # 로그인 후의 네비게이션 바 크롤링
            soup = BeautifulSoup(response.data, 'html.parser')
            navbar_after_login = soup.nav

            # 로그인 후 네비게이션 바에 유저 이름과 로그아웃 버튼이 있는지,
            # 회원가입 버튼과 로그인 버튼이 있는지 확인
            self.assertIn(current_user.username, navbar_after_login.text)
            self.assertIn("Logout", navbar_after_login.text)
            self.assertNotIn("Login", navbar_after_login.text)
            self.assertNotIn("Sign up", navbar_after_login.text)
            db.session.close()


# class TestPostwithCategory(unittest.TestCase):
#     def setUp(self):
#         self.ctx = app.app_context()
#         self.ctx.push()
#         self.client = app.test_client()

#         self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
#         if not path.exists('tests/' + 'test_db'):
#             db.create_all(app=app)
#         db.session.close()

#     # 다른 테스트들에 영향을 줄 수 있기 때문에 테스트 후 데이터베이스 삭제
#     def tearDown(self):
#         db.session.close()
#         os.remove('tests/test.db')
#         self.ctx.pop()

#     def test_add_category_and_post(self):
#         # 이름 = "python" 인 카테고리를 하나 추가하고,
#         self.python_category = get_category_model()(
#             name="python"
#         )
#         db.session.add(self.python_category)
#         db.session.commit()
#         # 추가한 카테고리의 이름이 "python" 인지 확인한다.
#         self.assertEqual(get_category_model().query.first().name, "python")
#         # id는 1로 잘 추가되어있는지 확인한다.
#         self.assertEqual(get_category_model().query.first().id, 1)
#         # 이름 = "rust" 인 카테고리를 하나 추가하고,
#         self.rust_category = get_category_model()(
#             name="rust"
#         )
#         db.session.add(self.rust_category)
#         db.session.commit()
#         self.assertEqual(get_category_model().query.filter_by(id=2).first().name,
#                          "rust")  # id가 2인 카테고리의 이름이 "rust" 인지 확인한다.
#         # 이름 = "javascript" 인 카테고리를 하나 더 추가해 주자.
#         self.rust_category = get_category_model()(
#             name="javascript"
#         )
#         db.session.add(self.rust_category)
#         db.session.commit()

#         # 카테고리 리스트 페이지에 접속했을 때에, 추가했던 3개의 카테고리가 잘 추가되어 있는지?
#         response = self.client.get('/categories-list')
#         soup = BeautifulSoup(response.data, 'html.parser')
#         self.assertIn('python', soup.text)
#         self.assertIn('rust', soup.text)
#         self.assertIn('javascript', soup.text)

#         # 로그인 전에는, 포스트 작성 페이지에 접근한다면 로그인 페이지로 이동해야 한다. 리디렉션을 나타내는 상태 코드는 302이다.
#         response = self.client.get('/create-post', follow_redirects=False)
#         self.assertEqual(302, response.status_code)

#         # 스태프 권한을 가지고 있지 않는 작성자 생성
#         response = self.client.post('/auth/sign-up',
#                                     data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
#                                               password2="dkdldpvmvl"))
#         # 스태프 권한을 가지고 있지 않은 작성자가 포스트 작성 페이지에 접근한다면, 권한 거부가 발생해야 한다.
#         with self.client:
#             response = self.client.post('/auth/login',
#                                         data=dict(email="helloworld@naver.com", username="hello",
#                                                   password="dkdldpvmvl"),
#                                         follow_redirects=True)
#             response = self.client.get('/create-post', follow_redirects=False)
#             self.assertEqual(403,
#                              response.status_code)  # 스태프 권한을 가지고 있지 않은 사람이 /create-post 에 접근한다면, 서버는 상태 코드로 403을 반환해야 한다.
#             # 스태프 권한을 가지고 있지 않은 작성자에서 로그아웃
#             response = self.client.get('/auth/logout')

#         # 스태프 권한을 가지고 있는 작성자 생성, 폼에서는 is_staff 를 정할 수 없으므로 직접 생성해야 한다.
#         self.user_with_staff = get_user_model()(
#             email="staff@example.com",
#             username="staffuserex1",
#             password="12345",
#             is_staff=True
#         )
#         db.session.add(self.user_with_staff)
#         db.session.commit()

#         # 스태프 권한을 가지고 있는 유저로 로그인 후, 게시물을 잘 작성할 수 있는지 테스트
#         from flask_login import FlaskLoginClient
#         app.test_client_class = FlaskLoginClient
#         with app.test_client(user=self.user_with_staff) as user_with_staff:
#             # 로그인한 상태로, 게시물 작성 페이지에 갔을 때에 폼이 잘 떠야 한다.
#             response = user_with_staff.get(
#                 '/create-post', follow_redirects=True)
#             self.assertEqual(response.status_code,
#                              200)  # 스태프 권한을 가지고 있는 사용자가 서버에 get 요청을 보냈을 때에, 정상적으로 응답한다는 상태 코드인 200을 돌려주는가?

#             # 미리 작성한 카테고리 3개가 셀렉트 박스의 옵션으로 잘 뜨고 있는가?
#             soup = BeautifulSoup(response.data, 'html.parser')
#             select_tags = soup.find(name='category')
#             self.assertIn("python", select_tags.text)
#             self.assertIn("rust", select_tags.text)
#             self.assertIn("javascript", select_tags.text)

#             response_post = user_with_staff.post('/create-post',
#                                                  data=dict(
#                                                      title="안녕하세요, 첫 번째 게시물입니다.", content="만나서 반갑습니다!", category="1"),
#                                                  follow_redirects=True)

#             # 게시물을 폼에서 작성한 후, 데이터베이스에 남아 있는 게시물의 수가 1개가 맞는가?
#             self.assertEqual(1, get_post_model().query.count())

#         # 게시물은 잘 추가되어 있는지?
#         response = self.client.get(f'/posts/1')
#         soup = BeautifulSoup(response.data, 'html.parser')

#         # 게시물의 페이지에서 우리가 폼에서 입력했던 제목이 잘 나타나는지?
#         title_wrapper = soup.find(id='title-wrapper')
#         self.assertIn("안녕하세요, 첫 번째 게시물입니다.", title_wrapper.text)

#         # 게시물 페이지에서, 로그인했던 유저의 이름이 저자로 잘 표시되는지?
#         author_wrapper = soup.find(id='author-wrapper')
#         self.assertIn("staffuserex1", author_wrapper.text)

#         db.session.close()

#     def test_update_post(self):

#         # 2명의 유저 생성하기
#         self.smith = get_user_model()(
#             email="smithf@example.com",
#             username="smith",
#             password="12345",
#             is_staff=True,
#         )
#         db.session.add(self.smith)
#         db.session.commit()
#         self.james = get_user_model()(
#             email="jamesf@example.com",
#             username="james",
#             password="12345",
#             is_staff=True,
#         )
#         db.session.add(self.james)
#         db.session.commit()

#         # 2개의 카테고리 생성하기
#         self.python_category = get_category_model()(
#             name="python1"  # id == 1
#         )
#         db.session.add(self.python_category)
#         db.session.commit()
#         self.javascript_category = get_category_model()(
#             name="javascript1"  # id == 2
#         )
#         db.session.add(self.javascript_category)
#         db.session.commit()

#         # smith로 로그인 후, 수정 처리가 잘 되는지 테스트
#         from flask_login import FlaskLoginClient
#         app.test_client_class = FlaskLoginClient
#         # smith 로 게시물 작성, 이 게시물의 pk는 1이 될 것임
#         with app.test_client(user=self.smith) as smith:
#             smith.post('/create-post',
#                        data=dict(title="안녕하세요,smith가 작성한 게시물입니다.",
#                                  content="만나서 반갑습니다!",
#                                  category="1"), follow_redirects=True)
#             response = smith.get('/posts/1')  # smith가 본인이 작성한 게시물에 접속한다면,
#             soup = BeautifulSoup(response.data, 'html.parser')
#             edit_button = soup.find(id='edit-button')
#             self.assertIn('Edit', edit_button.text)  # "Edit" 버튼이 보여야 함

#             # smith 가 본인이 작성한 포스트에 수정하기 위해서 접속하면,
#             response = smith.get('/edit-post/1')
#             # 정상적으로 접속할 수 있어야 함, status_code==200이어야 함
#             self.assertEqual(200, response.status_code)
#             soup = BeautifulSoup(response.data, 'html.parser')

#             title_input = soup.find('input')
#             content_input = soup.find('textarea')

#             # 접속한 수정 페이지에서, 원래 작성했을 때 사용했던 문구들이 그대로 출력되어야 함
#             self.assertIn(title_input.text, "안녕하세요,smith가 작성한 게시물입니다.")
#             self.assertIn(content_input.text, "만나서 반갑습니다!")

#             # 접속한 수정 페이지에서, 폼을 수정하여 제출
#             smith.post('/edit-post/1',
#                        data=dict(title="안녕하세요,smith가 작성한 게시물을 수정합니다.",
#                                  content="수정이 잘 처리되었으면 좋겠네요!",
#                                  category="2"), follow_redirects=True)
#             # 수정을 완료한 후, 게시물에 접속한다면 수정한 부분이 잘 적용되어 있어야 함
#             response = smith.get('/posts/1')
#             soup = BeautifulSoup(response.data, 'html.parser')
#             title_wrapper = soup.find(id='title-wrapper')
#             content_wrapper = soup.find(id='content-wrapper')

#             self.assertIn(title_wrapper.text, "안녕하세요,smith가 작성한 게시물을 수정합니다.")
#             self.assertIn(content_wrapper.text, "수정이 잘 처리되었으면 좋겠네요!")

#             # 마찬가지로 smith로 접속한 상태이므로,
#             response = smith.get('/posts/1')  # smith가 본인이 작성한 게시물에 접속한다면,
#             soup = BeautifulSoup(response.data, 'html.parser')
#             edit_button = soup.find(id='edit-button')
#             self.assertIn('Edit', edit_button.text)  # "Edit" 버튼이 보여야 함
#             smith.get('/auth/logout')  # smith 에서 로그아웃
#         # james 로 로그인
#         with app.test_client(user=self.james) as james:
#             response = james.get('/posts/1')  # Read 를 위한 접속은 잘 되어야 하고,
#             self.assertEqual(response.status_code, 200)
#             soup = BeautifulSoup(response.data, 'html.parser')
#             self.assertNotIn('Edit', soup.text)  # Edit 버튼이 보이지 않아야 함
#             response = james.get('/edit-post/1')  # Update 를 위한 접속은 거부되어야 함
#             self.assertEqual(response.status_code, 403)

#         db.session.close()


class TestComment(unittest.TestCase):
    # 테스트를 위한 사전 준비
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        # 테스트를 위한 db 설정
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists("tests/" + "test_db"):  # DB 경로가 존재하지 않는다면,
            db.create_all(app=app)  # DB를 하나 만들어낸다.

        # 2명의 유저 생성하기
        self.james = get_user_model()(
            email="jamesf@example.com",
            username="james",
            password="12345",
            is_staff=False,
        )
        db.session.add(self.james)
        db.session.commit()
        self.nakamura = get_user_model()(
            email="nk222f@example.com",
            username="nakamura",
            password="12345",
            is_staff=False,
        )
        db.session.add(self.nakamura)
        db.session.commit()

        # 댓글을 작성할 게시물 하나 생성하기
        self.example_post = get_post_model()(
            title="댓글 작성을 위한 게시물을 추가합니다.",
            content="부디 테스트가 잘 통과하길 바랍니다.",
            category_id="1",
            author_id=1  # 작성자는 james
        )
        db.session.add(self.example_post)
        db.session.commit()
        self.assertEqual(get_post_model().query.count(), 1)

    # 테스트가 끝나고 나서 수행할 것, 테스트를 위한 데이터베이스의 내용들을 모두 삭제한다.
    def tearDown(self):
        os.remove('tests/test.db')
        self.ctx.pop()

    def test_add_comment(self):
        app.test_client_class = FlaskLoginClient
        with app.test_client(user=self.james) as james:
            response = james.post('/create-comment/1',
                                  data=dict(content="만나서 반갑습니다!"))
            # 댓글을 작성하면 해당 페이지로 자동 리디렉션되어야 한다.
            self.assertEqual(302, response.status_code)
            # 작성한 댓글이 데이터베이스에 잘 추가되어 있는가?
            self.assertEqual(get_comment_model().query.count(), 1)
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id="comment-wrapper")
            # 작성한 댓글의 내용이 게시물의 상세 페이지에 잘 표시되는가?
            self.assertIn("만나서 반갑습니다!", comment_wrapper.text)
            self.assertIn("james", comment_wrapper.text)  # 작성자의 이름이 잘 표시되는가?
            # 작성자로 로그인되어 있을 경우 수정 버튼이 잘 표시되는가?
            self.assertIn("Edit comment", comment_wrapper.text)
            james.get('/auth/logout')  # james에서 로그아웃
        with app.test_client(user=self.nakamura) as nakamura:
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id="comment-wrapper")
            # 작성자로 로그인되어 있지 않을 경우 수정 버튼이 보이지 않는가?
            self.assertNotIn("Edit comment", comment_wrapper.text)
            db.session.close()

    def test_update_comment(self):
        app.test_client_class = FlaskLoginClient
        with app.test_client(user=self.james) as james:
            # james 로 댓글을 하나 작성한 다음,
            response = james.post('/create-comment/1',
                                  data=dict(content="만나서 반갑습니다!"))
            # 작성이 된 후 정상적으로 리디렉션되어야 한다.
            self.assertEqual(response.status_code, 302)
            response = james.post(
                '/edit-comment/1/1', data=dict(content="댓글 내용을 수정합니다!"))  # 댓글을 수정해 주고,
            # 수정이 완료된 후 정상적으로 리디렉션되어야 한다.
            self.assertEqual(response.status_code, 302)
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id='comment-wrapper')
            # 기존의 댓글 내용은 있으면 안 되고
            self.assertNotIn("만나서 반갑습니다!", comment_wrapper.text)
            # 수정한 댓글의 내용이 표시되어야 한다.
            self.assertIn("댓글 내용을 수정합니다!", comment_wrapper.text)
            james.get('/auth/logout')  # james에서 로그아웃
            db.session.close()


if __name__ == "__main__":
    unittest.main()
