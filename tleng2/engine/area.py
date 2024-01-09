import pygame
from warnings import warn
from ..utils.colors import WHITE, BLACK
from ..utils.settings import GlobalSettings
from ..utils.annotations import Color


class Area(pygame.sprite.Sprite): # Move area to the entities and stuff
    '''
    Class for area, acts as an area that is dedicated to the entity or the class that inherits this, also can be used for "static" hitboxes
    (depracated)

    Class variables:
        self.rect: the rectangle class from pygame (created for the group sprite object, and as the main hitbox of the Area)
        self.core_x: the core x coordinate of the rect (it doesn't store the top left coordinate) (float)
        self.core_y: the core y coordinta of the rect (it doesn't store the top left coordinate) (float)
        self.core_width: the width of the rectangle (int)
        self.core_height: the height of the rectangle (int)
        self.image: image (i don't know what it can be used for) (created for the group sprite object) (pygame.Surface)
        self.color: the color of the rectangle (tuple)
    '''
    def __init__(self,
            x: float = 0,
            y: float = 0,
            width: float = 10.0,
            height: float = 10.0,
            color: Color = WHITE,
            polygon: list = None,
            poly_polygon: list = None,
        ) -> None:
        '''
        Initialising the Area
        
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the area (float)
        :param height: The height of the area (float)
        :param color: The color of the Area (tuple)
        :param polygon: Not implemented yet
        :param poly_polygon: Not implemented yet
        '''
        self.image = pygame.Surface([width,height])
        print(float(x), float(y), float(width) , float(height), type(x), type(y), type(width) , type(height))
        self.rect = pygame.Rect(float(x), float(y), float(width) , float(height)) # screen coordinates

        self.core_x = x # actual x coordinate
        self.core_y = y # actual y coordinate
        self.core_width = width
        self.core_height = height
        self.color = color  

        self.thickness = 0
   
   
    def render(self) -> None:
        '''
        Draws the area in the screen.
        If there the outline has been set to anything than 0, then it will be rendered
        :return: It returns nothing
        '''
        pygame.draw.rect(GlobalSettings._display, self.color, self.rect)
        if self.thickness != 0:            
            pygame.draw.rect(GlobalSettings._display, self.color, self.frame_rect, abs(self.thickness))


    def render_outline(self) -> None:
        '''
        Only renders the outline of the area, the outline needs to be set before it gets rendered.
        :return: It returns nothing
        '''
        pygame.draw.rect(GlobalSettings._display, self.color, self.frame_rect, abs(self.thickness))


    def set_outline(self, 
            thic: float = 1, 
            frame_color: Color = BLACK
        ) -> None:
        '''
        It draws the outline of the area by creating another rect object
        
        :param thic: it's the thickness of the Area's outline, if it is more than 
        :param frame_color: Specifes the color of the area's outline
        :return: it returns nothing
        '''
        self.thickness = thic
        self.frame_color = frame_color
        if thic > 0:
            self.frame_rect = pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2) #outside outline (*performnce issue)
        elif thic <= 0:
            self.frame_color = self.rect
            if thic == 0:
                warn("the thickness of the outline is zero, you can not see it") #giving a "warning" that the thickness of the outline is zero (for performance reasons we could remove it in production)


    def update_entity(
            self,
            x = None,
            y = None,
            width = None,
            height = None,
    ) -> None:
        self.core_x = x
        self.core_y = y
        self.core_width = width
        self.core_height = height

        self.rect.x = self.core_x
        self.rect.y = self.core_y
        self.rect.width = self.core_width
        self.rect.height = self.core_height 


    def update(self) -> None:
        '''
        Function for the sprite group updating
        '''
        # self.rect.x = x
        # self.rect.y = y
        # self.rect.width = width
        # self.rect.height = height

        self.rect.x = self.core_x
        self.rect.y = self.core_y
        self.rect.width = self.core_width
        self.rect.height = self.core_height