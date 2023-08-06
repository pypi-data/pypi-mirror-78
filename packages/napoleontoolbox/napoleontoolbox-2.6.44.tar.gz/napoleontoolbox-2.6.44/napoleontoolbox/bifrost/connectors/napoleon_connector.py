__author__ = "hugo.inzirillo"

import requests

from napoleontoolbox.bifrost.models.auth import Scope, Token
from napoleontoolbox.bifrost.headers import AuthenticationManager, AuthorizationHeaderManager, \
    TemplateConnectorManager
from napoleontoolbox.bifrost.utils.auth_handler import AuthResponseHandlerTemplate
from napoleontoolbox.dataloader.models import NapoleonService
from napoleontoolbox.napoleon_config_tools import getter


class NapoleonServiceAuthHandler(AuthResponseHandlerTemplate):

    def _get_token(self):
        return self._response["access_token"]

    def _get_token_type(self):
        return str(self._response["token_type"]).capitalize()

    def get_token(self):
        _token = Token()
        _token.value = self._get_token()
        _token.type = self._get_token_type()
        return _token


class NapoleonAuthenticationManager(AuthenticationManager):

    @property
    @getter(value="providers.napoleon_service.access_token_uri")
    def url(self):
        return self.url

    @property
    def credentials(self):
        return NapoleonService().get_credentials()

    @property
    def scope(self):
        return Scope(["READ"])

    def _handle_reponse(self):
        if self.response:
            if self.response.status_code == requests.codes.OK:
                _reponse = self.response.json()
                self.token = NapoleonServiceAuthHandler(_reponse).get_token()
                self.authorization_header = AuthorizationHeaderManager(self.token).build()


class NapoleonConnectorManager(TemplateConnectorManager):
    def __init__(self):
        self.__authentication_manager = NapoleonAuthenticationManager()
        self.__url = str()
        self.authentication_manager.authenticate()

    @property
    def authentication_manager(self):
        return self.__authentication_manager

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url
