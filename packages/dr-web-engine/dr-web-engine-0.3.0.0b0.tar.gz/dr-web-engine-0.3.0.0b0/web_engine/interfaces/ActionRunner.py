from interface import Interface
from interface import interface

from web_engine.interfaces.Action import Action
import re


class ActionRunner(Interface):
    """
    Implement this interface on objects that can execute Actions
    """

    @property
    def actions(self) -> dict:
        pass

    @property
    def history(self):
        pass

    @interface.default
    def register(self, action_name: str, action: Action):
        self.actions[action_name] = action

    def execute(self, action_composite: str):
        pass
