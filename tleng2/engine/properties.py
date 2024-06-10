# have every not setting related variable stored here

# from logging import getLogger

import pygame
from .settings import GlobalSettings
from abc import abstractmethod, ABC

class LocalProperties(ABC):
    @abstractmethod
    def __init__(self):
        """
        Put the local specific properties that you want the scene/enviroment/object to have
        e.x. (pseudo code)

        self.fps = 30
        self.font = comic_sans
        self.disp = True
        self.in-game-keyboard = False
        """    


class EngineProperties:
    """
    Engine properties, needed across the framework/game.
    """
    _clock: pygame.time.Clock = pygame.time.Clock()
    _dt: float = 0
    _events: list = []
    _keys_pressed: list = []
    GAME_RUNNING: bool = True
    # _logger = getLogger("EngineLogger")

    # _index_event = 1

    # animation_database = {} # probably not to use


class SceneManagerProperties:
    _default_scene: str = ''

    _current_scene: str = ''
    
    _waiting_scene: str = ''
    _changing_scenes: bool = False


class RendererProperties:
    __temp_disp = None

    _default_display: pygame.SurfaceType = None

    _display: pygame.SurfaceType = None
    _window: pygame.SurfaceType  = None

    _local_default_camera = None

    # parameters to be used in scenes
    scene_parameters: dict = {}
    type_parameters: dict = {}

    # when you call to render a sprite, it's renderable attr will be passed 
    # here for the renderer to later inspect it and render it
    render_calls = []