from typing import List
import pandas as pd
import numpy as np
from prepnet.core.frame_converter_base import FrameConverterBase
from prepnet.core.dataframe_array import DataFrameArray

class SplitConverter(FrameConverterBase):
    def __init__(self, n_split, shuffle=True):
        """Split dataframe

        Args:
            n_split ([type]): [description]
            shuffle (bool, optional): [description]. Defaults to True.
        """
        super().__init__()
        self.n_split = n_split
        self.shuffle = shuffle
        self.original_index = None

    def encode(self, df:pd.DataFrame):
        if self.shuffle:
            self.original_index = df.index
            indices = np.arange(len(df))
            np.random.shuffle(indices)
            shuffled_index = df.index[indices]
            df = df.loc[shuffled_index]
        start = 0
        result = DataFrameArray()
        for i in range(self.n_split):
            end = start + len(df) // self.n_split
            result.append(df.loc[df.index[start:end]])
            start = end
        return result

    def decode(self, df:List[pd.DataFrame]):
        df = pd.concat(df, axis=0)
        if self.original_index is not None:
            df = df.loc[self.original_index]
        return df
