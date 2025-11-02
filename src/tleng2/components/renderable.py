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


def frect() -> pygame.FRect:
    return pygame.FRect(0,0,0,0)


@dataclass
class RenderableComp:
    surface: pygame.Surface = None
    rect: pygame.FRect = field(default_factory=frect)
    layer: int = 0
    ysort: bool = False


@dataclass
class RenderablesComp:
    renderable: list[RenderableComp] = field(default_factory=list)
    layer: int = 0
    ysort: bool = False


@dataclass
class DisplayCanvasComp:
    size: tuple[int, int]
    surface: pygame.Surface = field(init=False)

    def __post_init__(self):
        self.surface = pygame.Surface(self.size)


class Renderable:
    def __init__(self,) -> None:
        self.world_pos = Vector2(0,0)
        self.surface = None # pygame.Surface()
        self.render_method = None
        self.centered = False
        self.frect = None # pygame.FRect()

        self.ysort = False
        
        # only changed by the renderer
        self._screen_pos = Vector2(0,0)


    def __repr__(self):
        return f'x: {self.world_pos}, y: {self.world_pos}, surface: {self.surface}'
    

    @staticmethod
    def rect(frect: pygame.FRect, color: Color, thickness: int, radius: int) -> pygame.Surface:
        """
        To get only the frect, use this method but with the thickness set at 0.
        """   
        surface = None
        if thickness > 0:
            surface = pygame.Surface((frect.w + (thickness<<1), frect.w + (thickness<<1)))
            frect = pygame.FRect(frect.x - thickness, frect.y - thickness, frect.width + thickness*2 , frect.height + thickness*2)
        else:
            surface = pygame.Surface(frect.size)

        temp_rect = frect.copy()
        temp_rect.center = surface.get_frect().center

        pygame.draw.rect(surface, color, temp_rect, abs(thickness), radius)
        return surface
    

    @staticmethod
    def sprite_stack(images, rotation, spread) -> pygame.Surface: ...


    def update_cords(self, 
            x: float,
            y: float
        )-> None: 
        self.world_pos.x = x
        self.world_pos.y = y


    def update_cords_rect(self, 
            frect: pygame.FRect
        )-> None: 
        """
        Update the coordinates with a rectangle
        """
        self.world_pos.x = frect.center[0]
        self.world_pos.y = frect.center[1]


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
        