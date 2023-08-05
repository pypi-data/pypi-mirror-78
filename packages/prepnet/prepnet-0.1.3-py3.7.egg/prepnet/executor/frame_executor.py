from prepnet.executor.executor_base import ExecutorBase
from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.core.dataframe_array import DataFrameArray
from typing import List, Dict

import pandas as pd

class FrameExecutor(ExecutorBase):
    def __init__(self, converters:List[FrameConverterBase], columns: List[str]=None):
        if columns is not None:
            self.columns = list(columns) 
        else:
            self.columns = None
        self.result_columns = None
        self.converters = converters

    def encode(self, df: pd.DataFrame):
        if self.columns is None:
            self.columns = df.columns
            input_df = None
        else:
            input_df = df.drop(columns=self.columns)
            df = df[self.columns]
        for converter in self.converters:
            df = converter.encode(df)
        if self.result_columns is None:
            self.result_columns = df.columns
        
        if input_df is None:
            return df
        else:
            return pd.concat([input_df, df], axis=1)

    def decode(self, df: pd.DataFrame):
        assert self.result_columns is not None
        input_df = df.drop(columns=self.result_columns)
        df = df[self.result_columns]
        for converter in self.converters:
            df = converter.decode(df)
        if isinstance(input_df, DataFrameArray):
            if isinstance(df, DataFrameArray):
                return DataFrameArray(
                    pd.concat(i, d) for i, d in zip(input_df, df)
                )
            elif all(input_df._apply(lambda x: x.empty)):
                return df
            else:
                raise ValueError(
                    'Unexpected decoding due to type mismatch or shape mismatch.\n'
                )
        else:
            return pd.concat([input_df, df], axis=1)
