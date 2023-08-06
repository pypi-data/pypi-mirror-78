__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta


class AbstractAuthResponseHandlerTemplate(metaclass=ABCMeta):

    @property
    @abstractmethod
    def _response(self):
        raise NotImplemented

    @abstractmethod
    def _get_token(self):
        raise NotImplemented

    @abstractmethod
    def _get_token_type(self):
        raise NotImplemented

    @abstractmethod
    def get_token(self):
        raise NotImplemented


class AuthResponseHandlerTemplate(AbstractAuthResponseHandlerTemplate):
    def __init__(self, _reponse: dict):
        self.__reponse = _reponse

    @property
    def _response(self):
        return self.__reponse

    def _get_token(self): ...

    def _get_token_type(self): ...

    def get_token(self): ...
