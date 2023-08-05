from abc import ABCMeta, abstractmethod
import pandas as pd

class ColumnConverterBase(metaclass=ABCMeta):
    def __init__(self):
        self.origin = None

    async def encode_async(self, xs:pd.Series):
        yield self.encode(xs)

    async def decode_async(self, xs:pd.Series):
        yield self.decode(xs)

    @abstractmethod
    def encode(self, xs:pd.Series):
        raise NotImplementedError

    @abstractmethod
    def decode(self, xs:pd.Series):
        raise NotImplementedError
