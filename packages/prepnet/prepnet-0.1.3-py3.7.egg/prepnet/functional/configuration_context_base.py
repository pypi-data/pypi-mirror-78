from typing import Dict, List
from prepnet.functional.function_configuration import FunctionConfiguration

class ConfigurationContextBase:
    def __init__(self, columns: List[str]):
        self.columns: List[str] = columns
        self.converters = []

    def to_config(self)->List[FunctionConfiguration]:
        configs = []
        for klass, args, kwargs in self.converters:
            configs.append(
                FunctionConfiguration(
                    self.columns, klass,
                    args, kwargs
                )
            )
        return configs

    def add_config(self, klass, *args, **kwargs):
        """Add converter

        Args:
            klass (type): Class of converter derrived ColumnConverterBase or FrameConverterBase
            *args, **kwargs: Arguments of the class constructor
        """
        self.converters.append((klass, args, kwargs))
