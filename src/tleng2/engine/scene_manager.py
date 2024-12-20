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

"""
Scene Manager
It justs puts the stuff on the screen and it handles the <scene changes> like menu->game->pause screen etc.
Idea:
SceneHandler will get layers, that the dev can assign multiple scenes to play.
Scene will just handle the updates of the objects that it draws. After they were updated and drawn to the buffer screen then they will be flipped and start again onto the next frame.
Scene should also change the scene state when neceasery.

SceneHandler should recognise the state of the app for the right scene to play.

Pseudo code:

class menu_scene ...
class game_scene ...

scene_dict = menu : menu_scene, game : game_scene  ...
game_state = menu

gameloop
    scene_phase(game_state)
    clock.tick(fps)
    buffer.flip()

fn scene_phase:
    sceneloop
        events()
        update()
        render()
"""

import pygame

from .settings import GlobalSettings
from .properties import EngineProperties, SceneManagerProperties

from ..components.scene import Scene, SceneCatcher
from ..utils.debug import debug_print

from typing import Any as _Any

class SceneManager:
    """
    Manages the animation service, scenes how they are getting rendered. Game Engine Backend function.
    """

    def __init__(self, ) -> None: 
        """
        :param scenes: The dictionary should have Scene classes, or classes that have the structure of a scene class.
        :return: None
        """
        self.scenes = None
        self.scene_layers = [] # future support for having a scene render on top of another scene, 
        # self.current_scene

        # self.current_scene = ''

    def return_scene_phase(self, key:str) -> Scene:
        """
        Returns the entire scene class.
        :param key: Must be a string
        :return: Scene Class
        """
        return self.scenes[key]
    

    def load_scenes(self, scenes: dict[str,Scene]) -> None:
        self.scenes = scenes
    

    @staticmethod
    def rendering_scene(scene):
        pygame.event.pump()
        keys_pressed = pygame.key.get_pressed()
        scene.event_handling(keys_pressed)
        scene.update()
        scene.render()
        EngineProperties.update_window()
        EngineProperties.clock_tick_GP_dt(GlobalSettings._fps)
        pygame.display.flip()


    @staticmethod
    def run_current_scene() -> None:
        """
        Runs the current scene that is assigned.
        """
        # for scene in SceneCatcher.scenes[self.current_scene]:
        scene = SceneCatcher.scenes[SceneManagerProperties._current_scene]
        keys_pressed = pygame.key.get_pressed()
        scene.event_handling(keys_pressed)
        scene.update()
        scene.render()

        debug_print("Successfull scene render from SceneManager from SceneCatcher", tags=["Rendering"])
