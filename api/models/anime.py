from marshmallow import Schema, fields
from typing import Dict, List, Set
from api.models.entity import Entity
from api.utils import utils


class AttrField(Schema):
    only = ('value')
    value = fields.Integer()


class MembersField(AttrField):
    pass


class RatingField(AttrField):
    value = fields.Float()


class TitleField(AttrField):
    value = fields.Str()


class TypeField(AttrField):
    value = fields.Str()


class EpisodeField(AttrField):
    value = fields.Integer()


class IdField(AttrField):
    value = fields.Str()


class AnimeSchema(Schema):
    only = ('anime_id', 'title', 'type', 'rating', 'episodes', 'members')

    anime_id = fields.Nested(IdField())
    title = fields.Nested(TitleField())
    type = fields.Nested(TypeField())
    rating = fields.Nested(RatingField())
    episodes = fields.Nested(EpisodeField())
    members = fields.Nested(MembersField())


class AnimeModel(Entity):
    ANIME_ATTR = {
        'anime_id', 'episodes', 'members',
        'rating', 'title', 'type',
    }

    def __init__(self):
        super().__init__()

    def get_all_anime(self, limit: int) -> List[Dict]:
        return self.grakn.query(f'''
            match $anime isa anime has attribute $attr; limit {limit}; get;
         ''')

    @utils.marshall_with(AnimeSchema)
    def get_anime(self, anime_id: str, wanted_attr: Set=None) -> List[Dict]:
        attr_to_get = wanted_attr if wanted_attr else self.ANIME_ATTR
        attributes = (f'has {attr} ${attr}' for attr in attr_to_get)
        get_attr = (f'${attr}' for attr in attr_to_get)

        return self.grakn.query(f'''
            match $anime isa anime has anime_id "{anime_id}" {' '.join(attributes)};
            limit 1; offset 0;
            get {','.join(get_attr)};
        ''')

    @utils.marshall_with(AnimeSchema)
    def get_similar_anime(self, anime_title: str, limit: int, offset: int, genre: str=None) -> List[Dict]:
        filter_by_genre = f'$name val = "{genre.lower()}";' if genre else ''

        return self.grakn.query(f'''
            match (tagged: $anime_a, tagger: $genre_a) isa tagging;
            (tagged: $anime_a, similar_to: $anime_b) isa similar_anime;
            $anime_a has title $a_title;
            $a_title val = "{anime_title.lower()}";
            $anime_b has anime_id $anime_id has title $title;
            $genre_a has name $name;
            {filter_by_genre}
            limit {limit}; offset {offset}; get $anime_id, $title;
        ''')
