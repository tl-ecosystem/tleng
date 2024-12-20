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

from .system import System

from typing import Literal as _Literal
from typing import Any as _Any


class SceneComp:
    """
    Here for symbolic reasons
    """


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
# TODO General ideas for states in scheduler
# What if we treat our states like sequance orders, like what if when we create a Pause state, underneath it there are systems that work with that state, if the
# game gets unpaused then then that sequence type gets removed from the list and the systems that it had don't run anymore..
# 
# The other more brutal idea is to just a good data structure (or use an existing one like hashmaps) that supports fast looksup for systems and
# every time we switch state some systems are enabled some other are disabled.
# 
# Best of both worlds: Use both :) nope


def _ScheduleComp_default_factory() -> dict[SEQUENCE_TYPES, list[System]]:
    return {key: [] for key in sequence_types}


@dataclass
class ScheduleComp:
    system_schedule: dict[SEQUENCE_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    cached_system_sequence_types: set[SEQUENCE_TYPES] = field(default_factory=set)

    system_state_order: list[str] = field(default_factory=list)


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        # current running scheduling for systems
        self.system_schedule: dict[str, list[System]] = {key: [] for key in sequence_types}
        self.cached_system_sequence_types: list[SEQUENCE_TYPES] = []

        self.system_state_order: list[str] = UPDATE_ORDER
        self.state_groups: dict[str, str] = {}

        self.state_changed = False
        self.temp_system_state_order: list[str] = UPDATE_ORDER
        self.temp_state_groups: dict[str, str] = {}


    def _add_cached_system_sequence(self, *new_sequence_type: SEQUENCE_TYPES, order: list[str] = UPDATE_ORDER) -> None:
        """
        Appends the new_sequence_type to the cached_system_sequence_types,
        and then it sorts it out.
        """
        self.cached_system_sequence_types.extend(new_sequence_type)

        self.cached_system_sequence_types = sorted(
            self.cached_system_sequence_types, 
            key = lambda x: order.index(x)
        )


    def add_state(self, state_name: str, *systems: System) -> None:
        """
        Adds a state after Update (or every other state that is after Update)
        """
        assert state_name not in UPDATE_ORDER

        self.system_schedule[state_name] = systems
        self.system_state_order.insert(self.system_state_order.index('Update') + 1, state_name)

    
    def create_state_group(self, state_group_name: str, start_with:str, *state_names: str) -> None:
        """
        Creates a state group from all the created states.

        :state_group_name: The state group name
        :start_with: With which state from the state group should it start
        :*state_names: Include all the states that the state group should have (even the one starting with)
        """
        assert state_group_name not in UPDATE_ORDER

        self.state_groups[state_group_name] = [start_with, state_names]
        self.enable(start_with)

    
    def move_state(self,
                state_name: str,
                before_position: str = "", 
                after_position: str = "", 
        ) -> None:
        """
        Moves a specified state to another place after or before, another state.

        There are 7 default states, that always exist:
        ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']

        :state_name: the name of the state you want to move.
        :before_position: pass here the name of your selected state to be before (exaple ['selected_state','passed_state'])
        :after_position: pass here the name of your selected state to be after (exaple ['passed_state', 'selected_state'])
        :return: Returns mothing.

        WARNING: Don't input both `before_position` and `after_position` arguments, or else an error will be thrown. 
        You must only provide one of the two arguments, with the ability to provide a default as well        
        """
        assert before_position and after_position

        try:
            if before_position:
                self.system_state_order.insert(self.system_state_order.index(before_position), state_name)
            elif after_position:
                self.system_state_order.insert(self.system_state_order.index(after_position) + 1, state_name)
            
        except ValueError as e:
            print('Caught ValueError:', e, 'is not in the system_state_order. Make sure that you have created the state in this schedule')


    def move_state_group(self,
                state_group_name: str,
                before_position: str = "", 
                after_position: str = "", 
        ) -> None:
        """
        Experimental!

        Moves a state group to another place after or before, another default state.

        There are 7 default states, that always exist:
        ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']

        :state_group_name: the name of the state group you want to move.
        :before_position: pass here the name of your selected state to be before (exaple ['selected_state','passed_state'])
        :after_position: pass here the name of your selected state to be after (exaple ['passed_state', 'selected_state'])
        :return: Returns mothing.

        WARNING: Don't input both `before_position` and `after_position` arguments. 
        You must only provide one of the two arguments, with the ability to provide a default as well        
        """
        ...


    def enable_state(self, state_name: str) -> None:
        """
        Enables a specific state.
        """
        self._add_cached_system_sequence(state_name, self.system_state_order)
        
    
    def disable_state(self, state_name: str) -> None:
        """
        Disables a specific state that isn't one of the default states:
        ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']
        """
        assert state_name not in UPDATE_ORDER

        self.cached_system_sequence_types.remove(state_name)

        
    def change_state(self, state_group: str, state_name: str) -> None:
        """
        From the passed state group, it changes the state to the one passed.
        Frees the programmer from constantly checking to disable the other active state from
        the state group.
        
        Example:
        ```
        'MyPausedState' = ['Paused', 'Running']
        current_state = 'Paused'
        # with change_state you can change 'Paused' to 'running'
        ```
        """
        assert state_name in self.state_groups[state_group][1]

        self.disable_state(self.state_groups[state_group][0])
        self.enable_state(state_name)
        # Assigning the new state_name as the running state of the state group
        self.state_groups[state_group][0] = state_name


    def add_systems(self, sequence_type: SEQUENCE_TYPES, *systems) -> None:
        """
        Add systems in the scheduler.

        :return: Nothing
        """
        # I am not sure if the line below is slow
        self.system_schedule[sequence_type] += systems
        self.system_schedule[sequence_type].sort(
            key=lambda syst: syst.priority, reverse=True
        )

        self._add_cached_system_sequence(sequence_type)
    

    #TODO: unneeded wasteful code! Garbaj logic!
    def load_systems_from_scenes(self, scenes: dict[str, SceneComp]) -> None:
        for key, scene in scenes.items():
            self.system_schedule.update(scene.schedule.system_schedule)


    def init(self, parameters: dict[type, _Any]) -> None:
        """
        Instantiates the systems on their parameters. It analyzes the parameters 
        and injects what they asked for.
        """
        try:
            # self.system_schedule.items()
            for key, systems in self.system_schedule.items():
                for system in systems:
                    syst_param_signature = signature(system.parameters)
                    params = syst_param_signature.parameters

                    # Determine which parameters to inject based on type annotations
                    injection_args = []

                    for param in params.values():
                        annotation = param.annotation

                        injection_args.append(parameters[annotation])

                    system.parameters(*injection_args)
        except KeyError as key:
            print(f"""KeyError occured, 
                      - <{key}> was wrongly typed in the parameters of the systems
                      - key: <{key}> was either not initialized in app or 
                      - <{key}> was not properly put in the parameter of the app""")
            
    
    def update(self) -> None:
        """
        According to what the resources say the right systems will run.
        """            
        for key in self.cached_system_sequence_types:
            for system in self.system_schedule.setdefault(key,[]):
                if system.enabled:
                    system.update() # by design (not a bug, it's a feature!)

        # TODO Change the state, if it was changed here.
        if self.state_changed:
            self.state_groups = self.temp_state_groups
            self.system_state_order = self.temp_system_state_order

    
    # for this to be done efficiently (from the schedule) we need to use sets
    def disable_system(self,) -> None:
        ...


    def enable_system(self,) -> None:
        ...

    
    def return_schedule_component(self) -> ScheduleComp: 
        """
        Used from the scenes_manager to change scenes
        
        :schedule_component: It can be a `ScheduleComp` of even a plain `Schedule`  
        :returns: Nothing
        """
        return ScheduleComp(
            self.system_schedule, 
            self.cached_system_sequence_types, 
        )


    def load_schedule_component(self, schedule_component: ScheduleComp) -> None:
        """
        Used from the scenes_manager to change scenes
        
        :schedule_component: It can be a `ScheduleComp` of even a plain `Schedule`  
        :returns: Nothing
        """
        self.system_schedule = schedule_component.system_schedule
        self.cached_system_sequence_types = schedule_component.cached_system_sequence_types


def _merge_to_scene_schedulers(scene_comp_list: list[SceneComp], scheduler: Schedule) -> None:
    """
    Takes the list from the scene components, and injects the schedule of the scenecomp the schedule of the App.
    """
    for scene in scene_comp_list:
        for seq_type in scheduler.cached_system_sequence_types:
            # for some unknown reason, this is faster than calling the schedule.add_systems method.
            if scene.schedule.system_schedule[seq_type]:
                scene.schedule.system_schedule[seq_type].extend(scheduler.system_schedule[seq_type])
            else:
                scene.schedule.system_schedule.update(
                    {
                        seq_type :  scheduler.system_schedule[seq_type]
                    }
                )
            # print(seq_type, scene.schedule.system_schedule[seq_type])
            scene.schedule.system_schedule[seq_type].sort(
                key=lambda syst: syst.priority, reverse=True
            )
            
        scene.schedule._add_cached_system_sequence(*scheduler.cached_system_sequence_types)


def _scenes_init(scenes: dict[str,SceneComp], parameters: dict[type, _Any]) -> None:
    """
    Instantiates the systems on their parameters. It analyzes the parameters and injects what they asked for.
    """

    try:
        all_systems: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in sequence_types}
        for key, scene in scenes.items():
            for seq_type, system_list in scene.schedule.system_schedule.items():
                all_systems[seq_type] += system_list

        # self.system_schedule.items()
        for key, systems in all_systems.items():
            for system in systems:
                syst_param_signature = signature(system.parameters)
                params = syst_param_signature.parameters

                # Determine which parameters to inject based on type annotations
                injection_args = []

                for param in params.values():
                    annotation = param.annotation
                    injection_args.append(parameters[annotation])

                system.parameters(*injection_args)

    except KeyError as key:
        print(f"""KeyError occured, 
                  - <{key}> was wrongly typed in the parameters of the systems
                  - key: <{key}> was either not initialized in app or 
                  - <{key}> was not properly put in the parameter of the app""")