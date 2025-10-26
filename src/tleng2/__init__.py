from os import environ

#, path, getcwd
# import json

# core_engine Directory
#from .core_engine.scene_manager import SceneManager

# core_engine Directory
# from .core_engine.scene_manager import SceneManager
from .engine.settings import GlobalSettings
from .engine.properties import EngineProperties, SceneManagerProperties, RendererProperties
from .engine.methods import EngineMethods, SceneManagerMethods, RendererMethods
from .engine.app import App
# from .engine.ui_manager

# utils Directory
from .utils import colors
from .utils.utils import convert_rad_to_deg, convert_deg_to_rad, get_parent_dir
from .utils.debug import debug_print
from .utils.subpixel import SubPixelSurface


# object Directory
from .object.area import Area
from .object.sprite import Sprite

# systems Directory
from . import systems

# components Directory
from .components import events

from .components.scene import Scene, SceneCatcher
from .components.camera import Camera
from .components.renderable import Renderable, RenderableComp, DisplayCanvasComp
from .components.map import Map

# ui_elements Directory
from .uix.label import Label
from .uix.button import Button
# from .ui_manager import 


# physics Directory
# from .physics.object import Object
# from .physics.projectile import Projectile, Particles


# services Directory
from .services.animation import LazyAnimationService
from .services.image import ImageService
from .services.sound import SoundService
from .services.font import FontService
from .services.tilemap import TileMap, TileSet
from .services.sprite_stack import SpriteStackService


# the whole ecs module
from . import ecs


def hide_pygame_support_prompt() -> None:
    """
    Hides the pygame support prompt. 

    Cleaner Terminal :)
    """
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


def tleng_base_plugin(app: App) -> None:
    """
    The Game Engines Plugin.
    """

    # the developer should type what are the events that he will be using.

    events = ecs.Events(app.properties.get(ecs.EventsComp))

    # put here the initialized parameters, world, events.
    app.injection_parameters(
        app.world , # app already has a world, and it's the central world.
        app.properties, # app properties (they work like the resources of the world)
        app.scenes_manager, # to change scenes duh
        events
    )

    app.add_systems(
        PreUpdate=[
            ecs.EventManagerSystem(),
        ],
        Update=[
            systems.ClockTickSystem(),
            systems.EventsTranslation(),
            systems.QuitSystem()
        ],
        Renderer=[
            systems.RendererSystem()
        ],
    )


def tleng_additional_plugin(app: App) -> None:
    """
    The Game Engines Additionals Plugin.

    This plugin is dependent to the base one.

    WIP (Doesn't add anything yet.)
    """
    # app.add_systems(
    #     renderer=[
    #         # Render
    #     ] 
    # )


__all__ = [
    # core_engine Directory
    'GlobalSettings',
    'EngineProperties', 'SceneManagerProperties', 'RendererProperties',
    'EngineMethods', 'SceneManagerMethods', 'RendererMethods',
    'App',
    # utils Directory
    'colors',
    'convert_rad_to_deg', 'convert_deg_to_rad', 'get_parent_dir',
    'debug_print',
    'SubPixelSurface',
    # object Directory
    'Area',
    'Sprite',
    # systems Directory
    'systems',
    # components Directory
    'events',
    'Scene', 'SceneCatcher',
    'Camera',
    'Renderable', 'RenderableComp', 'DisplayCanvasComp',
    'Map',
    # ui_elements Directory
    'Label',
    'Button',
    # services Directory
    'LazyAnimationService', 
    'ImageService',
    'SoundService',
    'FontService',
    'TileMap', 'TileSet',
    'SpriteStackService',
    # the ecs module
    'ecs',
    # plugins & misc
    'hide_pygame_support_prompt',
    'tleng_base_plugin',
    'tleng_additional_plugin',
]


__author__ = "TheooKing/Theolaos"
__version__ = "v2.2.12a"

import platform

print(f"tleng {__version__} (Python: {platform.python_version()})")

del platform

__name__ = "tleng"
__doc__ = f'''
TLeng is a 2d python game engine.

Current version is {__version__}.

Find the wiki of the game engine here: https://github.com/tl-ecosystem/tleng/wiki
'''

__license__ = '''MIT License

Copyright (c) 2023 theolaos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''