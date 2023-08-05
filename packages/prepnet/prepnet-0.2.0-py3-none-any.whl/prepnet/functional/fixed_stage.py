from typing import List, Dict
from collections import defaultdict

import pandas as pd

# from prepnet.functional.function_configuration import FunctionConfiguration
from prepnet.functional.configuration_context_base import ConfigurationContextBase
from prepnet.executor.converter_array import ConverterArray
from prepnet.executor.executor import Executor

class FixedStage:
    def __init__(
        self, stage_name:str, 
        configs:List[ConfigurationContextBase], 
        enable:bool=True
    ):
        self.stage_name = stage_name
        self.stage_configurations:List[ConfigurationContextBase] = configs
        self.enable = enable

    def create_converters(self):
        return [
            context.to_converter_array()
            for context in self.stage_configurations
        ]

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