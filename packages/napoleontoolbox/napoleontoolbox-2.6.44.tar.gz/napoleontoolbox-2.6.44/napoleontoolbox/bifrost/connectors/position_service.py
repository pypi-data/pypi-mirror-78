__author__ = "hugo.inzirillo"

from typing import List

from napoleontoolbox.bifrost.connectors.napoleon_connector import NapoleonConnectorManager
from napoleontoolbox.bifrost.headers import TemplateConnector
from napoleontoolbox.bifrost.models.filter import SignalComputationFilter
from napoleontoolbox.bifrost.utils.rest_template import Post


class NapoleonPositionServiceConnector(TemplateConnector):
    def __init__(self):
        self.__connector_manager = NapoleonConnectorManager()
        self.__connector_manager.url = "https://api.napoleonx.ai/quote-service/v1/eod-quote"

    @property
    def connector_manager(self):
        return self.__connector_manager

    def authenticate(self):
        self.connector_manager.authentication_manager.authenticate()

    @Post("/filter")
    def filter(self, data: SignalComputationFilter = None) -> List[dict]:
        """

        Parameters
        ----------
        data
        kwargs

        Returns
        -------

        """
        pass
