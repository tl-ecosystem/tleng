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
        self.waiting_scene: str = ""
        self.scene_is_changed: bool = False


    def load_scenes(self, **scenes: SceneComp) -> None: 
        self.scenes.update(scenes) 

    
    def change_scene(self, new_scene_name: str) -> None:
        self.waiting_scene = new_scene_name
        self.scene_is_changed = True

    
    def changing_scene(self, world, schedule) -> None:

        new_scene_comp = self.scenes[self.waiting_scene]

        # schedule.scene_transition_exit()

        world.load_world_component(new_scene_comp.world)
        schedule.load_schedule_component(new_scene_comp.schedule)

        # schedule.scene_transition_start()
        
        self.current_scene = self.waiting_scene


    def get_scene(self, scene_name: str) -> SceneComp:
        return self.scenes[scene_name]
    

    def from_scene_get(self) -> None:
        """
        TODO: It will give you only the schedule or world from the scene!
        """
        ...


    def get_schedules(self) -> _Iterator[list[Schedule]]:
        """
        Needed to initialize the systems to the central World
        """
        for key, scene in self.scenes:
            yield scene.schedule