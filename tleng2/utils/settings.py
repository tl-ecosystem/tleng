# for creating class functions that require a constant global setting variable from this page
import pygame, json


class GlobalSettings:
    _width = 1280
    _height = 720
    _scaling = 1
    _window = None # the window that you see
    _display = None # the inner display of the window

    _clock = pygame.time.Clock()
    _fps = 60

    # indexEvent = 1

    # animation_database = {} # probably not to use

    @staticmethod
    def load_display( bg_color: tuple[int,int,int] = (200,200,255) ) -> None:
        """
        Initialize the display.
        """
        GlobalSettings._display = pygame.Surface((GlobalSettings._width, GlobalSettings._height)) 
        GlobalSettings._window = pygame.display.set_mode((GlobalSettings._width, GlobalSettings._height))
        GlobalSettings._display.fill(bg_color)


    @staticmethod
    def load_settings():
        """
        Pass the saved settings
        """
        pass
