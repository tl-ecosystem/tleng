"""
Stores a dictionary of "name_of_scene" and 
"""

from ..ecs.schedule import Schedule
from ..components.scene import SceneComp
from ..utils.debug import debug_print

from typing import Any as _Any
from typing import Iterator as _Iterator


class ScenesManager:
    """
    The ECS manager of tleng2
    """
    def __init__(self) -> None:
        self.scenes: dict[str, SceneComp] = {}
        self.current_scene: str = ""
        self.changing_scene: bool = False


    def load_scene(self, **scenes: SceneComp) -> None: 
        self.scenes.update(scenes) 

    
    def change_scene(self, new_scene_name: str) -> None:
        self.current_scene = new_scene_name
        self.changing_scene = True


    def get_scene(self, scene_name: str) -> SceneComp:
        return self.scenes[scene_name]
    

    def get_schedules(self) -> _Iterator[list[Schedule]]:
        for key, scene in self.scenes:
            yield scene.schedule
    

    def run_current_scene(self) -> None:
        # runs the schedule of the scene
        self.scenes[self.current_scene].run_schedule()