from web_engine.interfaces.Scraper import Scraper
from web_engine.interfaces.ActionRunner import ActionRunner
from web_engine.engine.actions.ClickAction import ClickAction
from web_engine.engine.actions.FilterRemoveAction import FilterRemoveAction
from web_engine.engine.config.ScraperConfig import ScraperConfig
import geckodriver_autoinstaller

from interface import implements
import time
import re
from urllib.parse import urljoin

from selenium import webdriver
from xvfbwrapper import Xvfb

geckodriver_autoinstaller.install()


class SeleniumScraper(implements(Scraper, ActionRunner)):

    def __init__(self, log, config: ScraperConfig):
        self.log = log
        self.config = config
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', self.config.img.get())
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        if self.config.xvfb.get():
            self.display = Xvfb()
            self.display.start()

        self._driver = webdriver.Firefox(firefox_profile)

        self._driver.set_window_size(self.config.width.get(), self.config.height.get())
        self._driver.set_window_position(self.config.lat.get() or 0, self.config.lon.get() or 0)
        self.last_url = None
        self.last_page = None
        self._actions = {}
        self._history = []

        click = ClickAction(self, self.log)
        filter_remove = FilterRemoveAction(self, self.log)
        self.register('click', click)
        self.register('remove', filter_remove)

    @property
    def actions(self) -> dict:
        return self._actions

    def get_doc(self, doc):
        """
        get the html element from the url [doc]
        :param doc: the url to the page
        :return: html.from string content
        """
        self._driver.get(doc)
        page_source = self.driver.page_source
        self.last_url = doc
        self.last_page = page_source
        return self.last_page

    def get(self):
        page_source = self._driver.page_source
        self.last_page = page_source
        return self.last_page

    def action_get(self, actions: list):
        for x in actions:
            self.execute(x)
        return self.get()

    def filter_get(self, filters: list):
        for x in filters:
            self.execute_filter(x)
        return self.get()

    @property
    def history(self):
        return self._history

    def execute_filter(self, filter_def: dict):
        action_name, action_path = next(iter(filter_def.items()))
        action_name = action_name.strip().replace('_pre_', '')
        if action_name in self._actions.keys():
            self._history.append((time.time(), action_name))
            self._actions[action_name].execute(action_path)
        else:
            self.log.warn(f"Command [{action_name}] not recognised")

    def execute(self, action_composite: str):
        action_name, action_path = SeleniumScraper.__get_action(action_composite)
        action_name = action_name.strip()
        if action_name in self._actions.keys():
            self._history.append((time.time(), action_name))
            self._actions[action_name].execute(action_path)
        else:
            self.log.warn(f"Command [{action_name}] not recognised")

    @property
    def driver(self):
        return self._driver

    def make_absolute_url(self, url):
        return urljoin(self.last_url, url)

    @staticmethod
    def __get_action(action_composite):
        pattern = '{(.+?)}'
        matches = re.search(pattern, action_composite)
        if not matches:
            return None, None
        action_name = matches.group(1)
        action_xpath = re.sub(pattern, '', action_composite)
        return action_name, action_xpath

    def __del__(self):
        if self.driver is not None:
            try:
                time.sleep(10)  # wait for operations to complete before closing
                if hasattr(self, "_driver"):
                    self.driver.close()
                if self.config.xvfb.get():
                    self.display.stop()
            except Exception as ex:
                self.log.error(ex)
                pass

