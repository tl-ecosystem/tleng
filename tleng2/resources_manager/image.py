from os import path 
import pygame
from tleng2.utils.annotations import Coordinate
from tleng2.utils.settings import GlobalSettings


class ImageManager:
    def __init__(self):
        self.rotation = 0
        self.image = None
        self.image_x = 0
        self.image_y = 0


    def load_image(self,
            img_filename: str,
            width: float,
            height: float,
            ) -> None:
        
        self.image = pygame.image.load(img_filename).convert_alpha() #setting the idle image 
        self.image = pygame.transform.rotate(pygame.transform.scale(self.idle_image, (width,height)), self.rotation) #transforming the idle image
        self.image_x = self.image.get_width() 
        self.image_y = self.image.get_height()
        self.image_x = self.rect.x
        self.image_y = self.rect.y
    
    
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
            flip_x: bool,
            flip_y: bool,
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


class LazyAnimationManager:
    """
    Animation that imports image files immedietly.
    """
    def __init__(self, LocalSettings: None = None):
        self.anim_x = 0
        self.anim_y = 0
        self.anim_dict = {}
        self.current_anim = ''
        self.anim_frame_data = 0


    def load_animation(self,
            anim_dict:dict
            ) -> None:
        '''
        Load the animation.


        {"%name_anim1%" : {"anim":[str,str,...], "anim_fps" : int}, "%name_anim2%" : {"anim":[str,str,...], "frames" : int}, ...}
        '''
        self.anim_dict = anim_dict
        temp_anim_keys = anim_dict.keys()
        #looping through the whole dictianary to change them into pygame images
        for i in temp_anim_keys:
            for j in range(len(anim_dict[i])):
                self.new_image = pygame.image.load(anim_dict[i][j]).convert_alpha()
                self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width, self.rect.height)), self.rotation)
                temp_anim_dict += [self.new_image]

            self.anim_dict.update({i: temp_anim_dict}) #updating the entitys animation dict
            temp_anim_dict = [] #resseting the NEW animation list


    def flip_anim(self):
        pass


    def update(self, 
            x: float,
            y: float,
            ) -> None:
        '''
        Updating the current animation

        :param target_fps: These are the targeted fps, it is useful in case the current fps are 0, then we will use the target_fps
        :param fps: The "wanted" fps of the game (it is advised to use get_fps function as it may not work if you have capped at 1000fps but only get 60)
        :param frames: *How many frames will the animation last
        :return: it returns nothing

        For debugging animation use: 
        print(self.anim[int(self.anim_frame_data)], len(self.anim), self.anim_frame_data, frames, (self.rect.width,self.rect.height))   <----- debugging line
        '''

        # self.window.blit(self.animDict[self.currentAnim][int(self.anim_frame_data)],(self.imageX,self.imageY))
        #(e.x.: 12/60=0.2, every frame its going to be incremented by 0.2, if it is more than the lenght of the animation (4)
        #    then the next image of the animation will play and anim_frame_data will reset)
        current_fps = GlobalSettings._clock.get_fps()
        target_fps = GlobalSettings._fps
        anim_fps = self.anim_dict[self.current_anim]["anim_fps"]

        if current_fps > 0:
            self.anim_frame_data += anim_fps/current_fps
        else:
            self.anim_frame_data += anim_fps/target_fps #just in case the current_fps hit 0

        if self.anim_frame_data >= len(self.animDict[self.current_anim]):
            self.anim_frame_data = 0


    def render(self) -> None:
        self.window.blit(self.anim_dict[self.current_anim]["anim"][int(self.anim_frame_data)], (self.anim_x, self.anim_y))