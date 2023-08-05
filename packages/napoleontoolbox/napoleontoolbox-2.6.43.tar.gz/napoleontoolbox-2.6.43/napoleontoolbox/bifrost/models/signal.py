__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List


@dataclass
class SignalComputation:
    """
    Position Service
    Mapping of Java Objects
    """
    productCode: List[str] = None
    underlyingCode: List[str] = None
    ts: str = None
    value: float = None

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.__dict__ = dict_object
            return self
