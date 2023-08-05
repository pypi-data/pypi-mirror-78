from prepnet.core.config import get_config
from prepnet.core.column_converter_base import ColumnConverterBase
import pandas as pd

class NanImputer(ColumnConverterBase):
    """NaN filled by value.
    """
    def __init__(self, value:float=0.0):
        super().__init__()
        self.value = value
        self.mask = None

    def encode(self, df:pd.DataFrame):
        if get_config('keep_original'):
            self.mask = df.isna()
        return df.fillna(self.value)

    def decode(self, df:pd.DataFrame):
        if self.mask is not None:
            df = df.mask(self.mask)
        return df
