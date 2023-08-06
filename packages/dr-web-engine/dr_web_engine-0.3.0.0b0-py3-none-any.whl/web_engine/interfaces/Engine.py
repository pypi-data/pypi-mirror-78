from interface import Interface


class Engine(Interface):
    """
    Base interface for the engine that will do the main query processing and return the end result
    """

    def process(self) -> dict:
        pass

