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

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..ecs.world import WorldComp
from ..ecs.schedule import Scheduler
from ..engine.properties import RendererProperties


@dataclass
class SceneComp:
    """
    namespace conflict with ecs_scene, thus cSceneComp
    """
    world: WorldComp
    schedule: Scheduler


class SceneCatcher:
    scenes = {}

    def __init__(self, 
            scene_key:str, 
            sr_param_key: str
        ) -> None:
        self.scenes.update({scene_key: self})
        RendererProperties.scene_parameters.update({scene_key:sr_param_key})


class Scene(SceneCatcher, ABC):
    def __init__(self,
            scene_name, 
            sr_param_key: str = 'default'
        )-> None:

        SceneCatcher.__init__(self,
                              scene_key=scene_name, 
                              sr_param_key=sr_param_key),
        self.scene_name = scene_name


    @abstractmethod
    def event_handling(self) -> None:
        '''
        To handle the events of mouse and other.
        If you want to access Keys Pressed, you can do so, from 
        
        `EngineProperties._events`
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''

    @abstractmethod
    def update(self) -> None:
        '''
        game logic
        '''

    @abstractmethod
    def render(self) -> None:
        '''
        what to render to the screen
        '''
