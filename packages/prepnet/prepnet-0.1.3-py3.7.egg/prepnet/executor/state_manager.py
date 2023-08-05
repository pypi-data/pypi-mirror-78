from dataclasses import dataclass
from typing import Dict
from prepnet.executor.state_value import StateValue

class StateManager(dict):
    @dataclass
    class State:
        status: StateValue
        origin: object
        column: str

    def __init__(self, converters: Dict[str, object]):
        super().__init__(State)
        for key, converter in converters.items():
            self[converter] = State(
                state=StateValue.Prepared,
                origin=converter.origin,
                columns=key,
            )

    def prepare(self, converter):
        state = self[converter]
        state.status = StateValue.Prepared

    def set_prepare(self):
        for key in self.keys():
            self.prepare(key)

    def is_prepared(self, converter):
        return self[converter].status == StateValue.Prepared

    def queue(self, converter, ):
        self[converter].status = StateValue.Queued

    def is_queued(self, converter):
        return self[converter].status == StateValue.Queued

    def run(self, converter):
        state = self[converter]
        state.status = StateValue.Running

    def is_running(self, converter):
        return self[converter].status == StateValue.Running

    def finish(self, converter):
        self[converter].status = StateValue.Finished

    def is_finished(self, converter):
        return self[converter].status == StateValue.Running

    def is_all_finished(self):
        return all([self[k] == StateValue.Finished for k in self.key()])

    def is_all_queued(self):
        return all([self[k] == StateValue.Queued for k in self.key()])
