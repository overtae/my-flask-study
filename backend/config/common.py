import os
from datetime import timedelta


RESTFUL_JSON = dict(ensure_ascii=False)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, "static", "images")
