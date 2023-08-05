import asyncio
from typing import Any, List
from enum import Enum, auto

from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.core.column_converter_base import ColumnConverterBase

from prepnet.executor.column_executor import ColumnExecutor
from prepnet.executor.frame_executor import FrameExecutor
from prepnet.executor.executor_base import ExecutorBase

from prepnet.executor.converter_array import ConverterArray

import pandas as pd

class Executor(ExecutorBase):
    class Executors(Enum):
        ColumnExecutor = auto()
        FrameExecutor = auto()

    def __init__(self, converters: List[ConverterArray]):
        self.converters = converters
        self.enable = True

        self.executors = []
        for converter_array in converters:
            self.executor_type = self.validate_converters(converter_array)
            if self.executor_type == self.Executors.ColumnExecutor:
                impl = ColumnExecutor(converter_array)
            elif self.executor_type == self.Executors.FrameExecutor:
                impl = FrameExecutor(converter_array)
            self.executors.append(impl)

    def encode(self, df: pd.DataFrame):
        if not self.enable:
            return df
        for executor in self.executors:
            df = executor.encode(df)
        return df

    def decode(self, df: pd.DataFrame):
        if not self.enable:
            return df
        for executor in self.executors:
            df = executor.decode(df)
        return df

    def validate_converters(self, converters):
        if isinstance(converters, ConverterArray) and issubclass(type(converters[0]), FrameConverterBase):
            return Executor.Executors.FrameExecutor
        else:
            return Executor.Executors.ColumnExecutor
