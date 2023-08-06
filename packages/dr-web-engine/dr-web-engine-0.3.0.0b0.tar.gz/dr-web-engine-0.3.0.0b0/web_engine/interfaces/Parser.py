from interface import Interface


class Parser(Interface):
    """
    Implement this interface to support multiple parsing methods for example XPath and DOM and/or to use different
    parsing engines
    """

    def get_doc_element(self, doc):
        pass

    def get_element(self, html_element, xpath):
        pass

    def get_items(self, value: str, html_element) -> list:
        pass

    def get_inner_element(self, element, actions=None):
        pass

    def make_absolute_url(self, url):
        pass

    def get_doc_element_by_actions(self, actions: list):
        pass

    def get_doc_element_by_filter(self, filters: list):
        pass
