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

import pygame
from pygame import Vector2

from .settings import GlobalSettings
from .properties import RendererProperties, SceneManagerProperties
from ..components.camera import CameraCatcher
from ..utils.debug import debug_print
from ..utils.subpixel import SubPixelSurface

def pymunk_to_pygame(pos, surface_height):
    """
    Convert pymunk (world) coordinates to pygame (screen) coordinates.
    pos: tuple or Vec2d (x, y) in pymunk world coordinates
    surface_height: height of the pygame surface (window)
    Returns: tuple (x, y) in pygame screen coordinates
    """
    x, y = pos
    return (x, surface_height - y)

class Renderer:
    """
    Experimental Renderer
    """
    def __init__(self) -> None:
        self._display = None
        self._window = None


    def render(self) -> None:
        # debug_print(RendererProperties.render_calls,tags=['Renderer', 'Render_calls'])
        display = RendererProperties._display
        
        temp_vec = Vector2(0,0)

        default_camera = CameraCatcher.cameras.get(RendererProperties._local_default_camera, None)

        transform = default_camera.get_transform() if default_camera != None else None

        for renderable in RendererProperties.render_calls:
            
            debug_print(renderable, tags=["Renderer"])

            if default_camera != None:
                temp_vec.x = 0
                temp_vec.y = 0
                #step 1: Find the offset vector from the center of the camera to the renderable's world position
                #step 2: Rotate the offset vector by the camera's angle
                offset = renderable.world_pos - default_camera.get_position()
                screen_pos = transform(Vector2(renderable.world_pos), renderable.centered)
                debug_print(screen_pos, tags=["Renderer"])

                surface = renderable.surface

                rect = surface.get_rect(center=(pymunk_to_pygame(
                                 (round(screen_pos.x), round(screen_pos.y)), 
                                 RendererProperties._display.get_height()
                             )))
                display.blit(surface, rect)
            else:
                display.blit(renderable.surface, (renderable.x , renderable.y))
        
        debug_print(CameraCatcher.cameras, tags=["Renderer", "Camera"])