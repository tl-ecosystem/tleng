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

        self.tile_size = 0  # Default tile size, can be changed if needed

        # basically the center of the sprite stack (of the first image)
        self.world_pos = Vector2(0,0)

        self.first_layer_frect = None

        self.cached_angles: dict[list[pygame.Surface, pygame.Surface]] = {}
        self.caching = caching
      

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

        self.tile_size = self.images[0].get_width()

        if self.caching:
            self.cache() 
        # self.renderable.update
    

    def load_from_spritesheet(self, path: str, frame_width: int, total_frames: int) -> None:
        """
        Loads images from a vertical spritesheet (read from bottom to top).
        Each frame is assumed to be the full width of the image and frame_height tall.
        """
        frame_height = frame_width
        
        sheet = pygame.image.load(path).convert_alpha()

        self.images: list[pygame.Surface] = []

        sheet_height = sheet.get_height()
        print(sheet_height, frame_height, frame_width, total_frames)
        for y in range(0,sheet_height,frame_height):
            frame = sheet.subsurface((0, y, frame_width, frame_height))
            self.images.append(frame)
            print(frame)

        self.frect = self.images[0].get_frect()
        self.tile_size = frame_width
        if self.caching:
            self.cache() 


    def scale_images(self, scalar: float) -> None:
        ...


    def cache(self, step = 2) -> None:
        """
        step is an angle step in degrees.
        Caches the images for each angle in a dictionary.
        """
        
        for angle in range(0, 360, step):
            # The first layer determines the center
            base_img = self.images[0]
            rotated_base = pygame.transform.rotate(base_img, angle)

            surf = pygame.Surface(rotated_base.get_size(), pygame.SRCALPHA)
            surf.blit(rotated_base, (0, 0))

            # Build the full sprite stack surface
            sprite_surf = pygame.Surface(
                (surf.get_width(), surf.get_height() + len(self.images) * self.spread),
                pygame.SRCALPHA
            )
            sprite_surf.fill(COLOR_KEY)
            sprite_surf.set_colorkey(COLOR_KEY)
            for i, img in enumerate(self.images):
                rotated_img = pygame.transform.rotate(img, angle)
                if self.fill:
                    for j in range(self.spread):
                        sprite_surf.blit(rotated_img, (0, rotated_img.get_height() // 2 - i * self.spread - j))
                sprite_surf.blit(rotated_img, (0, len(self.images * self.spread) - i * self.spread))

            self.cached_angles[angle] = [sprite_surf, surf]


    def get_cached_angle(self, angle: float) -> _Optional[list[pygame.Surface]]:
        """
        angle is degrees
        Returns the cached list of rotated images for the closest cached angle.
        """
        angle = round(angle) % 360
        closest_angle = min(self.cached_angles.keys(), key=lambda a: abs(a - angle))
        print(angle, closest_angle)
        return self.cached_angles.get(closest_angle, None)


    def sprite_stacking(self,) -> None:
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
        # print(self.surf_frect, 'surface_rect')


    def render(self, angle: _Optional[float] = None, bysort: bool = False) -> None:
        """
        angle in radians
        """
        if angle is not None:
            self.rotation = convert_rad_to_deg(angle)

        if not self.caching:
            # The first layer determines the center
            base_img = self.images[0]
            rotated_base = pygame.transform.rotate(base_img, self.rotation)

            surf = pygame.Surface(rotated_base.get_size(), pygame.SRCALPHA)
            surf.blit(rotated_base, (0, 0))
            self.first_layer_frect = surf.get_frect()
            self.first_layer_frect.center = tuple(self.world_pos)  # <--- This line ensures the center is always world_pos

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
        else:
            sprite_surf, surf = self.get_cached_angle(self.rotation)
            self.first_layer_frect = surf.get_frect()
            self.first_layer_frect.center = tuple(self.world_pos)  # <--- This line ensures the center is always world_pos
           
            if sprite_surf is None:
                print(f"Warning: No cached surface for angle {self.rotation} degrees")
                return

        self.renderable.ysort = bysort

        self.renderable.frect = self.first_layer_frect

        self.renderable.update_surf(sprite_surf)
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
        
        self.frect.center = self.world_pos
        self.renderable.world_pos = self.world_pos  # Update the renderable's world position



    def update_new(self, **params) -> None:
        """
        Takes x, y parameters (world coordinates)
        """
        if params:
            if params.get('x') or params.get('y'):
                self.world_pos.x = params['x']
                self.world_pos.y = params['y']

