import sys
import pygame

from .settings import GlobalSettings
from .scene_manager import SceneManager, ScenesManager

from .properties import EngineProperties, SceneManagerProperties, RendererProperties
from .methods import  EngineMethods, RendererMethods, SceneManagerMethods
from .renderer import Renderer
from ..components.scene import SceneCatcher, SceneComp
from ..utils.debug import debug_print

from ..ecs.worlds_manager import WorldsManager, World

from typing import Callable as _Callable
from typing import Any as _Any


class App: 
    def __init__(self):
        # pygame.init()
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        
        self.ecs_manager = WorldsManager()
        self.scenes_manager = ScenesManager()

        self.world = World()


    def load_worlds(self, start_with: str, **worlds: World) -> None:
        """
        Loads worlds to Ecs Manager
        """
        self.ecs_manager.load_worlds(**worlds)

        self.ecs_manager.current_world = start_with

        # global components and scheduler databases
        self.components_db = {}
        self.scheduler_db = {} 

    
    def load_scenes(self, start_with: str, **scenes: SceneComp) -> None:
        """
        Loads worlds to scene manager
        """
        self.scenes_manager.load_worlds(**scenes)

        self.scenes_manager.current_world = start_with

    
    def use_plugins(self, *plugins: _Callable) -> None:
        for plugin in plugins:
            plugin(self)

        
    def add_systems(self, **systems: _Any) -> None:
        self.scheduler_db.update(systems)

    
    def run(self, tleng2_intro: bool = False):
        if tleng2_intro:
            raise NotImplementedError("A tleng2 intro has not been created yet.")

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            events = pygame.event.get()
            EngineProperties._events = events                 

            self.ecs_manager.run_current_world()

            if GlobalSettings._debug:
                EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")
        
        
        pygame.quit()
        sys.exit()



    def run_old(self, tleng2_intro: bool = False):
        '''
        Runs the Game Engine while loop with the game
        '''
        
        if tleng2_intro:
            raise NotImplementedError("A tleng2 intro has not been created yet.")

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            # handle the scene from here
            events = pygame.event.get()
            EngineProperties._events = events
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene_manager.run_current_scene()
            self.renderer.render()
            RendererMethods.update_window()
            pygame.display.flip()
            RendererMethods.clear_render_calls()

        
            EngineMethods.clock_tick_EP_dt(GlobalSettings._fps)
            SceneManagerMethods.update_scene()
            
            if GlobalSettings._debug:
                EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")


            # self.ecs_manager.update()

            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()


    