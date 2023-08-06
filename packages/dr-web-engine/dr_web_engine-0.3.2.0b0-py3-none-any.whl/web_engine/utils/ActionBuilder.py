from web_engine.interfaces import Action


class ActionBuilder:

    @staticmethod
    def build(action_string: str) -> Action:
        pass

    @staticmethod
    def build(action_strings: dict) -> Action:
        return [ActionBuilder.build(x) for _, x in action_strings.items()]
