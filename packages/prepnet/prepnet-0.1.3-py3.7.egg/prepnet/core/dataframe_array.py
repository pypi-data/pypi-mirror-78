import pandas as pd

class IterateWrapper:
    def __init__(self, iter_df, key):
        self.iter_df = iter_df
        self.key = key

    def __call__(self, *args, **kwargs):
        results = DataFrameArray()
        for df in self.iter_df:
            results.append(
                getattr(df, self.key)(*args, **kwargs)
            )
        return results

class DataFrameArray(list):
    def get(self, *keys):
        return super().__getitem__(*keys)

    def _apply(self, method, *args, **kwargs):
        return [
            method(df, *args, **kwargs) for df in self
        ]

    @property
    def index(self):
        return pd.concat([i.index for i in self])

    @property
    def columns(self):
        return self.get(0).columns if len(self) > 0 else None

    def __getitem__(self, *keys):
        return DataFrameArray(
            df.__getitem__(*keys) for df in self
        )

    def __getattr__(self, key):
        return IterateWrapper(self, key)