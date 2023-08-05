from abc import ABCMeta, abstractmethod
from typing import Union, List

import pandas as pd

class ExecutorBase(metaclass=ABCMeta):
    @abstractmethod
    def encode(self, df: Union[pd.Series, pd.DataFrame]):
        raise NotImplementedError()

    @abstractmethod
    def decode(self, df: Union[pd.Series, pd.DataFrame]):
        raise NotImplementedError()
