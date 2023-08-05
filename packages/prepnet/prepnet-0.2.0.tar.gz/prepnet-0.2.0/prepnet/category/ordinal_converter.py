from prepnet.core.config import get_config
from prepnet.core.column_converter_base import ColumnConverterBase
import pandas as pd

class OrdinalConverter(ColumnConverterBase):
    def __init__(self, na_value:int=-1):
        """Ordinal transform for categorical data.

        Args:
            na_value (int, optional): NaN or NA value will assign this value. Defaults to -1.
        """
        super().__init__()
        self.na_value = na_value
        self.uniques = None

    def encode(self, xs:pd.Series):
        if self.uniques is None:
            codes, self.uniques = pd.factorize(xs, na_sentinel=self.na_value)
            return pd.Series(codes, index=xs.index, name=xs.name)
        else:
            return xs.replace({ v: i for i, v in enumerate(self.uniques)})

    def decode(self, xs:pd.Series):
        ys = pd.Series(
            self.uniques.take(xs), 
            name=xs.name
        )
        ys.index = xs.index
        return  ys