from web_engine.interfaces.Scraper import Scraper
from web_engine.interfaces.ActionRunner import ActionRunner

from interface import implements
import requests


class RequestScraper(implements(Scraper, ActionRunner)):

    def __init__(self, log):
        self.log = log

        self.last_url = None
        self.last_page = None
        self._actions = {}
        self._history = []

    @property
    def actions(self) -> dict:
        return self._actions

    def get_doc(self, doc):
        """
        get the html element from the url [doc]
        :param doc: the url to the page
        :return: html.from string content
        """
        with requests.get(doc) as web_request:
            page_source = web_request.content
            self.last_url = doc
            self.last_page = page_source
            return self.last_page

    def get(self):
        return self.last_page

    def action_get(self, actions: list):
        self.log.error(f"[{type(self)}] Does not support actions. Please use another Scraper that supports actions")
        self.execute(x for x in actions)
        return self.get()

    def filter_get(self, filters: list):
        self.log.error(f"[{type(self)}] Does not support filters. Please use another Scraper that supports filters")
        self.execute(x for x in filters)
        return self.get()

    def execute(self, action_composite: str):
        action_name, action_path = RequestScraper.__get_action(action_composite)
        self.log.warn(f"Command [{action_name}] not recognised")

    @property
    def driver(self):
        return None

    @property
    def history(self):
        return self._history


