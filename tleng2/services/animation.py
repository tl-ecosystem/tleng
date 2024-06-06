import pygame

from ..engine.settings import GlobalSettings
from ..engine.properties import EngineProperties, RendererProperties
from ..components.renderable import Renderable


class FancyAnimationService:
    """
    It uses bones instead of multiple images.
    """
    ...


class LazyAnimationService:
    """
    Animation that imports image files immedietly.
    """
    def __init__(self):
        """
        An implementation of Local Settings has not been done yet.
        """
        self.rect = pygame.FRect(0,0,10,10)
        self.rotation = 0
        self.anim_db = {}
        self.current_anim = ''
        self.current_image_anim = ''
        self.anim_frame_data = 0

        # self.image = ...
        # self.center = ...
        self.renderable = Renderable() # deprecate


    def load_animation(self,
                        anim_db: dict,
                        alpha_conversion = True 
                      ) -> None:
        '''
        Load the animation. The animation must have consistent widths and heights!

        {"%name_anim1%" : {"anim":[str,str,...], "anim_fps" : int}, "%name_anim2%" : {"anim":[str,str,...], "anim_fps" : int}, ...}
        '''
        
        temp_anim_db = []
        new_image = None
        #looping through the whole dictianary to change them into pygame images
        for key in anim_db:
            for i in range(len(anim_db[key]["anim"])):
                new_image = pygame.image.load(anim_db[key]["anim"][i]).convert_alpha()
                new_image = pygame.transform.rotate(pygame.transform.scale(new_image, (self.rect.width, self.rect.height)), self.rotation)
                temp_anim_db += [new_image]

            self.anim_db.update({key: {"anim" : temp_anim_db, "anim_fps" : anim_db[key]["anim_fps"], "len": len(temp_anim_db)}}) #updating the entitys animation dict
            temp_anim_db = [] #resseting the NEW animation list
    

    def import_animation(self,
            anim_db:dict
            ) -> None:
        """
        {"%name_anim1%" : {"anim":[str,str,...], "anim_fps" : int},  ...}
        """
        self.anim_db.update(anim_db)


    def scale_animation(self,
            new_width: float,
            new_height: float
        ) -> None:

        self.rect.height = new_height
        self.rect.width = new_width


    def set_colorkey_animation(self, colorkey: tuple[int], *anim_keys: str) -> None:
        """
        Make applies color_key to the whole animation

        :anim_key: if you want to apply it to certain animations only 
        """

        for key in anim_keys if anim_keys != () else self.anim_db:
            for surface in self.anim_db[key]["anim"]:
                surface.set_colorkey(colorkey)


    def flip_animation(self,
                flip_x: bool = False,
                flip_y: bool = False,
                *anim_keys: str
            ) -> None: # TODO: fix this

        for key in anim_keys:

            self.anim_db[key]["anim"] = [
                pygame.transform.flip(frame, flip_x, flip_y) for frame in self.anim_db[key]["anim"]
            ]


    def change_current_animation(self, anim_key) -> None: 
        self.current_anim = anim_key


    def animate(self) -> None:
        '''
        Updating the current animation

        For debugging animation use: 
        print(self.anim[int(self.anim_frame_data)], len(self.anim), self.anim_frame_data, frames, (self.rect.width,self.rect.height))   <----- debugging line
        '''

        # self.window.blit(self.animDict[self.currentAnim][int(self.anim_frame_data)],(self.imageX,self.imageY))
        #(e.x.: 12/60=0.2, every frame its going to be incremented by 0.2, if it is more than the lenght of the animation (4)
        #    then the next image of the animation will play and anim_frame_data will reset)
        current_fps = EngineProperties._clock.get_fps()
        target_fps = GlobalSettings._fps
        anim_db_length = len(self.anim_db[self.current_anim]["anim"])
        
        anim_fps = self.anim_db[self.current_anim]["anim_fps"]
        if current_fps > 0:
            self.anim_frame_data += anim_fps/current_fps
        else:
            self.anim_frame_data += anim_fps/target_fps #just in case the current_fps hit 0

        if self.anim_frame_data >= anim_db_length:
            self.anim_frame_data = 0


    def update(self, params: dict = {}) -> None:
        """
        Updates the animation, and the coordinates.
        """
        
        if params:
            self.rect.center = (params["x"],params["y"])
        
        self.animate()
        self.renderable.update_cords(self.rect.x, self.rect.y)


    def render(self) -> None:
        """
        Makes a call for the renderer to render.
        """
        self.renderable.update_surf(self.anim_db[self.current_anim]["anim"][int(self.anim_frame_data)])

        self.renderable.render()
