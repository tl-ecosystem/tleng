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
startup_order: list[str] = ['PreStartUp', 'Startup', 'PostStartup']
scene_transition_order: list[str] = ['OnSceneExit']
state_transition_order: list[str] = ['OnStateExit']


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
        
        #TODO: can be used as the cached active systems, better if the lists change to sets.
        self.cached_system_schedule: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in sequence_types}
        self.cached_system_sequence_types: set[SEQUENCE_TYPES] = set()


        #TODO not sure about this
        self.current_order: SEQUENCE_TYPES = 'Update'

        # self.cached_queue: list = []


    def add_systems(self, sequence_type: SEQUENCE_TYPES, *systems) -> None:
        """
        Add systems in the scheduler.

        :Returns: Nothing
        """
        self.system_schedule[sequence_type] += systems
        self.cached_system_sequence_types.add(sequence_type)
        self.system_schedule[sequence_type].sort(key=lambda syst: syst.priority, reverse=True)

    
    #TODO: unneeded wasteful code! Garbaj logic!
    def load_systems_from_scenes(self, scenes: dict[str, SceneComp]) -> None:
        for key, scene in scenes.items():
            self.system_schedule.update(scene.schedule.system_schedule)


    def init(self, parameters: dict[type, _Any]) -> None:
        """
        Inits the systems on their parameters. It analyzes the parameters and injects what they asked for.
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
            
    # what if this becomes a staticmethod
    def _scenes_init(self, scenes: dict[str,SceneComp], parameters: dict[type, _Any]) -> None:
        """
        Inits the systems on their parameters. It analyzes the parameters and injects what they asked for.
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
            
    
    # TODO refine the caching system
    def update(self) -> None:
        """
        According to what the resources say the right systems will run.
        
        slight optimization: a cached queue. So it doesnt try to iterate over empty lists.
        """      
        for key in self.cached_system_sequence_types:
            for system in self.system_schedule.setdefault(key,[]):
                if system.enabled:
                    system.update()
            
        # when a scene transitions it calls the function that changes the entities, components, scheduler (systems)
        #   from the scene it wants to change to to the central world. The previous scene gets saved before the transition.
        # There a 

    
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
    # for scene in scene_comp_list:
        # scene.
    ...