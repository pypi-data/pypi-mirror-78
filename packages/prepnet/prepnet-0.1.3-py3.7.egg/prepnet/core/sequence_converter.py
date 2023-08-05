from prepnet.core.column_converter_base import ColumnConverterBase
from typing import List

class SequenceConverter(ColumnConverterBase):
    def __init__(self, converters: List[ColumnConverterBase]):
        super().__init__()
        self.converters = converters

    def encode(self, xs):
        for conv in self.converters:
            xs = conv.encode(xs)
        return xs

    def decode(self, xs):
        for conv in reversed(self.converters):
            xs = conv.decode(xs)
        return xs

