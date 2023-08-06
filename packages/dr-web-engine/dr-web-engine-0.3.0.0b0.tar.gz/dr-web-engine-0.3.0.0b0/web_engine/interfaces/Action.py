from interface import Interface
from interface import interface

import logging


class Action(Interface):
    """
    Implement this interface to support action on the scraping engine
    """

    def execute(self, *args):
        pass




