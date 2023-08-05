from prepnet.core.config import get_config
from prepnet.core.frame_converter_base import FrameConverterBase
import pandas as pd

class DropNA(FrameConverterBase):
    def __init__(self):
        super().__init__()
        self.mask = None
        self.original = None
        self.original_dropped_index = None

    def encode(self, df:pd.DataFrame):
        mask = df.isna().any(axis=1)
        self.original_dropped_index = df.index[mask]
        if get_config('keep_original'):
            self.original = df.loc[mask]
        return df.dropna()

    def decode(self, df:pd.DataFrame):
        if self.original is not None:
            df = df.append(self.original)
        else:
            df = df.append(pd.DataFrame(
                None, index=self.original_dropped_index,
                columns=df.columns
            ))
        return df
        