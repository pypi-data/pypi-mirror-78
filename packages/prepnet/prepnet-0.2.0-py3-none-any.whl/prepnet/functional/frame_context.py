from typing import Dict, List

from prepnet.core.module import copydoc
from prepnet.functional.configuration_context_base import ConfigurationContextBase

from prepnet.functional.function_configuration import FunctionConfiguration

from prepnet.core.lambda_converter import LambdaConverter
from prepnet.category.onehot_converter import OnehotConverter
from prepnet.impute.drop_na import DropNA
from prepnet.extra.split_converter import SplitConverter

class FrameContext(ConfigurationContextBase):
    @copydoc(OnehotConverter)
    def onehot(self):
        self.add_config(OnehotConverter)
        return self

    @copydoc(DropNA)
    def drop_na(self):
        self.add_config(DropNA)
        return self

    @copydoc(SplitConverter)
    def split(self, n_split, shuffle=True):
        self.add_config(SplitConverter, n_split, shuffle)
        return self

    @copydoc(LambdaConverter)
    def lambda_converter(self, encode, decode):
        self.add_config(LambdaConverter, encode, decode)
        return self
