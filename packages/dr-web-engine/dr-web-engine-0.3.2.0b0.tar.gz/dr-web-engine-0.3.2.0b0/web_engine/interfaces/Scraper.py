from interface import Interface


class Scraper(Interface):

    def get(self):
        pass

    def get_doc(self, doc):
        pass

    def action_get(self, actions: list):
        pass

    def filter_get(self, filters: list):
        pass
