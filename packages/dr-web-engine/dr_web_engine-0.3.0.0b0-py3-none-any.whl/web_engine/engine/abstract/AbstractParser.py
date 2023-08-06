from web_engine.interfaces.Parser import Parser
from web_engine.interfaces.Scraper import Scraper

from interface import implements
from lxml import html, etree
import requests
from urllib.parse import urljoin

import logging


class AbstractParser(implements(Parser)):

    def __init__(self, scraper: Scraper, log: logging = None):
        self.log = log
        self.last_tree: etree = None
        self.last_element: html.HtmlElement = None
        self.last_inner_element = None
        self.last_items: list = None
        self.last_url: str = None
        self.scraper = scraper

    def get_doc_element(self, doc):
        '''
        get the html element from the url [doc]
        :param doc: the url to the page
        :return: html.from string content
        '''
        return self.scraper.get_doc(doc)

    def get_items(self, value: str, html_element) -> list:
        if type(html_element) is str:
            html_element = html.fromstring(html_element)
        if type(html_element) is bytes:
            html_element = html.fromstring(html_element.decode("utf-8"))
        xpath_result = html_element.xpath(value)
        result = list()
        for x in xpath_result:
            if type(x) == html.HtmlElement:
                result.append(x.text)
            else:
                result.append(x)

        self.last_items = result
        return self.last_items

    def get_element(self, html_element, xpath):
        if type(html_element) is str:
            html_element = html.fromstring(html_element)
        if type(html_element) is bytes:
            html_element = html.fromstring(html_element.decode("latin1"))
        self.last_element = html_element.xpath(xpath)
        return self.last_element

    def get_inner_element(self, element, actions=None):
        self.last_inner_element = html.fromstring(etree.tostring(element, pretty_print=True))
        return self.last_inner_element

    def make_absolute_url(self, url):
        return urljoin(self.last_url, url)

    def get_doc_element_by_actions(self, actions: list):
        return self.scraper.action_get(actions)

    def get_doc_element_by_filter(self, filters: list):
        return self.scraper.filter_get(filters)



