from api import api
from api.resources.anime import Anime

api.add_route('/api/anime', Anime())
