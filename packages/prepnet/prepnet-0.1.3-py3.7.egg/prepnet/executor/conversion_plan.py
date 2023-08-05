from typing import List
import pandas as pd

from prepnet.core.column_converter_base import ColumnConverterBase

class ConversionPlan:
    def __init__(self, converters:List[ColumnConverterBase], columns: List[str]):
        self.converters = converters
        self.columns = columns

    def is_valid(self, df:pd.DataFrame):
        return True