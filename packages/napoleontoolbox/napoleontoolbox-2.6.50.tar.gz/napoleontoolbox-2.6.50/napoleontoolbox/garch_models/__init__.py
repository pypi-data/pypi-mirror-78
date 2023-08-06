__author__ = "hugo.inzirillo"

from collections import OrderedDict
from dataclasses import dataclass
from typing import List

from pandas import Timestamp, Series, DataFrame
from pandas._libs.tslibs.timedeltas import Timedelta
from statsmodels.stats.diagnostic import acorr_lm

from napoleontoolbox.garch_models.dataloader import NapoleonDataLoader, NapoleonDataLoaderParams
from napoleontoolbox.garch_models.plot import tsplot
from napoleontoolbox.garch_models.stats_factory import ArchTestResult
from napoleontoolbox.models.quote import EodQuote
from napoleontoolbox.utils.factory import EodQuoteFactory


@dataclass(frozen=True)
class GarchEstimationParams(object):
    start_date: Timestamp = None
    end_date: Timestamp = None
    underlyings: List[str] = None
    quotes: List[EodQuote] = None
    p: int = 1
    o: int = 0
    q: int = 1


@dataclass(frozen=True)
class GarchEstimationResult(object):
    pass


class GarchEstimation(object):
    def __init__(self, params: GarchEstimationParams):
        self.__quotes = OrderedDict()
        self.__parameters = params
        GarchEstimation.__post_init__(self)

    def __post_init__(self):
        self.__load_data()

    @property
    def quotes(self):
        return self.__quotes

    def ts_plot(self):
        prices = Series(self.quotes).sort_index()
        returns = (prices / prices.shift(1) - 1).dropna()
        return tsplot(returns, lags=20)

    @property
    def parameters(self):
        return self.__parameters

    def get_epsilon_squared(self):
        s = Series(self.quotes).sort_index()
        return (((s / s.shift(1) - 1) - (s / s.shift(1) - 1).mean()) ** 2).dropna()

    def __load_data(self):
        if self.__parameters.quotes is None:
            dataloader_params = NapoleonDataLoaderParams(self.__parameters.start_date, self.__parameters.end_date,
                                                         self.__parameters.underlyings)
            quotes = NapoleonDataLoader(dataloader_params).quotes
            if quotes is not None:
                self.__quotes = EodQuoteFactory().to_ordered_dict(quotes)
            else:
                raise Exception("Quote is none type : credentials should be checked")
        else:
            self.__quotes = EodQuoteFactory().to_ordered_dict(self.__parameters.quotes)
        return self

    def residuals_autocorr_test(self):
        lm_stat, lm_pval, f_stat, f_val = acorr_lm(self.get_epsilon_squared().values, nlags=20)
        res = ArchTestResult(lm_stat, lm_pval, f_stat, f_val)
        return DataFrame.from_dict(res.__dict__, orient="index")


if __name__ == '__main__':
    params = GarchEstimationParams(
        start_date=Timestamp.utcnow() - Timedelta(days=360),
        end_date=Timestamp.utcnow() - Timedelta(minutes=60),
        underlyings=["ETH-USD"]
    )
    garch = GarchEstimation(params)
    garch.ts_plot()
    arch_test = garch.residuals_autocorr_test()
    end = True
