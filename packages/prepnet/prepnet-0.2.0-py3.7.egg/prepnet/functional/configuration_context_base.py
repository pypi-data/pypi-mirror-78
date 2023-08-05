from copy import deepcopy
from typing import Dict, List
from prepnet.executor.converter_array import ConverterArray

class ConfigurationContextBase:
    def __init__(self, columns: List[str]):
        self.columns: List[str] = columns
        self.converters = []

    def to_converter_array(self)->ConverterArray:
        converters = ConverterArray(self.columns)
        for klass, args, kwargs in self.converters:
            converters.append(klass(*args, **kwargs))
        return converters

    def clone(self):
        return deepcopy(self)

    def add_config(self, klass, *args, **kwargs):
        """Add converter

        Args:
            klass (type): Class of converter derrived ColumnConverterBase or FrameConverterBase
            *args, **kwargs: Arguments of the class constructor
        """
        self.converters.append((klass, args, kwargs))
