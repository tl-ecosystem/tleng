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


# Every variable that is not related as a setting is here


import pygame

from .settings import GlobalSettings

from abc import abstractmethod, ABC

from typing import TypeVar
from typing import Any as _Any

class LocalProperties(ABC):
    @abstractmethod
    def __init__(self):
        """
        Put the local specific properties that you want the scene/enviroment/object to have
        e.x. (pseudo code)

        self.fps = 30
        self.font = comic_sans
        self.disp = True
        self.in-game-keyboard = False
        """    


T = TypeVar('T')

# New and improved Properties for tleng2.ecs
class GlobalProperties:
    """
    A way to handle and access properties from systems in `tleng2.ecs`
    """
    def __init__(self) -> None:
        self.properties: dict = {}

    
    def __contains__(self, item: _Any) -> bool:
        return item in self.properties


    def add_properties(self, *new_properties) -> None:
        self.properties.update(
            {
                type(key) : key for key in new_properties
            }
        )
    

    def get(self, property_type: T) -> T:
        """
        Gets you the property from type.
        It throws errors if not correct.
        """
        return self.properties[property_type]


    def exists(self, property_type: T) -> bool:
        return property_type in self.properties

    #TODO: some dunder that support the `some_comp IN global_properties`

class EngineProperties:
    """
    Engine properties, needed across the framework/game.
    """
    _clock: pygame.time.Clock = pygame.time.Clock()
    _dt: float = 0
    _events: list = []
    _keys_pressed: list = []
    GAME_RUNNING: bool = False
    # _logger = getLogger("EngineLogger")

    # _index_event = 1

    # animation_database = {} # probably not to use


class SceneManagerProperties:
    _default_scene: str = ''

    _current_scene: str = ''
    
    _waiting_scene: str = ''
    _changing_scenes: bool = False


class RendererProperties:
    """Exposing pygame functionality"""
    __temp_disp = None

    _default_display: pygame.SurfaceType = None

    _display: pygame.SurfaceType = None
    _window: pygame.SurfaceType  = None

    _local_default_camera = None

    # parameters to be used in scenes
    scene_parameters: dict = {}
    type_parameters: dict = {}

    fill_screen_color: tuple[int, int, int, int] = (0, 0, 0, 255)

    # when you call to render a sprite, it's renderable attr will be passed 
    # here for the renderer to later inspect it and render it
    render_calls = []