import os
from datetime import timedelta


RESTFUL_JSON = dict(ensure_ascii=False)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, "static", "images")

SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
JSON_AS_ASCII = False
