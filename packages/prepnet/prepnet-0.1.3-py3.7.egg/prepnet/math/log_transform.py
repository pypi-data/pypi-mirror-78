import pandas as pd
import numpy as np
from prepnet.core.column_converter_base import ColumnConverterBase

class LogTransform(ColumnConverterBase):
    def __init__(self, interception=1.0):
        """Log transform with interception。:math:`log(x+b)`
        """
        super().__init__()
        self.interception = interception

    def encode(self, xs:pd.Series)->pd.Series:
        return np.log(xs + self.interception)

    def decode(self, xs:pd.Series)->pd.Series:
        return np.exp(xs) - self.interception