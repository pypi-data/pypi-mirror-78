from web_engine.interfaces.Action import Action

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from interface import implements
import logging


class ClickAction(implements(Action)):

    def __init__(self, receiver, log: logging = None):
        self._log = log
        self._receiver = receiver

    def execute(self, *args):
        if args is None or len(args) != 1:
            return
        xpath_selector: str = args[0]
        wait = WebDriverWait(self._receiver.driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_selector)))
        elem.click()

