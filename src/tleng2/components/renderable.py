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
from dataclasses import dataclass, field


from ..engine.properties import RendererProperties
from ..utils.annotations import Color


@dataclass
class RenderableComp:
    surface: pygame.Surface = None
    rect: pygame.FRect = None
    layer: int = 0


@dataclass
class DisplayCanvasComp:
    size: tuple[int, int]
    surface: pygame.Surface = field(init=False)

    def __post_init__(self):
        self.surface = pygame.Surface(self.size)


class Renderable:
    def __init__(self,) -> None:
        self.x = 0
        self.y = 0
        self.world_pos = Vector2(0,0)
        self.surface = None # pygame.Surface()
        self.render_method = None
        self.centered = False


    def __repr__(self):
        return f'x: {self.x}, y: {self.y}, surface: {self.surface}'
    

    @staticmethod
    def rect(rect: pygame.FRect, color: Color, thickness: int, radius: int) -> pygame.Surface:
        """
        To get only the rect, use this method but with the thickness set at 0.
        """   
        surface = None
        if thickness > 0:
            surface = pygame.Surface((rect.w + (thickness<<1), rect.w + (thickness<<1)))
            rect = pygame.Rect(rect.x - thickness, rect.y - thickness, rect.width + thickness*2 , rect.height + thickness*2)
        else:
            surface = pygame.Surface(rect.size)

        temp_rect = rect.copy()
        temp_rect.center = surface.get_frect().center

        pygame.draw.rect(surface, color, temp_rect, abs(thickness), radius)
        return surface
    

    @staticmethod
    def sprite_stack(images, rotation, spread) -> pygame.Surface: ...


    def update_cords(self, 
            x: float,
            y: float
        )-> None: 
        self.x = x
        self.y = y
        self.world_pos.x = x
        self.world_pos.y = y


    def update_cords_rect(self, 
            rect: pygame.FRect
        )-> None: 
        """
        Update the coordinates with a rectangle
        """
        self.x = rect.x
        self.y = rect.y
        self.world_pos.x = rect.x
        self.world_pos.y = rect.y


    def update_surf(self, 
            new_surface: pygame.Surface
        ) -> None: 
        self.surface = new_surface


    def update(self,
            x: float,
            y: float,
            new_surface: pygame.Surface
        ) -> None: 
        self.update_cords(x,y)
        self.update_surf(new_surface)
    

    def render(self,) -> None:
        RendererProperties.render_calls += [self]


    def rendering_method(self, render_method, game_object):
        """
        Gets invoked if the the game object is in the camera area. Used if it has a complex system for rendering 
        e.x. SpriteStacking

        :param render_method: must be a class method, or a function
        """
        self.render_method = render_method
        self.self_class = game_object
        