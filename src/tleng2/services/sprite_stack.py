import os
import pygame
from pygame.math import Vector2

from typing import Optional as _Optional

from ..components.renderable import Renderable
from ..engine.properties import RendererProperties
from ..utils.colors import COLOR_KEY, RED
from ..utils.utils import convert_rad_to_deg

class LazySpriteStackService:
    """
    Embraces caching
    """
    ...


class SpriteStackService:
    """
    Simple SpriteStacking method

    Should load the pictures into a self.images list
    And pass them into a Renderable Object 
    """
    def __init__(self, caching: bool = False) -> None:
        """
        Rotation are calculated with radians.
        """
        self.renderable = Renderable()
        self.renderable.rendering_method(self.sprite_stacking, self)
        self.images = None
        self.rotation = 0 # degrees TODO change this to radians

        self.fill = False
        self.spread = 1
        self.frect = None

        # basically the center of the sprite stack (of the first image)
        self.world_pos = Vector2(0,0)

        self.first_layer_frect = None

        self.caching = caching
        if caching:
            self.cache()        


    def cache(self) -> None: ...


    def load_images(self, directory: str, sprite_set: bool = False) -> None:
        """
        Images in sprite stacking must be consistent, even if in a sprite-set.
        Use os.path.join() for directory parameter.
        """
        list_dir = os.listdir(directory)
        list_dir.sort()
        images = [pygame.image.load(os.path.join(directory, img)) for img in list_dir]
        # print(images[0].get_width(), images[0].get_height())
        temp_images = []
        for i in images:
            temp_images += [i.convert_alpha()]

        self.images: list[pygame.Surface] = temp_images 
        self.frect = self.images[0].get_frect()
        # self.renderable.update
    

    def scale_images(self, scalar: float) -> None:
        ...


    def sprite_stacking(self, display) -> None:
        surf = pygame.Surface(pygame.transform.rotate(self.images[0], self.rotation).get_size())
        self.frect = surf.get_frect() 
        self.frect.center = self.world_pos
        sprite_surf = pygame.Surface((surf.get_width(),
                                          surf.get_height() + len(self.images)*self.spread))
        sprite_surf.fill(COLOR_KEY)
        sprite_surf.set_colorkey(COLOR_KEY)
        for i, img in enumerate(self.images):
            rotated_img = pygame.transform.rotate(img, self.rotation)
            if self.fill:
                for j in range(self.spread):
                    sprite_surf.blit(rotated_img, (0,rotated_img.get_height() // 2 -i*self.spread -j))
            sprite_surf.blit(rotated_img, (0,len(self.images*self.spread) - i*self.spread))
        
        self.renderable.update_surf(sprite_surf)
        self.surf_frect = sprite_surf.get_frect()
        self.surf_frect.bottomleft = self.frect.bottomleft
        #pygame.draw.rect(RendererProperties._display,RED,pygame.FRect(self.renderable.x+20,self.renderable.y,sprite_surf.get_width(),sprite_surf.get_height()),3)
        print(self.surf_frect, 'surface_rect')


    def render(self, angle: _Optional[float] = None, bysort: bool = False) -> None:
        """
        angle in radians
        """
        if angle is not None:
            self.rotation = convert_rad_to_deg(angle)

        # The first layer determines the center
        base_img = self.images[0]
        rotated_base = pygame.transform.rotate(base_img, self.rotation)
        surf = pygame.Surface(rotated_base.get_size(), pygame.SRCALPHA)
        surf.blit(rotated_base, (0, 0))
        self.rect = surf.get_frect()
        self.rect.center = self.world_pos  # <--- This line ensures the center is always world_pos

        # Build the full sprite stack surface
        sprite_surf = pygame.Surface(
            (surf.get_width(), surf.get_height() + len(self.images) * self.spread),
            pygame.SRCALPHA
        )
        sprite_surf.fill(COLOR_KEY)
        sprite_surf.set_colorkey(COLOR_KEY)
        for i, img in enumerate(self.images):
            rotated_img = pygame.transform.rotate(img, self.rotation)
            if self.fill:
                for j in range(self.spread):
                    sprite_surf.blit(rotated_img, (0, rotated_img.get_height() // 2 - i * self.spread - j))
            sprite_surf.blit(rotated_img, (0, len(self.images * self.spread) - i * self.spread))

        self.renderable.frect = surf.get_frect()
        self.renderable.frect.center = self.world_pos  # <--- Also set the renderable's frect center
        self.renderable.update_surf(sprite_surf)
        self.renderable.ysort = bysort
        self.renderable.world_pos = self.world_pos  # Only pass world position!
        self.renderable.render()

        
    def update(self, params: dict = {}) -> None:
        """
        Takes x, y parameters (world coordinates)
        """
        if params:
            if params.get('x') or params.get('y'):
                self.world_pos.x = params['x']
                self.world_pos.y = params['y']


    def update_new(self, **params) -> None:
        """
        Takes x, y parameters (world coordinates)
        """
        if params:
            if params.get('x') or params.get('y'):
                self.world_pos.x = params['x']
                self.world_pos.y = params['y']
