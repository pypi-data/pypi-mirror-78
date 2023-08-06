from __future__ import absolute_import, division, print_function

import copy

from vivarium.library.dict_utils import deep_merge_combine_lists
from vivarium.core.process import Process, Generator


class TimelineProcess(Process):

    name = 'timeline'

    defaults = {
        'timeline': []}

    def __init__(self, initial_parameters=None):
        if initial_parameters is None:
            initial_parameters = {}

        self.timeline = copy.deepcopy(
            self.or_default(initial_parameters, 'timeline'))

        # get ports
        self.ports = {'global': ['time']}
        for event in self.timeline:
            for state in event[1].keys():
                port = {state[0]: [state[1:]]}
                self.ports = deep_merge_combine_lists(self.ports, port)

        parameters = {'timeline': self.timeline}
        super(TimelineProcess, self).__init__(parameters)

    def ports_schema(self):

        schema = {
            port: {
                '*': {}}
            for port in list(self.ports.keys())
            if port not in ['global']}

        schema.update({
            'global': {
                'time': {
                    '_default': 0,
                    '_updater': 'accumulate'}}})
        return schema

    def next_update(self, timestep, states):
        time = states['global']['time']
        update = {'global': {'time': timestep}}
        for (t, change_dict) in self.timeline:
            if time >= t:
                for state, value in change_dict.items():
                    port = state[0]
                    variable = state[1]
                    if port not in update:
                        update[port] = {}
                    update[port][variable] = {
                        '_value': value,
                        '_updater': 'set'}
                self.timeline.pop(0)
        return update


TimelineProcess()
