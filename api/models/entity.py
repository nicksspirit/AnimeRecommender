from api.utils import grakn_client


class Entity:

    def __init__(self):
        self.grakn = grakn_client.Grakn() 