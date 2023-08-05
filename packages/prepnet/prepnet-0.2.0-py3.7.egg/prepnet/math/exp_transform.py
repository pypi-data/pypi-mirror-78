import pandas as pd
import numpy as np
from prepnet.core.column_converter_base import ColumnConverterBase

class ExpTransform(ColumnConverterBase):
    def __init__(self):
        """Expornential transform
        """
        super().__init__()

    def encode(self, xs:pd.Series)->pd.Series:
        return np.exp(xs)

    def decode(self, xs:pd.Series)->pd.Series:
        return np.log(xs)