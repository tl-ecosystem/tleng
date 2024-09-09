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

scheduler_types: list[str] = [
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
scene_transition_order: list[str] = ['OnExit']
state_transition_order: list[str] = ['OnExit']

# TODO: POSSIBLE OPTIMIZATION OF THE DICTIONARY COMPREHENSION
def _ScheduleComp_default_factory() -> dict[SEQUENCE_TYPES, list[System]]:
    return {key: [] for key in scheduler_types}

@dataclass
class ScheduleComp:
    system_schedule: dict[SEQUENCE_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    cached_system_schedule: dict[SEQUENCE_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    queue: list[str] = field(default_factory=list)


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        self.world = None
        self.system_schedule: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in scheduler_types}
        
        # can be used as the cached active systems.
        self.cached_system_schedule: dict[SEQUENCE_TYPES, list[System]] = {key: [] for key in scheduler_types}

        self.current_order: SEQUENCE_TYPES = 'Update'


    def add_systems(self, scheduler_type: SEQUENCE_TYPES, *systems) -> None: 
        self.system_schedule[scheduler_type] += systems
        self.system_schedule[scheduler_type].sort(key=lambda syst: syst.priority, reverse=True)

    
    def load_systems_from_scenes(self, scenes: list[SceneComp]) -> None:
        for scene in scenes:
            self.system_schedule.update(scene.schedule.system_schedule)


    def init(self, parameters: dict[type, _Any]) -> None:
        """
        Inits the schedule on what world to use, and inits the systems on what world for them to use.
        """
        try:
            for system in self.system_schedule:
                syst_param_signature = signature(system.parameters)
                params = syst_param_signature.parameters

                # Determine which parameters to inject based on type annotations
                injection_args = []

                for param in params.values():
                    annotation = param.annotation

                    injection_args.append(parameters[annotation])

                system.parameters(*annotation)

        except KeyError as key:
            print(f"""KeyError occured, 
                      - <{key}> was wrongly typed in the parameters of the systems
                      - key: <{key}> was either not initialized in app or 
                      - <{key}> was not properly put in the parameter of the app""")
            

    def update(self) -> None:
        """
        According to what the resources say the right systems will run.
        """
        for key in self.queue:
            for system in self.system_schedule[key]:
                if system.abled:
                    system.update()

    
    def update_queue(self, queue) -> None: 
        """
        Adds to the end of the key queue the 
        """
        ...

    
    def disable_system(self,) -> None:
        ...


    def enable_system(self,) -> None:
        ...

    
    def return_schedule_component(self) -> ScheduleComp: 
        ...

    
    def load_schedule_component(self, schedule_component) -> None:
        ...


# class SchedulerManager?