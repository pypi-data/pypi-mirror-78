__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta

import requests
import requests.auth

from napoleontoolbox.bifrost.models.auth import Token, ClientCredentials, PasswordCredentials, Scope
from napoleontoolbox.bifrost.utils.security_headers import AuthorizationHeader, ApplicationJsonHeader


class AuthorizationHeaderManager(object):
    def __init__(self, token: Token):
        self.__token = token

    def build(self):
        return AuthorizationHeader.build(self.__token)


class AbstractAuthManagerTemplate(metaclass=ABCMeta):

    @abstractmethod
    def authenticate(self) -> Token: ...

    @abstractmethod
    def _request(self) -> requests.Request: ...

    @abstractmethod
    def _handle_reponse(self) -> requests.Request: ...

    @abstractmethod
    def _data(self): ...

    @abstractmethod
    def _auth(self): ...

    @property
    @abstractmethod
    def response(self): ...

    @property
    @abstractmethod
    def token(self): ...

    @property
    @abstractmethod
    def authorization_header(self): ...


class AuthManagerTemplate(AbstractAuthManagerTemplate):
    def __init__(self):
        self.__url = str()
        self.__credentials = None
        self.__scope = Scope()
        self.__response = requests.Response
        self.__token = Token()
        self.__authorization_header = str()

    @property
    def url(self):
        return self.__url

    @property
    def credentials(self):
        return self.__credentials

    @property
    def scope(self):
        return self.__scope

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, response):
        self.__response = response

    @property
    def authorization_header(self):
        return self.__authorization_header

    @authorization_header.setter
    def authorization_header(self, header: str):
        self.__authorization_header = header

    @property
    def token(self):
        return self.__token

    def _request(self) -> requests.Request: ...

    def _data(self): ...

    def _auth(self): ...

    def authenticate(self): ...


class AuthenticationManager(AuthManagerTemplate):

    def _auth(self):
        return requests.auth.HTTPBasicAuth(self.credentials.client_id, self.credentials.client_secret)

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    def _data(self):
        _temp = None
        if isinstance(self.credentials, ClientCredentials):
            _temp = {"grant_type": "{grant_type}"}
            _temp.update({"grant_type": self.credentials.__repr__()})
        elif isinstance(self.credentials, PasswordCredentials):
            _temp = {"username": "{username}", "password": "{password}", "grant_type": "{grant_type}"}
            _temp.update(
                {"username": self.credentials.user, "password": self.credentials.password,
                 "grant_type": self.credentials.__repr__()}
            )
        if _temp:
            return _temp
        return {}

    def _request_token(self):
        if self.url and self.credentials and self.scope:
            self.response = self._request()
            self._handle_reponse()

    def _handle_reponse(self):
        raise NotImplemented

    def _request(self):
        return requests.post(url=self.url, headers=ApplicationJsonHeader().build(), auth=self._auth(),
                             data=self._data())

    def authenticate(self):
        self._request_token()


class AbstractTemplateConnectorManager(metaclass=ABCMeta):

    @property
    @abstractmethod
    def authentication_manager(self):
        raise NotImplemented

    @property
    @abstractmethod
    def url(self):
        pass


class TemplateConnectorManager(AbstractTemplateConnectorManager):
    @property
    def authentication_manager(self) -> AuthenticationManager:
        return super(TemplateConnectorManager, self).authentication_manager()
    @property
    def url(self) -> str:
        return super(TemplateConnectorManager, self).url()


class AbstractTemplateConnector(metaclass=ABCMeta):

    @property
    @abstractmethod
    def connector_manager(self):
        raise NotImplemented


class TemplateConnector(AbstractTemplateConnector):
    @property
    def connector_manager(self) -> TemplateConnectorManager:
        return super(TemplateConnector, self).connector_manager()
