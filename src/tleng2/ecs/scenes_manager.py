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

from .schedule import Scheduler
from .ecs_scene import SceneComp

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
        """
        Stores them to the scenes dictionary of ScenesManager
        """
        self.scenes.update(scenes) 

    
    def change_scene(self, new_scene_name: str) -> None:
        self.waiting_scene = new_scene_name
        self.scene_is_changed = True

    
    def changing_scene(self, world, scheduler, startup: bool = False) -> None:
        """
        Pass the centrall world and the central scheduler
        """

        new_scene_comp = self.scenes[self.waiting_scene]

        if startup == False:
            scheduler.scene_transition_exit()

        world.load_world_component(new_scene_comp.world)
        scheduler.load_scheduler_component(new_scene_comp.scheduler)
        
        scheduler.scene_transition_enter()
        
        self.current_scene = self.waiting_scene

        self.scene_is_changed = False


    def get_scene(self, scene_name: str) -> SceneComp:
        return self.scenes[scene_name]
    

    def from_scene_get(self) -> None:
        """
        TODO: It will give you only the scheduler or world from the scene!
        """
        ...


    def get_schedules(self) -> _Iterator[list[Scheduler]]:
        """
        Needed to initialize the systems to the central World
        """
        for key, scene in self.scenes:
            yield scene.scheduler