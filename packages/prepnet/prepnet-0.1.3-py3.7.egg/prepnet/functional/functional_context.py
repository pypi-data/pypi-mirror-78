from contextlib import contextmanager
from typing import Any, List
from copy import deepcopy

import pandas as pd

from prepnet.executor.executor import Executor
from prepnet.functional.fixed_stage import FixedStage
from prepnet.functional.configuration_context import ConfigurationContext
from prepnet.functional.frame_context import FrameContext
from prepnet.core.null_converter import NullConverter

class FunctionalContext:
    """Functional style preprocess

    Examples:
        >>> context = FunctionalContext()
        >>> # Registering preprocesses
        >>> with context.enter() as f:
        >>>     f['tom'].ordinal()
        >>>     f['becky'].quantile(0.99).standardize()
        >>> with context.enter('secondaly') as f:
        >>>     f.split([0.8, 0.2], shuffle=True) # Apply frame context without accessor
        >>> context.encode(other_df) # Registered preprocesses will be applied.
        >>> context.disable('secondaly').encode(alt_df) # Split method will not be applied.
        >>> # Decoding preprocess can same as encode...
    """
    def __init__(self):
        self.stages: List[FixedStage] = []
        
        self.stage_name: str = '0'
        self.stage_index:int = 1
        
        self.current_stage_contexts: List[ConfigurationContext] = []

        self.stage_executors = None
        self.result_columns = None

        self.post_stage_context: FrameContext = None
        self.post_stage_status: bool = True
        self.post_executor = None

    @contextmanager
    def enter(self, stage_name:str=None)->"FunctionalContext":
        old_stage_name = self.stage_name
        old_stage = self.current_stage_contexts 
        
        if stage_name is None:
            self.stage_name = str(self.stage_index)
            self.stage_index += 1
        else:
            self.stage_name = stage_name
        self.current_stage_contexts  = []
        
        try:
            yield self
        finally:
            configs = []
            for context in self.current_stage_contexts:
                configs.extend(context.to_config())
            self.stages.append(
                FixedStage(self.stage_name,configs)
            )
            self.stage_name = old_stage_name
            self.current_stage_contexts = old_stage

    def __getitem__(self, keys)->ConfigurationContext:
        if not isinstance(keys, tuple):
            keys = (keys, )
        context = ConfigurationContext(keys)
        self.current_stage_contexts.append(context)
        return context

    def __getattr__(self, name):
        context = ConfigurationContext(None)
        self.current_stage_contexts.append(context)
        return getattr(context, name)
    
    @property
    def post(self):
        context = FrameContext(None)
        self.post_stage_context = context
        return context

    def create_converters(self):
        return [
            stage.create_converters()
            for stage in self.stages
            if stage.enable
        ]

    def disable(self, *keys)->"FunctionalContext":
        obj = self.clone()
        obj.stages = [
            stage.disable() if stage.stage_name in keys else stage
            for stage in obj.stages
        ]
        if 'post-process' in keys: # Post process
            obj.post_stage_status = False
        return obj

    def clone(self)->"FunctionalContext":
        context = FunctionalContext()
        context.stages = [
            stage.clone() for stage in self.stages
        ]
        
        context.stage_name = self.stage_name
        context.stage_index = self.stage_index
        
        context.post_stage_context = self.post_stage_context
        context.post_stage_status = self.post_stage_status

        return context

    def encode(self, df: pd.DataFrame):
        if self.stage_executors is None:
            self.stage_executors = []
            stage_converters = self.create_converters()
            for converters in stage_converters: # Create executor
                self.stage_executors.append(Executor(converters))

        for executor in self.stage_executors:
            df = executor.encode(df)

        if self.post_stage_context is not None:
            if self.post_executor is None: # Create executor
                converters = FixedStage(
                    'post-process', self.post_stage_context.to_config(),
                    enable=self.post_stage_status,
                ).create_converters()
                self.post_executor = Executor(converters)
            df = self.post_executor.encode(df)
        self.result_columns = df.columns
        return df

    def decode(self, df: pd.DataFrame):
        assert self.stage_executors is not None
        result_columns = self.result_columns
        if self.post_executor is not None:
            df = self.post_executor.decode(df)
        for executor in reversed(self.stage_executors):
            df = executor.decode(df)
        return df
