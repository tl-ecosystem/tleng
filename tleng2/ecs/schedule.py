from dataclasses import dataclass, field

from .system import System
from ..components.scene import SceneComp

from typing import Literal as _Literal

scheduler_types = [
    'StateTransition', 
    'PreStartupStateTransition',
    'First', 
    'PreUpdate', 
    'RunFixedMainLoop', 
    'Update', 
    'PostUpdate', 
    'Last',
    'PreStartup', 
    'Startup', 
    'PostStartup'
]

SCHEDULER_TYPES = _Literal[
    'StateTransition', 
    'PreStartupStateTransition',
    'First', 
    'PreUpdate', 
    'RunFixedMainLoop', 
    'Update', 
    'PostUpdate', 
    'Last',
    'PreStartup', 
    'Startup', 
    'PostStartup'
]

# TODO: POSSIBLE OPTIMIZATION OF THE DICTIONARY COMPREHENSION
def _ScheduleComp_default_factory() -> dict[SCHEDULER_TYPES, list[System]]:
    return {key: [] for key in scheduler_types}

@dataclass
class ScheduleComp:
    system_schedule: dict[SCHEDULER_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)
    current_system_schedule: dict[SCHEDULER_TYPES, list[System]] = field(default_factory=_ScheduleComp_default_factory)


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        self.system_schedule: dict[SCHEDULER_TYPES, list[System]] = {key: [] for key in scheduler_types}
        
        # can be used as the cached active systems.
        self.current_system_schedule: dict[SCHEDULER_TYPES, list[System]] = {key: [] for key in scheduler_types}
    

    def add_systems(self, scheduler_type: SCHEDULER_TYPES, *systems) -> None: 
        self.system_schedule[scheduler_type] += systems
        self.system_schedule[scheduler_type].sort(key=lambda syst: syst.priority, reverse=True)

    
    def load_systems_from_scenes(self, scenes: list[SceneComp]) -> None:
        for scene in scenes:
            self.system_schedule.update(scene.schedule.system_schedule)

    
    def init_systems(self, world) -> None:
        for system in self.system_schedule:
            system.change_world(world)


    def update(self) -> None:
        for system in self.system_schedule:
            system.update()

    
    def disable_system(self,) -> None:
        ...


    def enable_system(self,) -> None:
        ...


# class SchedulerManager?