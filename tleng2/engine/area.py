import pygame
from warnings import warn
from ..colors import *


class Area(pygame.sprite.Sprite):
    '''
    Class for area, acts as an area that is dedicated to the entity or the class that inherits this, also can be used for "static" hitboxes

    Class variables:
        self.rect: the rectangle class from pygame (created for the group sprite object, and as the main hitbox of the Area)
        self.core_x: the core x coordinate of the rect (it doesn't store the top left coordinate) (float)
        self.core_y: the core y coordinta of the rect (it doesn't store the top left coordinate) (float)
        self.core_width: the width of the rectangle (int)
        self.core_height: the height of the rectangle (int)
        self.window: the window that the rectangle can be drawn at (pygame.Surface)
        self.image: image (i don't know what it can be used for) (created for the group sprite object) (pygame.Surface)
        self.color: the color of the rectangle (tuple)
    '''
    def __init__(self, window:pygame.Surface, x:float = 0, y:float = 0, width:float = 10.0, height:float = 10.0,  color:tuple = WHITE):
        '''
        Initialising the Area
        
        :param window: It is the window that you want the area to be drew at (pygame Surface)
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the area (float)
        :param height: The height of the area (float)
        :param color: The color of the Area (tuple)
        '''
        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        self.rect.centerx = x # screen coordinate
        self.rect.centery = y # screen coordinate

        self.core_x = x # actual x coordinate
        self.core_y = y # actual y coordinate
        self.core_width = width
        self.core_height = height
        self.window = window
        self.color = color  
        self.outline = 0
        self.thickness = 0
   
   
    def render(self)->None:
        '''
        Draws the area in the screen
        :return: It returns nothing
        '''
        pygame.draw.rect(self.window, self.color, self.rect)
        if self.thickness != 0:            
            pygame.draw.rect(self.window, self.color, self.frame_rect, abs(self.thickness))


    def outline_Area(self, thic: float = 1, frame_color: tuple(int,int,int) = BLACK)->None:
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
    

    def update(self)->None:
        '''
        Function for the sprite group updating

        x:int, y:int, width:int, height:int
        '''
        # self.rect.x = x
        # self.rect.y = y
        # self.rect.width = width
        # self.rect.height = height

        self.rect.x = self.core_x
        self.rect.y = self.core_y
        self.rect.width = self.core_width
        self.rect.height = self.core_height