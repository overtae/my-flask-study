import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# print(BASE_DIR) # ...\my-flask-study\backend
UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, "static", "images")
