import falcon
import falcon_jsonify

api = application = falcon.API(middleware=[
    falcon_jsonify.Middleware(help_messages=True),
])

from api import routes
