from typing import List, Dict
from collections import defaultdict

import pandas as pd

from prepnet.functional.function_configuration import FunctionConfiguration
from prepnet.functional.converter_array import ConverterArray
from prepnet.executor.executor import Executor

class FixedStage:
    def __init__(
        self, stage_name:str, 
        configs:List[FunctionConfiguration], 
        enable:bool=True
    ):
        self.stage_name = stage_name
        self.stage_configurations:List[FunctionConfiguration] = configs
        self.enable = enable

    def create_converters(self):
        all_converters = defaultdict(list)
        all_converters_array = None
        for config in self.stage_configurations:
            if not                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           self.enable:
                continue
            converters = config.create()
            if isinstance(converters, dict):
                for col, converter in converters.items():
                    all_converters[col].append(converter)
            else:
                if all_converters_array is None:
                    all_converters_array = ConverterArray(config.columns)
                all_converters_array.append(converters)
        assert len(all_converters) == 0 or all_converters_array is None, \
            'All converter should only be FrameConverter or ColumnConverter.'
        if all_converters_array is not None:
            return all_converters_array
        else:
            return all_converters

    def disable(self):
        stage = self.clone()
        stage.enable = False
        return stage

    def clone(self):
        stage = FixedStage(
            self.stage_name,
            [
                config.clone()
                for config in self.stage_configurations
            ],
            enable=self.enable,
        )
        return stage