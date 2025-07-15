from ..components.renderable import Renderable
from ..utils.utils import convert_rad_to_deg

import pygame
# from tleng2.utils.annotations import Coordinate
# from ..utils.settings import GlobalSettings


class ImageService:
    def __init__(self):
        self.current_angle = 0
        self.image = None
        self.frect = None
        self.or_surf = None  # Store the original surface
        self.rotated_surf = None
        self.rotated_frect = None
        self.center = pygame.Vector2(0, 0)
        self.renderable = Renderable()



    def load_image(self,
            img_filename: str,
            width: float,
            height: float,
            ) -> None:
        
        self.image = pygame.image.load(img_filename).convert_alpha() #setting the idle image 
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (width,height)), convert_rad_to_deg(self.current_angle)) #transforming the idle image
        self.or_surf = self.image.copy()  # Store the original surface
        self.frect = pygame.FRect(0,0,self.image.get_width(),self.image.get_height())
        self.center = pygame.Vector2(self.frect.center)
        self.renderable.update_surf(self.image)
        self.renderable.frect = self.frect

    
    def set_image(self, image: pygame.Surface) -> None:
        '''
        Set the image to be used for rendering.
        '''
        self.image = image
        self.or_surf = image.copy()
        self.frect = pygame.FRect(0, 0, self.image.get_width(), self.image.get_height())
        self.center = pygame.Vector2(self.frect.center)
        self.renderable.update_surf(self.image)
        self.renderable.frect = self.frect
    

    def render_surface(self)-> pygame.Surface:
        return self.image
    

    def update(self, params: dict = {}):
        if params != {}:
            ...
        else:
            self.renderable.update_cords_rect(self.frect)
            self.renderable.world_pos.x = self.frect.centerx
            self.renderable.world_pos.y = self.frect.centery


    def render(self) -> None:
        self.renderable.update_surf(self.render_surface())
        self.renderable.render()


    def render_angle(self, angle) -> None:
        """
        Angle is in radians.
        Rotates and renders the image centered on its own surface.
        """
        if self.current_angle != angle or self.rotated_surf is None:
            surf = pygame.transform.rotate(self.or_surf, angle).convert_alpha()
            self.rotated_frect = surf.get_frect(center=self.center)
            self.current_angle = angle
            self.rotated_surf = surf

        self.renderable.world_pos = self.center
        self.renderable.frect = self.rotated_frect
        self.renderable.update_surf(self.rotated_surf)
        self.renderable.render()


    def rotate_img_deg(self,
            rotate: float
            ) -> None:
        '''
        Rotates the image by some given angle (degrees)
        '''
        pass


    def rotate_img_rad(self,
            rotate: float
            ) -> None:
        '''
        Rotates the image by some given angle (radians)
        '''
        pass


    def flip_img(self,
            flip_x: bool = False,
            flip_y: bool = False,
            ) -> None:
        '''
        Flips an image to the according axis
        '''
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)


    def scale_img_px(self,
            width: float, 
            height: float, 
            ) -> None:
        '''
        Scale the image to the new desired res (uses pixels) 
        '''


    def scale_img_per(self,
            per: float
            ) -> None: 
        '''
        Scale the image to the new desired res (uses percentage) 
        '''


    def scale_img_dpi(self) -> None:
        '''
        TODO
        '''
        raise NotImplementedError('Function "scale img to dpi" has not been implemented')