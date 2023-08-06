from web_engine.utils.JsonReader import JsonReader


class ScraperConfig(JsonReader):
    def __init__(self, configuration: dict):
        super(ScraperConfig, self).__init__(configuration)

