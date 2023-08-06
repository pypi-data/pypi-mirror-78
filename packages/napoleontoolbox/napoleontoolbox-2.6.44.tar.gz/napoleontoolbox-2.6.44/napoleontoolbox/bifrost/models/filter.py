__author__ = "hugo.inzirillo"

from dataclasses import dataclass

from typing import List


@dataclass(frozen=True)
class SignalComputationFilter:
    """
    Position Service
    Mapping of Java Objects
    """
    productCodes: List[str]
    underlyingCodes: List[str] = None
    minTs: str = None
    maxTs: str = None
    lastOnly: bool = False

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "SignalComputationFilter{productCodes=" + str(
            self.productCodes) + ", minTs=" + self.minTs + ", maxTs=" + self.maxTs + ", lastOnly=" + str(
            self.lastOnly) + '}'


@dataclass(frozen=True)
class EodQuoteFilter:
    """
    Position Service
    Mapping of Java Objects
    """
    productCodes: List[str]
    underlyingCodes: List[str] = None
    minDate: str = None
    maxDate: str = None
    lastOnly: bool = False

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "EodQuoteFilter{productCodes=" + str(
            self.productCodes) + ", minDate=" + self.minDate + ", maxDate=" + self.maxDate + ", lastOnly=" + str(
            self.lastOnly) + '}'


if __name__ == '__main__':
    filter = SignalComputationFilter("test", "test", "test").to_dict()

    SignalComputationFilter(productCodes="STRAT_BTC_USD_D_3")
    end = True
