import falcon
from falcon import Request, Response
from api.models.anime import AnimeModel
from webargs import fields
from webargs.falconparser import use_args
from typing import Dict, List


class SimilarAnime:
    request_args = {
        'to': fields.Str(required=True),
        'by_genre': fields.Str(),
        'limit': fields.Integer(missing='10'),
        'offset': fields.Integer(missing='0'),
    }

    def __init__(self):
        self.resource = AnimeModel()

    @use_args(request_args)
    def on_get(self, req: Request, resp: Response, q_args: Dict) -> None:
        anime_title = q_args['to']
        limit = q_args['limit']
        offset = q_args['offset']
        genre = q_args['by_genre'] if 'by_genre' in q_args else None
        json_result: List[Dict] = self.resource.get_similar_anime(anime_title, limit, offset, genre=genre)

        if not json_result:
            raise falcon.HTTPNotFound(
                title='Animes not Found',
                description=f'No animes are similar to {anime_title} by {genre}',
            )

        resp.json = json_result
        resp.status = falcon.HTTP_200
