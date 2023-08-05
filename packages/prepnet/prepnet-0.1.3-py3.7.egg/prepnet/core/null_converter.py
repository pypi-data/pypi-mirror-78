import pandas as pd

from prepnet.core.column_converter_base import ColumnConverterBase
from prepnet.core.frame_converter_base import FrameConverterBase

class NullConverter(FrameConverterBase, ColumnConverterBase):
    """None conversion
    """
    def __init__(self):
        self.origin = None

    def encode(self, xs:pd.Series):
        return xs

    def decode(self, xs:pd.Series):
        return xs
