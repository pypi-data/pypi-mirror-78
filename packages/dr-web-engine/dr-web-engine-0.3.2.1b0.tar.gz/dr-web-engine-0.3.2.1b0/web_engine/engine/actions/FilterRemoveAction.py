from web_engine.interfaces.Action import Action

import logging
from interface import implements


class FilterRemoveAction(implements(Action)):

    def __init__(self, receiver, log: logging = None):
        self._log = log
        self._receiver = receiver

    def execute(self, *args):
        if args is None or len(args) != 1:
            return
        xpath_selector: str = args[0]
        elements = self._receiver.driver.find_elements_by_xpath(xpath_selector)
        if elements is not None:
            for element in elements:
                try:
                    self._receiver.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)
                except Exception as ex:
                    if self._log:
                        self._log.warn(ex)

