from prepnet.executor.state_value import StateValue
from prepnet.core.column_converter_base import ColumnConverterBase
from prepnet.core.frame_converter_base import FrameConverterBase
import pandas as pd
from typing import List, Dict

class FrameConverterContext(ColumnConverterBase):
    converters: Dict[FrameConverterBase, FrameConverterContext] = {}
    def __init__(self, frame_converter: FrameConverterBase):
        super().__init__()
        self.origin: FrameConverterBase = frame_converter
        if self.converters not in self.converters:
            self.converters[frame_converter] = self
            self.queued: List[pd.Series] = []

    async def encode_async(self, xs: pd.Series):
        if self.origin in self.converters:
            self.converters[self.origin].queue(xs)
        yield StateValue.Queued
        df = pd.DataFrame(self.queued)
        yield await self.origin.encode_async(df)

    async def decode_async(self, xs: pd.Series):
        if self.origin in self.converters:
            self.converters[self.origin].queue(xs)
        yield StateValue.Queued
        df = pd.DataFrame(self.queued)
        yield await self.origin.decode_async(df)

    def queue(self, xs: pd.Series):
        if self.converters[queue] == self:
            self.queued = []
        self.queued.append(xs)