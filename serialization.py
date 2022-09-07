# import json
from dataclasses import field
from marshmallow import Schema, fields


class Person:
    def __init__(self, name, height, weight, gender, age, address, job, ):
        self.name = name        # 이름
        self.height = height    # 신장
        self.weight = weight    # 몸무게
        self.gender = gender    # 성별
        self.age = age          # 나이
        self.address = address  # 주소
        self.job = job          # 직업


gildong = Person(
    '홍길동',
    '180cm',
    '80kg',
    'male',
    '24',
    '조선 땅 어느 곳이던 내가 가는 곳이 곧 나의 거처일 것이니...',
    '의적'
)

chulsu = Person(
    '김철수',
    '110cm',
    '28kg',
    'male',
    '7',
    '떡잎마을',
    '유치원생'
)


class PersonSchema(Schema):
    name = fields.String()
    height = fields.String()
    gender = fields.String()
    age = fields.String()


person_data_converter = PersonSchema()

gildong_data = person_data_converter.dump(gildong)
chulsu_data = person_data_converter.dump(chulsu)

print(gildong_data)
print(chulsu_data)


# print(json.dumps(gildong_data, ensure_ascii=False))
# print(json.dumps(chulsu_data, ensure_ascii=False))
