from api import api
from api.resources.anime import Animes, Anime

api.add_route('/api/animes', Animes())
api.add_route('/api/anime/{anime_id}', Anime())
