from .area import Area
from ..services.animation import LazyAnimationService
from ..services.sound import SoundService
from ..utils.settings import GlobalSettings
from ..utils.colors import RED
# import pygame

class EntityCatcher:
    entity_in_scene = {}

    def __init__(self, scene_key):
        self.entity_in_scene.update({scene_key:[self]})


class Entity:
    def __init__(
            self,
            x: int | float, 
            y: int | float,  
            width: int | float, 
            height: int | float, 
            entity_type: str, 
        ) -> None:

        self.core_x = x
        self.core_y = y
        self.core_width = width
        self.core_height = height
        self.hitbox = Area(x=x, y=y, width=width, height=height)
        #self.set_outline(1,RED)
        self.anim_service = LazyAnimationService()
        # self.sound_service = SoundService('')
        self.entity_type = entity_type

    def load_animation(self, 
            anim_dict: dict
        )-> None:
        self.anim_manager.import_animation(anim_dict=anim_dict)


    def new_hitbox(self, hitbox_width : float, hitbox_height : float) -> None: # TODO : hitbox/coordination system
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, which is a Rect)
        :param hitbox_width: The new number of the new hitbox width (either a flot or an int)
        :param hitbox_height: The new number of the new hitbox height (either a flot or an int)
        :return: it returns nothing
        '''
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitbox_width, hitbox_height
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2


    def update(self) -> None:
        '''
        It updates everything without the need of the programmer to type out every function of the entity.
        '''
        self.anim_manager.update()
        self.hitbox.update()
    

    def render(self) -> None:
        if GlobalSettings._debug:
            self.entity_hitbox.render_outline()

        self.anim_manager.render()
