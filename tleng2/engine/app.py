import sys
import pygame
import warnings

from .settings import GlobalSettings
from .scene_manager import SceneManager

from .properties import EngineProperties, SceneManagerProperties, RendererProperties
from .methods import  EngineMethods, RendererMethods, SceneManagerMethods
from .renderer import Renderer

from ..components.scene import SceneCatcher, SceneComp

from ..ecs.worlds_manager import WorldsManager, World
from ..ecs.scenes_manager import ScenesManager
from ..ecs.schedule import Schedule
from ..ecs.events import Events

from ..utils.debug import Debugging, debug_print

from typing import Callable as _Callable
from typing import Any as _Any


class App: 
    def __init__(self) -> None:
        # pygame.init()
        # for running old projects still in tleng v2.2.11.dev
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        
        # The new and improved ECS scene manager
        self.scenes_manager = ScenesManager()

        self.scheduler_db = Schedule()
        self.properties_db = {}

        self.world = World()
        # self.events = Events()


    def get_property(self, property_type: type) -> _Any:
        """
        It will search if the World has this resources
        """
        raise NotImplementedError()


    def append_properties(self, *properties: _Any) -> None:
        """
        Appends resources to the world.
        
        - Example:
        {
            ComponentType: Compoenent, ...
        }
        """
        self.properties_db.update( {type(_property): _property for _property in properties})


    def load_worlds(self, start_with: str, **worlds: World) -> None:
        """
        Loads worlds to Ecs Manager
        """
        self.ecs_manager.load_worlds(**worlds)

        self.ecs_manager.current_world = start_with


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


    def run(self, tleng2_intro: bool = False) -> None:
        if tleng2_intro:
            raise NotImplementedError("A tleng2 intro has not been created yet.")
        # if scheduler_res_dynamic_load is not True:
        self.scheduler_db.load_systems_from_scenes(self.scenes_manager.scenes)


        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            events = pygame.event.get()
            EngineProperties._events = events
            # push pygame events in the TlengEventManager


            # same as what world.run_schedule() would do
            self.scheduler_db.update()

            self.world.update()

            if self.properties_db[Debugging]:
                EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")

        pygame.quit()
        sys.exit()


    def run_old(self) -> None:
        '''
        Runs the Game Engine while loop with the game
        '''
        warnings.warn(
            "run_old() is deprecated and will be removed in a future release."
            "Please use run() instead.",
            FutureWarning,
            stacklevel=2
        )

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


            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()