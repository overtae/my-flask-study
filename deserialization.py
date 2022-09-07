from marshmallow import Schema, fields
from serialization import Person
import json

JSON_minji_data = {"name": "김민지",
                   "height": "160cm",
                   "weight": "45kg",
                   "gender": "female",
                   "age": 25,
                   "address": "그대 마음 속..",
                   "job": "회사원"}


class PersonSchema(Schema):
    name = fields.String()
    height = fields.String()
    weight = fields.String()
    gender = fields.String()
    age = fields.Integer()
    address = fields.String()
    job = fields.String()


person_data_converter = PersonSchema()

data = person_data_converter.load(JSON_minji_data)
Person_object = Person(**data)

print(Person_object)
