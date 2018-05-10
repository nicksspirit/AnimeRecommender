from marshmallow import Schema, fields
from typing import Dict
from api.models.entity import Entity
from api.utils import utils


class TypeField(Schema):
    only = ('label')
    label = fields.Str()


class AttrField(Schema):
    only = ('id', 'type', 'value')

    id = fields.Str()
    type = fields.Nested(TypeField())
    value = fields.Integer()


class AnimeField(Schema):
    only = ('id', 'type')

    id = fields.Str()
    type = fields.Nested(TypeField())


class AnimeSchema(Schema):
    only = ('attr', 'anime')

    attr = fields.Nested(AttrField())
    anime = fields.Nested(AnimeField())


class AnimeModel(Entity):

    def __init__(self):
        super().__init__()

    @utils.marshall(AnimeSchema)
    def get_animes(self, limit: int) -> Dict:
        return self.grakn.query(f'''
            match $anime isa anime has attribute $attr; limit {limit}; get;
         ''')
