from prepnet.core.config import get_config
from prepnet.core.column_converter_base import ColumnConverterBase
import pandas as pd

class FillNA(ColumnConverterBase):
    """NaN filled by value.
    """
    def __init__(self, value:float=0.0, by=None):
        super().__init__()
        self.value = value
        self.by = by
        self.mask = None

    def encode(self, xs:pd.Series):
        if get_config('keep_original'):
            self.mask = xs.isna()
        if self.by is not None:
            return xs.fillna(getattr(xs, self.by)())
        else:
            return xs.fillna(self.value)

    def decode(self, xs:pd.Series):
        if self.mask is not None:
            xs = xs.mask(self.mask)
        return xs
