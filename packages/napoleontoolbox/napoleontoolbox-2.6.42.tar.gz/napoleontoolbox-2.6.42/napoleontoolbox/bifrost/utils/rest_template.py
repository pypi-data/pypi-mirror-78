__author__ = "hugo.inzirillo"

import json
from dataclasses import is_dataclass

import requests

from npxlogger import log


class Get(object):
    def __init__(self, flag: str):
        self.__flag = flag
        self.__header = dict()
        self.__connector = None

    @property
    def flag(self):
        return self.__flag

    @flag.setter
    def flag(self, flag):
        self.__flag = flag

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = header

    @property
    def connector(self):
        return self.__connector

    @connector.setter
    def connector(self, connector):
        self.__connector = connector

    def __call__(self, original_func):
        def wrappee(connector=None, **kwargs):
            self.connector = connector
            self.__fill_request(**kwargs)

            log.info("Api call rest end_point : {}".format(self.flag))
            log.info("header {}".format(self.header))
            return requests.get(url=self.flag, headers=self.header)

        return wrappee

    def __fill_request(self, **kwargs):
        if hasattr(self.connector, '__authentication_manager') and self.connector.authentication_manager is not None:
            self.header = self.connector.authentication_manager().authenticate().authorization_header
        else:
            self.header = None
        try:
            self.flag = self.flag.format(**kwargs)
        except Exception as e:
            log.error(e.args)


class Post(object):
    def __init__(self, flag: str):
        self.__flag = flag
        self.__header = dict()
        self.__connector = None

    @property
    def flag(self):
        return self.__flag

    @flag.setter
    def flag(self, flag):
        self.__flag = flag

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = header

    @property
    def connector(self):
        return self.__connector

    @connector.setter
    def connector(self, connector):
        self.__connector = connector

    def __call__(self, original_func):
        def wrappee(connector=None, **kwargs):

            try:
                self.connector = connector
                if "data" in kwargs:
                    data = self.__check_data(data=kwargs["data"])
                    self.__fill_request(**kwargs)
                    url = self.connector.connector_manager.url + self.flag
                    return self.__handle_response(response=requests.post(url=url, headers=self.header, data=data))
                else:
                    log.error("missing data in request {}".format(self.flag))
            except Exception as e:
                log.error(e.args)

        return wrappee

    def __check_data(self, data):
        if is_dataclass(data) and data is not None:
            try:
                data = data.__dict__
                return json.dumps(data)
            except RuntimeError as e:
                log.error(e.args)
                log.error("data {}".format(data))

    def __fill_request(self, **kwargs):
        if hasattr(self.connector.connector_manager,
                   'authentication_manager') and self.connector.connector_manager.authentication_manager is not None:
            self.header = self.connector.connector_manager.authentication_manager.authorization_header
        else:
            self.header = None
        try:
            self.flag = self.flag.format(**kwargs)
        except Exception as e:
            log.error(e.args)

    def __handle_response(self, response: requests.Response):
        try:
            if response.status_code == requests.status_codes.codes.OK:
                return response.json()
            elif response.status_code == requests.status_codes.codes.CREATED:
                return response
        except Exception as e:
            log.error(e.args)
