import pandas as pd
from prepnet.core.column_converter_base import ColumnConverterBase

class ConverterReference(ColumnConverterBase):
    def __init__(self, converter: ColumnConverterBase):
        super().__init__()
        self.origin = converter

    async def encode_async(self, xs:pd.Series):
        async for i in self.origin.encode_async(xs):
            yield i

    async def decode_async(self, xs:pd.Series):
        async for i in self.origin.decode_async(xs):
            yield i

    def encode(self, xs:pd.Series):
        return self.origin.encode(xs)

    def decode(self, xs:pd.Series):
        return self.origin.decode(xs)
