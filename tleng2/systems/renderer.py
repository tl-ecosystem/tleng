from dataclasses import dataclass
from time import time
import pygame


from ..ecs import *
from ..components.renderable import DisplayCanvasComp, RenderableComp
from ..components.events import ResizeWindowEvent
from ..engine.properties import EngineProperties, RendererProperties
from ..engine.methods import RendererMethods
from ..engine.settings import GlobalSettings
from ..utils.debug import debug_print


class RendererSystem(System):
    """
    Experimental ECS Renderer
    """
    def __init__(self, priority: int = 0) -> None:
        System.__init__(self, priority)
        self._display = None
        self._displays = None
        self._window = None


    def change_world(self, world) -> None:
        super().change_world(world)


        if DisplayCanvasComp in self.world.unique_components:
            self._display = self.world.unique_components[DisplayCanvasComp]

    
    def resize_window(self) -> None:
        GlobalSettings._win_res = RendererProperties._window.get_rect().size
        
        self._display.surface = pygame.transform.scale(self._display.surface, GlobalSettings._win_res)       
    

    def update(self) -> None:
        events = self.world.events.read(ResizeWindowEvent)
        if events:        
            self.resize_window()

        self._display.surface.fill(RendererProperties.fill_screen_color)

        # Basically render_calls but on steroids
        components = self.world.single_fast_query(
            RenderableComp
        )

        blit_seq = [(rc.surface, rc.rect.topleft) for e, rc in components]

        self._display.surface.fblits(blit_seq)


        RendererProperties._window.blit(self._display.surface, (0,0))
        pygame.display.flip()
        