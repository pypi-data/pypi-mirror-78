import asyncio
from typing import Any, List
from enum import Enum, auto

from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.core.column_converter_base import ColumnConverterBase

from prepnet.executor.conversion_plan import ConversionPlan
from prepnet.executor.column_executor import ColumnExecutor
from prepnet.executor.frame_executor import FrameExecutor
from prepnet.executor.executor_base import ExecutorBase

from prepnet.functional.converter_array import ConverterArray

import pandas as pd

class Executor(ExecutorBase):
    class Executors(Enum):
        ColumnExecutor = auto()
        FrameExecutor = auto()

    def __init__(self, converters: List[ConversionPlan], columns:List[str]=None):
        self.converters = converters
        self.columns = columns 
        self.enable = True

        self.executor_type = self.validate_converters(converters)
        if self.executor_type == self.Executors.ColumnExecutor:
            self.impl = ColumnExecutor(converters)
        elif self.executor_type == self.Executors.FrameExecutor:
            self.impl = FrameExecutor(converters, columns=converters.columns)

    def encode(self, df: pd.DataFrame):
        if self.enable:
            return self.impl.encode(df)
        else:
            return df

    def decode(self, df: pd.DataFrame):
        if self.enable:
            return self.impl.decode(df)
        else:
            return df

    def validate_converters(self, converters):
        if isinstance(converters, ConverterArray) and issubclass(type(converters[0]), FrameConverterBase):
            return Executor.Executors.FrameExecutor
        else:
            return Executor.Executors.ColumnExecutor
