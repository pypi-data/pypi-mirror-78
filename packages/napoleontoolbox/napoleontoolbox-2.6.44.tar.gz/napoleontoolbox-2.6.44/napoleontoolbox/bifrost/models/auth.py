__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta
from enum import Enum


class AbstractCredentials(metaclass=ABCMeta):

    @abstractmethod
    def _client_id(self):
        raise NotImplemented

    @abstractmethod
    def _client_secret(self):
        raise NotImplemented

    @abstractmethod
    def _user(self):
        raise NotImplemented

    @abstractmethod
    def _password(self):
        raise NotImplemented


class ClientCredentials(AbstractCredentials):
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.__client_id = client_id
        self.__client_secret = client_secret

    @property
    def client_id(self):
        return self._client_id

    @property
    def _client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def _client_secret(self):
        return self.__client_secret

    @property
    def _user(self):
        return None

    @property
    def _password(self):
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "client_credentials"


class PasswordCredentials(AbstractCredentials):
    def __init__(self, client_id: str = None, client_secret: str = None,
                 user: str = None, password: str = None):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__user = user
        self.__password = password

    @property
    def client_id(self):
        return self._client_id

    @property
    def _client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def _client_secret(self):
        return self.__client_secret

    @property
    def user(self):
        return self._user

    @property
    def _user(self):
        return self.__user

    @property
    def password(self):
        return self._password

    @property
    def _password(self):
        return self.__password

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "password"


class TokenType(Enum):
    BEARER = "Bearer"
    BASIC = "Basic"


class Token(object):
    def __init__(self):
        self.__value = None
        self.__type = TokenType.BEARER.value

    def __repr__(self):
        return self.__type + " " + self.__value

    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        return self.__type

    @value.setter
    def value(self, value):
        self.__value = value

    @type.setter
    def type(self, type):
        self.__type = type


class Scope(list):
    pass
