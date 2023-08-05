import pandas as pd

from prepnet.core.column_converter_base import ColumnConverterBase

class AsTypeConverter(ColumnConverterBase):
    def __init__(self, dtype):
        """As type converter
        """
        self.dtype = None
        self.original_dtype = None

    def encode(self, xs:pd.Series):
        self.original_dtype = xs.dtype
        return xs.astype(self.dtype)

    def decode(self, xs:pd.Series):
        return xs.astype(self.original_dtype)
