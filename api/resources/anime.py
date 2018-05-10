import falcon
from falcon import Request, Response
from api.models.anime import AnimeEntity 


class Anime:
    def __init__(self):
        self.resource = AnimeEntity()

    def on_get(self, req: Request, resp: Response) -> None:

        resp.json = self.resource.get_animes(limit=10)
        resp.status = falcon.HTTP_200