from typing import List

from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.core.column_converter_base import ColumnConverterBase

class FunctionConfiguration:
    """Data class of the function configuration
    """
    def __init__(self, columns, klass, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.converter_klass = klass
        self.columns = columns

    def create_frame_converter(self):
        return self.converter_klass(
            *self.args, **self.kwargs
        )

    def create_column_converter(self):
        if isinstance(self.columns, str):
            return {
                self.columns: self.converter_klass(
                    *self.args, **self.kwargs
                )
            }
        else:
            return {
                col: self.converter_klass(
                    *self.args, **self.kwargs
                ) for col in self.columns
            }

    def create(self):
        if issubclass(self.converter_klass, FrameConverterBase):
            return self.create_frame_converter()
        elif issubclass(self.converter_klass, ColumnConverterBase):
            return self.create_column_converter()
        else:
            raise TypeError(
                'Converter class should derrive ColumnConverterBase: ' + 
                str(type(self.converter_klass))
            )

    def clone(self):
        return FunctionConfiguration(
            self.columns, self.converter_klass,
            self.args, self.kwargs
        )