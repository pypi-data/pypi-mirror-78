from prepnet.executor.executor_base import ExecutorBase
from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.executor.converter_array import ConverterArray
from prepnet.core.dataframe_array import DataFrameArray
from prepnet.core.sequence_converter import SequenceConverter
from typing import List, Dict

import pandas as pd

class FrameExecutor(ExecutorBase):
    def __init__(self, converters:ConverterArray):
        self.converters = converters
        self.result_columns = None

    def encode(self, df: pd.DataFrame):
        if self.converters.columns is None:
            in_df = df
        else:
            in_df = df[self.converters.columns]

        if isinstance(in_df, DataFrameArray):
            out_df = in_df.apply(lambda x: SequenceConverter(self.converters).encode(in_df))
        else:
            out_df = SequenceConverter(self.converters).encode(in_df)

        # Modify columns

        self.result_columns = out_df.columns
        if self.converters.columns is None:
            # Modify index
            df = out_df
        else:
            if (len(out_df.columns) != len(self.converters.columns) or 
                    (out_df.columns != self.converters.columns).all()):
                df = df.drop(columns=self.converters.columns)
            if (out_df.index == in_df.index).all():
                df = df.assign(**{
                    col:series for col, series in out_df.items()
                })
            else:
                raise ValueError(
                    'Index is unmatched while column wise encoding.\n'
                    'If you want to modify the index, the columns should be None.\n'
                    f'Columns: {self.converters.columns}, Converter: {self.converters}'
                )

        return df

    def decode(self, df: pd.DataFrame):
        if self.converters.columns is None:
            in_df = df
        else:
            in_df = df[self.result_columns]
            df = df.drop(columns=self.result_columns)

        if isinstance(in_df, DataFrameArray):
            out_df = in_df.apply(lambda x: SequenceConverter(self.converters).decode(x))
        else:
            out_df = SequenceConverter(self.converters).decode(in_df)

        if self.converters.columns is None:
            df = out_df
        else:
            df = pd.concat([df, out_df], axis=1)

        return df


