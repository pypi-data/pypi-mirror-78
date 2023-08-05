from abc import ABCMeta, abstractmethod
import pandas as pd

class FrameConverterBase(metaclass=ABCMeta):
    def __init__(self):
        self.origin = None

    @abstractmethod
    def encode(self, xs:pd.DataFrame):
        raise NotImplementedError

    @abstractmethod
    def decode(self, xs:pd.DataFrame):
        raise NotImplementedError
