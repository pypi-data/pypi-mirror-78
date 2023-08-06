from web_engine.interfaces.Query import Query
from web_engine.utils.JsonReader import JsonReader

from interface import implements
import os
import json


class JsonQuery(implements(Query)):

    def __init__(self, json_query_path: str = None, json_query: dict = None):
        if json_query_path is None:
            if json_query is None:
                raise Exception('Please supply a json_query_path or a json_query')
            self.__data = json_query
            self.__json_query_path = None
            self.__status = True
            self.__json_reader = JsonReader(self.__data)
        else:
            self.__data = None
            self.__json_query_path = None
            self.__status = False
            self.__json_reader = None
            self.__load(json_query_path)
            if self.__status:
                self.__json_reader = JsonReader(self.__data)

    def load(self, query_def: dict = None, json_query_path: str = None) -> Query:
        if query_def is None:
            return self.load(json_query_path)
        return JsonQuery(json_query=query_def)

    def __load(self, json_query_path: str) -> Query:
        if not os.path.exists(json_query_path):
            self.__status = False
            raise Exception("File {} not found".format(json_query_path))
        try:
            with open(json_query_path) as json_file:
                data = json.load(json_file)
                self.__json_query_path = json_query_path
                self.__data = data
                self.__status = True
                self.__json_reader = JsonReader(self.__data)
                return self
        except Exception as ex:
            self.__status = False
            raise Exception("Unable to read json file {}, {}".format(json_query_path, ex))

    @property
    def query_def(self):
        return self.__data

    @property
    def query_items(self):
        return {key: value for key, value in self.__data.items() if not key.startswith('_')}

    @property
    def status(self):
        return self.__status

    @property
    def prop(self) -> JsonReader:
        if not self.__status:
            return None
        return self.__json_reader

    @property
    def pre_filters(self) -> list:
        return [{key: value} for key, value in self.__data.items() if key.startswith('_pre_')]
        # result = list()
        # for key, value in self.__data.items():
        #     if key.startswith('_pre_'):
        #         result.append({key: value})
        # return result
