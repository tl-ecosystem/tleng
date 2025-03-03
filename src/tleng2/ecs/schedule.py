# Copyright (c) 2023 Theolaos

# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to 
# whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the 
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from inspect import signature
from typing import get_args
from dataclasses import dataclass, field

from .sequence import Sequence
from .system import System

from typing import Literal as _Literal
from typing import Any as _Any



class SceneComp:
    """
    Here for symbolic reasons
    """


class StateNotFound(Exception):
    pass


SEQUENCE_TYPES = _Literal[
    'First', 
    'PreUpdate', 
    'Update', 
    'PostUpdate', 
    'PreRenderer', 'Renderer',
    'Last',
    'StateTransition', 'SceneTransition'
    'PreStartup', 
    'Startup', 
    'PostStartup'
]


sequence_types: list[str] = [
    *get_args(SEQUENCE_TYPES)
]


SEQUENCE_ORDER = _Literal[
    'Update',
    'Startup',
    'SceneTransition',
    'StateTransition'
]


UPDATE_ORDER: list[str] = ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']
STARTUP_ORDER: list[str] = ['PreStartUp', 'Startup']

# scene_transition_order_enter: list[str] = ['OnSceneEnter']
# scene_transition_order_exit: list[str] = ['OnSceneExit']

# state_transition_order_enter: list[str] = ['OnStateEnter']
# state_transition_order_exit: list[str] = ['OnStateExit']


def _ScheduleComp_default_factory() -> dict[SEQUENCE_TYPES, list[System]]:
    return {key: [] for key in sequence_types}


@dataclass
class SchedulerComp:
    sequences: dict[str, Sequence] = field(default_factory=_ScheduleComp_default_factory)
    cached_system_sequence_types: list[SEQUENCE_TYPES] = field(default_factory=list)


class Scheduler:
    def __init__(self) -> None:
        self.sequences: dict[str, Sequence] = {key: Sequence() for key in sequence_types}
        self.cached_system_sequence_types: list[SEQUENCE_TYPES] = []


    def add_systems(self, sequence_type: SEQUENCE_TYPES, *systems) -> None:
        print(sequence_type)
        self._add_cached_system_sequence(sequence_type)
        print(self.cached_system_sequence_types)

        self.sequences[sequence_type].add_systems(*systems)


    def add_sequences(self, **sequences: Sequence) -> None:
        """
        write the name of the sequence as a parameter, and then the Sequence as the value of the parameter
        """
        for seq_type, sequence in sequences:
            self.sequences[seq_type] = sequence

        # Every sequence added here, should be new to the scheduler
        self._add_cached_system_sequence(*list(sequences.keys()))


    def init(self, parameters: dict[type, _Any]) -> None:
        """
        Initializes all the sequences that were added in the scheduler with the parameters.
        """
        for sequence in self.sequences.values():
            sequence.init(parameters)

        
    def update(self) -> None:
        # for sequence in self.sequences.values():
        #     sequence.update()
        # print(self.cached_system_sequence_types)
        for key in self.cached_system_sequence_types:
            self.sequences[key].update()


    def _add_cached_system_sequence(self, *new_sequence_type: SEQUENCE_TYPES, order: list[str] = UPDATE_ORDER) -> None:
        """
        Appends the new_sequence_type to the cached_system_sequence_types,
        and then it sorts it out.
        """
        for seq_type in new_sequence_type:
            if seq_type not in self.cached_system_sequence_types:
                self.cached_system_sequence_types.append(seq_type)     

        self.cached_system_sequence_types = sorted(
            self.cached_system_sequence_types, 
            key = lambda x: order.index(x)
        )

    
    def return_scheduler_component(self) -> SchedulerComp: 
        """
        Used from the scenes_manager to change scenes
        
        :schedule_component: It can be a `SchedulerComp` of even a plain `Scheduler`  
        :returns: Nothing
        """
        return SchedulerComp(
            self.sequences
        )


    def load_scheduler_component(self, scheduler_component: SchedulerComp) -> None:
        """
        Used from the scenes_manager to change scenes
        
        :schedule_component: It can be a `SchedulerComp` or even a plain `Scheduler`  
        :returns: Nothing
        """
        self.sequences = scheduler_component.sequences
        self.cached_system_sequence_types = scheduler_component.cached_system_sequence_types


def _merge_to_scene_schedulers(scene_comp_list: list[SceneComp], scheduler: Scheduler) -> None:
    """
    Takes the list from the scene components, and injects the schedule of the scenecomp to the schedule of the App.

    Should always be ran before the initilization of the sequences
    """
    for scene in scene_comp_list:
        for seq_type in scheduler.cached_system_sequence_types:
            # for some unknown reason, this is faster than calling the schedule.add_systems method.
            # if scene.scheduler.system_schedule[seq_type]:
            #     scene.scheduler.system_schedule[seq_type].extend(scheduler.system_schedule[seq_type])
            # else:
            #     scene.scheduler.system_schedule.update(
            #         {
            #             seq_type :  scheduler.system_schedule[seq_type]
            #         }
            #     )
            # # print(seq_type, scene.schedule.system_schedule[seq_type])
            # scene.scheduler.system_schedule[seq_type].sort(
            #     key=lambda syst: syst.priority, reverse=True
            # )

            # TODO When reimplementing the sequence handling of systems and sets
            # TODO Somehow implement some kind of ordering for single threaded applications 
            # (maybe sequences are not needed...)
            try:
                scene.scheduler.sequences[seq_type].system_sets.extend(scheduler.sequences[seq_type].system_sets)
            except KeyError as key:
                print(f"Key error occured <{key}>, error handled")
                scene.scheduler.sequences[seq_type] = scheduler.sequences[seq_type].system_sets

        scene.scheduler._add_cached_system_sequence(*scheduler.cached_system_sequence_types)
        print(scene.scheduler.cached_system_sequence_types)


def _scenes_init(scenes: dict[str, SceneComp], parameters: dict[type, _Any]) -> None:
    """
    Instantiates the systems on their parameters. It analyzes the parameters and injects what they asked for.
    """

    for scene in scenes.values():
        for sequence in scene.scheduler.sequences.values():
            sequence.init(parameters)

    # try:
    #     all_systems: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in sequence_types}
    #     for key, scene in scenes.items():
    #         for seq_type, system_list in scene.schedule.system_schedule.items():
    #             all_systems[seq_type] += system_list
    #     # self.system_schedule.items()
    #     for key, systems in all_systems.items():
    #         for system in systems:
    #             syst_param_signature = signature(system.parameters)
    #             params = syst_param_signature.parameters
    #             # Determine which parameters to inject based on type annotations
    #             injection_args = []
    #             for param in params.values():
    #                 annotation = param.annotation
    #                 injection_args.append(parameters[annotation])
    #             system.parameters(*injection_args)
    # except KeyError as key:
    #     print(f"""KeyError occured, 
    #               - <{key}> was wrongly typed in the parameters of the systems
    #               - key: <{key}> was either not initialized in app or 
    #               - <{key}> was not properly put in the parameter of the app""")
