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
    'StateTransition', 'SceneTransition'
    'First', 
    'PreUpdate', 
    'Update', 
    'PostUpdate', 
    'Last',
    'PreRenderer', 'Renderer',
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


update_order: list[str] = ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']
startup_order: list[str] = ['PreStartUp', 'Startup']

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
# Best of both worlds: Use both :)


def _ScheduleComp_default_factory() -> dict[SEQUENCE_TYPES, list[System]]:
    return {key: [] for key in sequence_types}


@dataclass
class ScheduleComp:
    system_schedule: dict[SEQUENCE_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    cached_system_schedule: dict[SEQUENCE_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    cached_system_sequence_types: set[SEQUENCE_TYPES] = field(default_factory=set)
    current_order: str = field(default_factory=str)


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        # self.world = None
        # current running scheduling for systems
        self.system_schedule: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in sequence_types}
        self.cached_system_sequence_types: list[SEQUENCE_TYPES] = []


        #TODO: can be used as the cached active systems, better if the lists change to sets.
        self.cached_system_schedule: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in sequence_types}
        self.current_order: SEQUENCE_TYPES = 'Update'
        # self.cached_queue: list = []

    
    def _add_cached_system_sequence(self, *new_sequence_type: SEQUENCE_TYPES) -> None:
        """
        Appends the new_sequence_type to the cached_system_sequence_types,
        and then it sorts it out.
        """
        self.cached_system_sequence_types.extend(new_sequence_type)

        # print(new_sequence_type)
        # print(self.cached_system_sequence_types)
        # print(type(self.cached_system_sequence_types))

        self.cached_system_sequence_types = sorted(
            self.cached_system_sequence_types, 
            key=lambda x: update_order.index(x)
        )


    def add_systems(self, sequence_type: SEQUENCE_TYPES, *systems) -> None:
        """
        Add systems in the scheduler.

        :Returns: Nothing
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
        # for state in self.cached_state_sequence:
        #     for system in state:
        #         
        for key in self.cached_system_sequence_types:
            for system in self.system_schedule.setdefault(key,[]):
                if system.enabled:
                    system.update() # by design (not a bug, it's a feature!)

    
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
            self.cached_system_schedule, 
            self.cached_system_sequence_types,
            self.current_order 
        )


    def load_schedule_component(self, schedule_component: ScheduleComp | _Any) -> None:
        """
        Used from the scenes_manager to change scenes
        
        :schedule_component: It can be a `ScheduleComp` of even a plain `Schedule`  
        :returns: Nothing
        """
        self.system_schedule = schedule_component.system_schedule
        self.cached_system_schedule = schedule_component.cached_system_schedule
        self.cached_system_sequence_types = schedule_component.cached_system_sequence_types
        self.current_order = schedule_component.current_order


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
            
        scene.schedule.cached_system_schedule.update(scheduler.cached_system_schedule)
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