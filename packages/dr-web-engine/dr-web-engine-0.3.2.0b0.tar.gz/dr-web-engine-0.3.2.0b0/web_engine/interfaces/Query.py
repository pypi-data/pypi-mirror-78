from interface import Interface
from web_engine.interfaces import Query


class Query(Interface):
    """
    Implement this interface to parse the query into executable steps
    """

    def load(self, query_def: dict = None, json_query_path: str = None) -> Query:
        pass

    @property
    def query_def(self) -> dict:
        pass

    @property
    def query_items(self):
        pass

    @property
    def status(self) -> bool:
        pass

    @property
    def prop(self):
        pass

    @property
    def pre_filters(self) -> list:
        pass
