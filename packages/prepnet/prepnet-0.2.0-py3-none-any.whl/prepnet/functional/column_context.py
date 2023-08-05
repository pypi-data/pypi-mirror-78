from typing import Dict, List

from prepnet.core.module import copydoc
from prepnet.functional.configuration_context_base import ConfigurationContextBase

from prepnet.functional.function_configuration import FunctionConfiguration

from prepnet.core.lambda_converter import LambdaConverter
from prepnet.core.astype_converter import AsTypeConverter
from prepnet.category.onehot_converter import OnehotConverter
from prepnet.category.ordinal_converter import OrdinalConverter
from prepnet.normalize.quantile_round import QuantileRound
from prepnet.normalize.standardize import Standardize
from prepnet.math.exp_transform import ExpTransform
from prepnet.math.log_transform import LogTransform
from prepnet.impute.fill_na import FillNA
from prepnet.time.frequency_time import FrequencyTimeConverter

class ColumnContext(ConfigurationContextBase):
    @copydoc(OnehotConverter)
    def onehot(self):
        self.add_config(OnehotConverter)
        return self

    @copydoc(OrdinalConverter)
    def ordinal(self):
        self.add_config(OrdinalConverter)
        return self

    @copydoc(Standardize)
    def standardize(self):
        self.add_config(Standardize)
        return self

    @copydoc(Standardize)
    def rescale_variance(self):
        self.add_config(Standardize)
        return self

    @copydoc(QuantileRound)
    def quantile_round(self, percentile:float=0.99):
        self.add_config(QuantileRound, percentile)
        return self

    @copydoc(FillNA)
    def fill_na(self, value=0.0, by=None):
        self.add_config(FillNA, value, by)
        return self

    @copydoc(LambdaConverter)
    def convert_lambda(self, encode, decode):
        self.add_config(LambdaConverter, encode, decode)
        return self

    @copydoc(ExpTransform)
    def exp(self):
        self.add_config(ExpTransform)
        return self

    @copydoc(LogTransform)
    def log(self, interception: float=1.0):
        self.add_config(LogTransform, interception)
        return self

    @copydoc(AsTypeConverter)
    def astype(self, dtype):
        self.add_config(AsTypeConverter, dtype)
        return self

    @copydoc(FrequencyTimeConverter)
    def datetime_to_index(self, start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
        self.add_config(FrequencyTimeConverter, start, end, periods, freq, tz, normalize, name, closed)
        return self