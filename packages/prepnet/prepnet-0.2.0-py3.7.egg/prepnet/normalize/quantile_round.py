from prepnet.core.column_converter_base import ColumnConverterBase
from prepnet.core.config import get_config

import pandas as pd

class QuantileRound(ColumnConverterBase):
    def __init__(self, percentile=0.99):
        """Outlier removal using n-th percentile .

        Args:
            percentile (float, optional): [description]. Defaults to 0.99.
        """
        super().__init__()
        self.percentile = percentile
        self.upper = None
        self.lower = None
        self.lower_mask = None
        self.upper_mask = None

    def encode(self, xs:pd.Series)->pd.Series:
        if self.upper is None:
            upper = xs.quantile(self.percentile)
            lower = xs.quantile(1.0 - self.percentile)
            self.upper = upper
            self.lower = lower
        else:
            upper = self.upper
            lower = self.lower

        upper_mask = xs > upper
        lower_mask = xs < lower

        if get_config('keep_original'):
            self.lower_mask = lower_mask
            self.lower_original_values = xs[self.lower_mask]
            self.upper_mask = upper_mask
            self.upper_original_values = xs[self.upper_mask]

        xs = xs.mask(upper_mask, upper)
        xs = xs.mask(lower_mask, lower)

        return xs

    def decode(self, xs:pd.Series)->pd.Series:
        if self.lower_mask is not None:
            xs = xs.mask(self.lower_mask, other=self.lower_original_values)
        if self.upper_mask is not None:
            xs = xs.mask(self.upper_mask, other=self.upper_original_values)
        return xs
