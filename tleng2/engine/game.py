import sys
import pygame

from .settings import GlobalSettings
from .scene_manager import SceneManager

from ..ecs.worlds_manager import WorldsManager, World
from ..engine.properties import EngineProperties, SceneManagerProperties, RendererProperties
from ..engine.methods import  EngineMethods, RendererMethods, SceneManagerMethods
from ..engine.renderer import Renderer
from ..components.scene import SceneCatcher
from ..utils.debug import debug_print


class Game: 
    def __init__(self):
        # pygame.init()
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        self.ecs_manager = WorldsManager()
        

    def load_worlds(self, start_with: str, **worlds: World) -> None:
        """
        Loads worlds to Ecs Manager
        """
        self.ecs_manager.load_worlds(**worlds)

        self.ecs_manager.current_world = start_with

    
    def run(self, tleng2_intro: bool = False):
        if tleng2_intro:
            pass

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            events = pygame.event.get()
            EngineProperties._events = events

            # for event in events:
            #     if event.type == pygame.QUIT:
            #         print(f"Closing game")
            #         pygame.quit()
            #         sys.exit()                    

            self.ecs_manager.run_current_world()
            # RendererMethods.update_window()
            # pygame.display.flip()


            if GlobalSettings._debug:
                EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")
        
        
        pygame.quit()
        sys.exit()



    def run_old(self, tleng2_intro: bool = False):
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


    