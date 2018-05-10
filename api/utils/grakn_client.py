import grakn
from api import settings


class Grakn():
    def __init__(self, uri=settings.GRAKN_URL, keyspace=settings.GRAKN_KEYSPACE):
        self.client = grakn.Client(
            uri=uri,
            keyspace=keyspace,
        )

    def query(self, query: str):
        return self.client.execute(query)
