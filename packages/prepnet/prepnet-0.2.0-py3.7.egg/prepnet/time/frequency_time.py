import pandas as pd
import numpy as np

from prepnet.core.config import get_config
from prepnet.core.column_converter_base import ColumnConverterBase

class FrequencyTimeConverter(ColumnConverterBase):
    def __init__(self, start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
        """datetime to index of time period or frequency.
            All arguments passed pandas.

        Args:
            start (str or datetime-like, optional): 
                Left bound for generating dates. Defaults to None.
            end (str or datetime-like, optional): 
                Right bound for generating dates. Defaults to None.
            periods (int, optional): 
                Number of periods to generate. Defaults to None.
            freq (str or DateOffset, optional): 
                Frequency strings can have multiples, e.g. '5H'. See
                :ref:`here <timeseries.offset_aliases>` for a list of
                frequency aliases. Defaults to None.
            tz (str or tzinfo, optional): 
                Time zone name for returning localized DatetimeIndex, for example
                'Asia/Hong_Kong'. By default, the resulting DatetimeIndex is
                timezone-naive. Defaults to None.
            normalize (bool, optional):
                Normalize start/end dates to midnight before generating date range.
                Defaults to False.
            closed (str, optional): 
                {None, 'left', 'right'}
                Make the interval closed with respect to the given frequency to
                the 'left', 'right', or both sides (None, the default).
        """
        self.date_range = None
        self.start = start
        self.end = end
        self.freq = freq
        self.periods = periods
        self.freq = freq
        self.tz = tz
        self.normalize = normalize
        self.name = name
        self.closed = closed

    def encode(self, xs:pd.Series)->pd.Series:
        if self.date_range is None:
            self.date_range = pd.date_range(
                self.start, self.end, self.periods, self.freq, self.tz, 
                self.normalize, closed=self.closed
            )
        
        result = pd.Series(
            np.zeros_like(xs, dtype=np.int64),
            index=xs.index, name=xs.name
        )
        for i, (start, end) in enumerate(zip(self.date_range, self.date_range[1:])):
            result[xs.between(start, end)] = i
        if get_config('keep_original'):
            self.original_xs = xs
        return result

    def decode(self, xs:pd.Series)->pd.Series:
        if get_config('keep_original'):
            return self.original_xs
        else:
            return pd.Series(self.date_range.take(xs))