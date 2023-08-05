__author__ = "hugo.inzirillo"

from collections import OrderedDict
from dataclasses import dataclass
from time import time, sleep

import requests

ITERATION = 10

response = requests.get("https://www.bitmex.com/api/v1/orderBook/L2?symbol=eth&depth=100000").json()
response2 = requests.get("https://www.bitmex.com/api/v1/orderBook/L2?symbol=xbt&depth=100000").json()
response = response +response2

def time_this(original_function):
    def new_function(*args, **kwargs):
        import datetime
        before = datetime.datetime.now()
        x = original_function(*args, **kwargs)
        after = datetime.datetime.now()
        print("Elapsed Time = {0}".format(after - before))
        return x

    return new_function


class Quote(object):
    def __init__(self, product_code, ts, close):
        self.__product_code = product_code
        self.__ts = ts
        self.__close = close


"https://www.bitmex.com/api/v1/orderBook/L2?symbol=eth&depth=100000"


@dataclass(init=False)
class BitMexOrder:
    symbol: str
    id: int
    side: str
    price: float

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.__dict__ = dict_object
            return self

    def __hash__(self):
        return hash((self.symbol, self.id, self.side, self.price))


class QuoteSlottedPk(object):
    __slots__ = ("product_code", "ts")

    def __init__(self, product_code: str, ts: float):
        self.product_code = product_code
        self.ts = ts

    def __hash__(self):
        return hash((self.product_code, self.ts))

    def __eq__(self, other):
        return self.product_code == other.product_code and self.ts == other.ts if isinstance(other,
                                                                                             self.__class__) else False


class QuoteSlotted(object):
    __slots__ = ("close", "pk")

    def __init__(self, pk, close):
        self.close = close
        self.pk = pk

    def __hash__(self):
        return hash((self.pk, self.close))

    def __eq__(self, other):
        return self.pk.__eq__(other.pk) if isinstance(other, self.__class__) else False


def test3():
    res = OrderedDict()
    for iter in range(ITERATION):
        quote = QuoteSlotted(QuoteSlottedPk("Okayebifibzeifbziefbizuebfizebifbziuef", time()), iter)
        res[quote.pk] = quote
        sleep(0.01)
    return res


@time_this
def bitmex2(response):
    return (BitMexOrder().from_dict(item) for item in response)


if __name__ == '__main__':
    gen = test3()

    carnet2 = bitmex2(response)


