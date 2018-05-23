import falcon
from falcon import Request, Response
from api.models.anime import AnimeModel
from marshmallow.validate import OneOf
from webargs import fields
from webargs.falconparser import use_args
from typing import Dict, List


class Animes:
    def __init__(self):
        self.resource = AnimeModel()

    def on_get(self, req: Request, resp: Response) -> None:

        resp.json = self.resource.get_all_anime(limit=10)
        resp.status = falcon.HTTP_200


class Anime:
    request_args = {
        'only_attr': fields.List(fields.Str(
            required=True,
            validate=OneOf(
                choices=AnimeModel.ANIME_ATTR,
                error='{input} not a valid anime attribute.',
            ),
        )),
    }

    def __init__(self):
        self.resource = AnimeModel()

    @use_args(request_args)
    def on_get(self, req: Request, resp: Response, q_args: Dict, anime_id: str) -> None:
        attr_args: List[str] = q_args['only_attr'] if q_args else None
        json_result: List = self.resource.get_anime(anime_id, wanted_attr=attr_args)

        if not json_result:
            raise falcon.HTTPNotFound(
                title='Anime not Found',
                description=f'Anime with id: {anime_id} does not exist.',
            )

        resp.json = json_result
        resp.status = falcon.HTTP_200
