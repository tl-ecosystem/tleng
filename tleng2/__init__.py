from os import environ#, path, getcwd
# import json
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# core_engine Directory
#from .core_engine.scene_manager import SceneManager


# core_engine Directory
# from .core_engine.scene_manager import SceneManager
from .engine.settings import GlobalSettings, LocalSettings
from .engine.properties import EngineProperties, SceneManagerProperties, RendererProperties
from .engine.methods import EngineMethods, SceneManagerMethods, RendererMethods
from .engine.game import Game
# from .engine.ui_manager

from . import ecs

# utils Directory
from .utils import colors
from .utils.utils import convert_rad_to_deg, convert_deg_to_rad, get_parent_dir
from .utils.debug import debug_print
from .utils.subpixel import SubPixelSurface


# object Directory
from .object.area import Area
from .object.sprite import Sprite


# object Directory
from .components.scene import Scene, SceneCatcher
from .components.camera import Camera
from .components.renderable import Renderable
from .components.map import Map

# ui_elements Directory
from .uix.label import Label
from .uix.button import Button
# from .ui_manager import 


# physics Directory
from .physics.object import Object
from .physics.projectile import Projectile, Particles


# services Directory
from .services.animation import LazyAnimationService
from .services.image import ImageService
from .services.sound import SoundService
from .services.font import FontService
from .services.tilemap import TileMap, TileSet
from .services.sprite_stack import SpriteStackService

__all__ = [
'colors', 'convert_rad_to_deg', 'convert_deg_to_rad', 'get_parent_dir',
'EngineMethods', 'SceneManagerMethods', 'SceneManagerProperties', 'RendererMethods', 'RendererProperties', 'EngineProperties',
'Renderable',
'Map',
'Area', 
'Sprite', 
'Scene', 
'Camera', 
'Scene', 'SceneCatcher',
"Game",
'Label', 'Button',
'Object', 
'Projectile', 'Particles', 
'LazyAnimationService', 
'SoundService',
'ImageService', 
'FontService', 'SpriteStackService',
'TileMap', 'TileSet', 
'GlobalSettings', 'LocalSettings',
'debug_print',
'SubPixelSurface',
'ecs'
]


__author__ = "TheooKing/Theolaos"
__version__ = "v2.2.0.dev12"

import platform

print(f"tleng {__version__} (Python: {platform.python_version()})")

__name__ = "tleng"
__doc__ = f'''
TLeng is a 2d python game engine.

Current version is {__version__}.
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

# Engine Report:
# TODO: Settings Json support.
# TODO: Animation Json Support.
# TODO: Redo the Label system in update 2.2 and add:
#       capitilize / lower
#       striketrough, underlined
#       left|Center|Right
#       find
#       join
#       change_{smt}
#       __len__, __str__