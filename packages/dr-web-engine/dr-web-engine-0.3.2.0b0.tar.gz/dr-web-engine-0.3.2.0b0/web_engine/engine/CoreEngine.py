from web_engine.interfaces.Engine import Engine
from web_engine.interfaces.Parser import Parser
from web_engine.interfaces.Query import Query

from interface import implements
import logging


class CoreEngine(implements(Engine)):

    def __init__(self, parser: Parser, query: Query, log: logging = None, context=None):
        if log is None:
            logging.basicConfig(level=logging.ERROR)
            self.log = logging.getLogger('Engine')
        else:
            self.log = log

        self.parser = parser
        self.query = query
        self.context = context

    def process(self) -> dict:
        if not self.query.status:
            return None

        doc = self.query.prop._doc.get()
        if doc:
            self.context = self.parser.get_doc_element(doc)

        if self.context is None:
            return None

        return self.__process()

    def __process(self) -> dict:
        result = dict()

        self.log.info("XPathEngine::__process -> query: {}".format(self.query.query_def))

        for key, value in self.query.query_items.items():
            self.log.info("XPathEngine::__process -> key, value {}, {}".format(key, value))
            type_value = type(value)
            self.log.info("XPathEngine::__process -> value type {}".format(type_value))

            if type_value == type(None):
                break
            if type_value in [str, int, float, bool]:
                result.update(self._process_item(key, value, self.context))
            if type_value == list:
                if result.get(key) is None:
                    result[key] = list()
                temp_return = self.__process_array(self.query.load(query_def=value[0]))
                result[key].extend(temp_return)
            if type_value == dict:
                x = CoreEngine(self.parser, self.query.load(query_def=value),
                               context=self.context, log=self.log)
                result.update({key: x.process()})

        self.log.info("XPathEngine::__process -> result {}".format(result))
        return result

    def __process_array(self, inner_query: Query) -> list:
        result = list()
        html_element = self.context

        if inner_query.prop._doc.get():
            return self._process_doc(inner_query)

        pre_filters = inner_query.pre_filters
        if len(pre_filters) > 0:
            html_element = self._apply_pre_filter(pre_filters)

        _base_path = inner_query.prop._base_path.get()
        if not _base_path:
            self.log.warning("XPathEngine::_process_array -> _base_path was not present")
            _base_path = "//*"
            # return result

        self.log.info("XPathEngine::_process_array -> xpath {}".format(_base_path))
        selector = self.parser.get_element(html_element, _base_path)
        if len(selector) == 0:
            self.log.warning("XPathEngine::_process_array -> selector length was 0")
            return result

        _key = inner_query.prop._key.get()

        for item in selector:
            self.log.info("XPathEngine::_process_array -> selector.item {}".format(item))

            inner_context = self.parser.get_inner_element(item)
            x = CoreEngine(self.parser, inner_query.load(inner_query.query_def), context=inner_context, log=self.log)
            if _key:
                result.append({_key: x.process()})
            else:
                result.append(x.process())

        if self.query.prop._follow.get():
            next_url = self.parser.get_element(html_element, self.query.prop._follow.get())

            if next_url is not None and len(next_url) > 0:

                if self.query.prop._follow_action.get():
                    action = self.query.prop._follow_action.get()
                    next_html_element = self.parser.get_doc_element_by_actions([action])
                    result.extend(CoreEngine(self.parser, inner_query, self.log, next_html_element).
                                  __process_array(inner_query))
                else:
                    next_url = self.parser.make_absolute_url(next_url[0])
                    next_html_element = self.parser.get_doc_element(next_url)
                    result.extend(CoreEngine(self.parser, inner_query, self.log, next_html_element).
                                  process_array(inner_query))

        self.log.info("XPathEngine::__process_array -> return result {}".format(result))
        return result

    def _process_item(self, key, value, html_element):

        self.log.info("XPathEngine::__process_item -> input key,value {}".format(key, value))

        self.log.info("XPathEngine::__process_item -> input html_elements {}".format(html_element))

        result = self.parser.get_items(value, html_element)

        self.log.info("XPathEngine::__process_item -> return result {}".format(result))
        return {key: result}

    def _process_doc(self, inner_query: Query) -> list():
        self.log.info("XPathEngine::_process_array -> doc {}".format(inner_query.prop.doc.get()))
        html_element = self.parser.get_doc_element(inner_query.prop._doc.get())
        del inner_query.query_def['_doc']
        inner_query = inner_query.load(query_def=inner_query.query_def)
        return CoreEngine(self.parser, inner_query, context=html_element, log=self.log).__process_array(inner_query)

    def _apply_pre_filter(self, filters: list):
        return self.parser.get_doc_element_by_filter(filters)
