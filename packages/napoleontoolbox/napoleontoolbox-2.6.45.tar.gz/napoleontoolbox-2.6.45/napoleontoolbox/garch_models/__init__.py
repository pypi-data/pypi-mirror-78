__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List

from arch.univariate.volatility import GARCH
from pandas import Timestamp

from napoleontoolbox.backend.quote_service import NapoleonQuoteService
from napoleontoolbox.models.filter import EodQuoteFilter
from napoleontoolbox.models.product import EodQuoteProductCodeBuilder

filter = EodQuoteFilter(productCodes=EodQuoteProductCodeBuilder.product_code_generator(["ETH-USD", "BTC-USD"]),
                        minDate="2020-08-21",
                        maxDate="2020-08-24")
quotes = NapoleonQuoteService().filter(filter)


@dataclass(frozen=True)
class GarchEstimationParams(object):
    start_date: Timestamp = None
    end_date: Timestamp = None
    underlyings: List[str] = None
    p: int = 1
    o: int = 0
    q: int = 1


@dataclass(frozen=True)
class GarchEstimationResult(object):
    pass


class GarchEstimation(object):
    def __init__(self, params: GarchEstimationParams):
        self.__model = GARCH
        self.__quotes = list()
        self.__parameters = params

    def __post_init__(self):
        self.__load_data()

    @property
    def model(self):
        return self.__model

    @property
    def parameters(self):
        return self.__parameters

    def __load_data(self):
        if self.__parameters.start_date and self.__parameters.end_date and self.__parameters.underlyings:
            filter = EodQuoteFilter(
                productCodes=EodQuoteProductCodeBuilder.product_code_generator(self.__parameters.underlyings),
                minDate=self.__parameters.start_date.strftime("%Y-%m-%d"),
                maxDate=self.__parameters.start_date.strftime("%Y-%m-%d"))
            quotes = NapoleonQuoteService().filter(filter)
            if quotes is not None:
                self.__quotes = quotes
            else:
                raise Exception("Quote is none type : credentials")
        else:
            raise Exception("Missing parameters : check start_date ; end_date ; underlyings")


if __name__ == '__main__':
    params = GarchEstimationParams(
        start_date=Timestamp("2020-08-21"),
        end_date=Timestamp("2020-08-24"),
        underlyings=["ETH-USD", "BTC-USD"]
    )
    test = GarchEstimation(params)
