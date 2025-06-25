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

# Tilemap used for a map

import pygame

from ..services.tilemap import TileMap
from ..engine.properties import RendererProperties
from ..components.renderable import Renderable


class Map(TileMap):
    '''
    Requires Tiles that have objects in render.
    '''
    def __init__(self) -> None:
        self.renderable = Renderable()
        self.current_angle = 0


    def pre_render(self) -> None:
        # Renderer.render_tiles()

        surf = pygame.Surface((self.tileset.width*len(self.tiles[0]), self.tileset.height*len(self.tiles)))

        for y, y_tiles in enumerate(self.tiles):
            for x, tile_name in enumerate(y_tiles):
                # print(tile_name,self.tileset.set[tile_name])
                
                surf.blit(self.tileset.set[tile_name],(x*self.tileset.width, y*self.tileset.height))
                # self.renderable.update(x*self.tileset.width, y*self.tileset.height, self.tileset.set[tile_name])
                # self.renderable.render()

        # caching
        self.or_surf = surf
        self.renderable.update_surf(surf)
        self.center = surf.get_rect().center


    def render(self) -> None:
        # RendererProperties._display.blit
        self.renderable.render()


    def update_center(self, new_center) -> None:
        """
        Update the center of the map surface.
        new_center: tuple or pygame.Vector2
        """
        self.center = pygame.Vector2(new_center)

    def render_angle(self, angle) -> None:
        """
        Angle must NOT be in radians.
        Rotates and renders the map centered on its own surface.
        """
        if self.current_angle != angle:
            surf = pygame.transform.rotate(self.or_surf, angle)
            self.rotated_surf = surf
            self.rotated_rect = surf.get_rect()
            self.current_angle = angle
        else:
            surf = getattr(self, 'rotated_surf', self.or_surf)
            self.rotated_rect = surf.get_rect()

        centered_rect = surf.get_rect(center=self.center)
        self.renderable.update_cords_rect(centered_rect)
        self.renderable.update_surf(surf)
        self.renderable.render()


    def add_to_space(self, space):
        """
        Adds the physics side of the tiles to space (pymunk)
        """
        for y, y_tiles in enumerate(self.tiles):
            for x, tile_name in enumerate(y_tiles):
                # print(tile_name,self.tileset.set[tile_name])
                space.add() 