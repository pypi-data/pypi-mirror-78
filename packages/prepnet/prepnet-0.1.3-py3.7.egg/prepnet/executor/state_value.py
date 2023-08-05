from enum import Enum, auto

class StateValue(Enum):
    Prepared = auto()
    Queued = auto()
    Running = auto()
    Finished = auto()