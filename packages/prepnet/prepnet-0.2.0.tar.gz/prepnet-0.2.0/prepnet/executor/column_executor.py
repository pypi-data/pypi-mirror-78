from typing import List, Dict
from copy import deepcopy

import pandas as pd

from prepnet.executor.executor_base import ExecutorBase
from prepnet.core.column_converter_base import ColumnConverterBase
from prepnet.core.sequence_converter import SequenceConverter
from prepnet.executor.converter_array import ConverterArray


class ColumnExecutor(ExecutorBase):
    def __init__(self, converters: ConverterArray):
        self.converters = {
            col: SequenceConverter([
                deepcopy(converter)
                for converter in converters
            ])
            for col in converters.columns
        }

    def encode(self, df: pd.DataFrame):
        results = {}
        for col, converter in self.converters.items():
            results[col] = converter.encode(df[col])
        df = df.assign(**results)
        return df

    def decode(self, df: pd.DataFrame):
        results = {}
        for col, converter in self.converters.items():
            results[col] = converter.decode(df[col])
        df = df.assign(**results)
        return df
