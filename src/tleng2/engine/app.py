import sys
import pygame
import warnings


from .settings import GlobalSettings
from .scene_manager import SceneManager

from .properties import EngineProperties, GlobalProperties, SceneManagerProperties, RendererProperties
from .methods import  EngineMethods, RendererMethods, SceneManagerMethods
from .renderer import Renderer

from ..components.scene import SceneCatcher, SceneComp

from ..ecs.worlds_manager import World
from ..ecs.scenes_manager import ScenesManager
from ..ecs.schedule import Schedule,  _scenes_init, _merge_to_scene_schedulers, SEQUENCE_TYPES
from ..ecs.events import EventsComp
from ..ecs.system import System

from ..utils.debug import Debugging, debug_print

from typing import Callable as _Callable
from typing import Any as _Any
from typing import TypeVar

T = TypeVar('T')

class App: 
    def __init__(self) -> None:
        # for backwards compatability
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        
        # The new and improved ECS
        self.scenes_manager = ScenesManager()
        self.world = World()
        self.scheduler = Schedule()
        self.properties = GlobalProperties()
        self.plugin_scheduler = Schedule()


        # injection parameters for the scheduler.init() method
        self.inj_parameters = {}
        


    def get_property(self, property_type: T) -> T:
        """
        It will search if the World has this resources
        """
        return self.properties.properties[property_type]


    def add_properties(self, *properties: _Any) -> None:
        """
        Appends resources to the world.
        
        - Example:
        {
            ComponentType: Compoenent, ...
        }
        """
        self.properties.add_properties( 
            *properties
        )


    def load_scenes(self, start_with: str, **scenes: SceneComp) -> None:
        """
        Loads scenes to Ecs Manager
        """
        self.scenes_manager.load_scenes(**scenes)

        self.scenes_manager.waiting_scene = start_with

    
    def register_events(self, *events_types: type) -> None:
        """
        Registers the Events Properties of the App (Tleng Plugin also registers some default events)
        """
        self.properties.add_properties(
            EventsComp(events_types) 
        )


    def use_plugins(self, *plugins: _Callable[[_Any],None]) -> None:
        '''
        Registers Plugins in the main App. 

        Plugins can setup crucial `systems`, `resources`, `events`, or even implement `queries`, `worlds` and more. The default plugin is the 
        `tleng_base_plugin` there is also the `tleng_additionals_plugin` (not implemented)

        **plugins**: Plugins must be `Any` callable that takes as a first and only parameter the `App` it self. \n
        **return**: Returns nothing
        '''
        for plugin in plugins:
            plugin(self)


    def add_systems(self, **systems: list[System]) -> None:
        """
        Syntax for add systems
        """
        for seq_type, l_systems in systems.items():
            print(seq_type, type(seq_type), l_systems)
            self.plugin_scheduler.add_systems(
                seq_type,
                *l_systems,
            )


    def injection_parameters(self, *parameters) -> None:
        self.inj_parameters.update(
            {
                type(key): key for key in parameters
            }
        )


    def run(self, tleng2_intro: bool = False) -> None:
        """
        ECS support for running ECS applications, that have worlds, schedules, scenecomps and more
        """
        if tleng2_intro:
            warnings.warn(
                "A tleng2 intro has not been created yet nor implemented.",
                FutureWarning,
                stacklevel=2
            )

        self.scenes_manager.changing_scene(self.world, self.scheduler)

        _merge_to_scene_schedulers(list(self.scenes_manager.scenes.values()), self.plugin_scheduler)
        _scenes_init(self.scenes_manager.scenes, self.inj_parameters) 

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            events = pygame.event.get()
            EngineProperties._events = events

            # same as what world.run_schedule() would do
            self.scheduler.update()

            # cleans the dead entities of the active world.
            self.world.update()

            if self.scenes_manager.scene_is_changed:
                self.scenes_manager.changing_scene(self.world, self.scheduler)

            # maybe this is not a good way to do it?
            # if self.properties_db[Debugging]:
            #     EngineMethods.set_caption(f"{EngineProperties._clock.get_fps()}")

        pygame.quit()
        sys.exit()


    def _run_test(self, s=5) -> None:
        """
        ONLY FOR TESTING
        """
        #TODO this to match the above code
        import time

        self.scenes_manager.changing_scene(self.world, self.scheduler)
        
        # I don't know why this configuration is faster
        _merge_to_scene_schedulers(list(self.scenes_manager.scenes.values()), self.plugin_scheduler) #TODO static method
        _scenes_init(self.scenes_manager.scenes, self.inj_parameters)

        scheduler = self.scheduler
        world = self.world
        scenes_manager = self.scenes_manager

        t1 = time.time()
        t2 = time.time()
        while t2-t1 <= s:
            t3 = time.time()
            events = pygame.event.get()
            EngineProperties._events = events
            # push pygame events in the TlengEventManager

            # same as what world.run_schedule() would do
            scheduler.update()

            # cleans the dead entities of the active world.
            world.update()

            if scenes_manager.scene_is_changed:
                scenes_manager.changing_scene(world, scheduler)

            t2 = time.time()
            # print("fps", 1/((t2-t3)))

        pygame.quit()


    def run_old(self) -> None:
        '''
        Runs the Game Engine while loop with the game (deprecated, use run() instead)
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