from abc import ABCMeta, abstractmethod
import pandas as pd

class ColumnConverterBase(metaclass=ABCMeta):
    def __init__(self):
        self.origin = None

    @abstractmethod
    def encode(self, xs:pd.Series):
        raise NotImplementedError

    @abstractmethod
    def decode(self, xs:pd.Series):
        raise NotImplementedError
