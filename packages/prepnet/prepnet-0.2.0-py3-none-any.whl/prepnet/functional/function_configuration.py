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

    def clone(self):
        return FunctionConfiguration(
            self.columns, self.converter_klass,
            self.args, self.kwargs
        )