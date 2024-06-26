import sys
import pygame

from ..ecs.worlds_manager import WorldsManager
from ..engine.properties import EngineProperties, SceneManagerProperties, RendererProperties
from ..engine.methods import  EngineMethods, RendererMethods, SceneManagerMethods
from ..engine.renderer import Renderer
from ..components.scene import SceneCatcher
from ..utils.debug import debug_print
from .settings import GlobalSettings
from .scene_manager import SceneManager


class Game: 
    def __init__(self):
        # pygame.init()
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        self.ecs_manager = WorldsManager()
        

    def load_worlds(self, ) -> None:
        """
        
        """
        self.ecs_manager = ...


    def run(self, tleng2_intro: bool = False):
        '''
        Runs the Game Engine while loop with the game
        '''
        
        # it is not ready yet
        if tleng2_intro:
            pass

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            # handle the scene from here
            events = pygame.event.get()
            EngineProperties._events = events
            
            for event in events:
                if event.type == pygame.QUIT: # escape to exit, personal preference
                    pygame.quit()
                    sys.exit()

            self.scene_manager.render_current_scene()
            self.renderer.render()
            RendererMethods.update_window()
            pygame.display.flip()

            RendererMethods.clear_render_calls()
            EngineMethods.clock_tick_GP_dt(GlobalSettings._fps)
            SceneManagerMethods.update_scene()
            
            if GlobalSettings._debug:
                EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")


            # self.ecs_manager.update()

            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()


    