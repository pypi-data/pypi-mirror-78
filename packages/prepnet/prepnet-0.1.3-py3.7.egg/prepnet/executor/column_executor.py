from prepnet.executor.executor_base import ExecutorBase
from prepnet.core.column_converter_base import ColumnConverterBase
from prepnet.core.sequence_converter import SequenceConverter
from typing import List, Dict

import pandas as pd

class ColumnExecutor(ExecutorBase):
    def __init__(self, converters:Dict[str, ColumnConverterBase]):
        self.converters = {}
        for key, converter in converters.items():
            if isinstance(converter, list):
                self.converters[key] = SequenceConverter(converter)
            else:
                self.converters[key] = converter 

    def encode(self, df: pd.DataFrame):
        for col, converter in self.converters.items():
            df = df.assign(**{col:converter.encode(df[col])})
        return df

    def decode(self, df: pd.DataFrame):
        for col, converter in self.converters.items():
            df = df.assign(**{col:converter.decode(df[col])})
        return df
