import pygame

from ..ecs import *
from ..components.renderable import DisplayCanvasComp, FillScreenComp, RenderableComp
from ..engine.properties import EngineProperties, RendererProperties
from ..engine.methods import RendererMethods
from ..engine.settings import GlobalSettings
from ..utils.debug import debug_print


class RendererSystem(System):
    """
    Experimental Renderer
    """
    def __init__(self, priority: int = 0) -> None:
        System.__init__(self, priority)
        self._display = None
        self._displays
        self._window = None


    def change_world(self, world) -> None:
        super().change_world(world)

        self._displays = self.world.single_fast_query(
            DisplayCanvasComp
        )

        self._display = self._displays[0][1]


    def update(self) -> None:
        components = self.world.single_fast_query(
            FillScreenComp
        )

        self._display.surface.fill(color=components[0][1].color)

        # Basically render_calls but on steroids
        components = self.world.single_fast_query(
            RenderableComp
        )

        for event in EngineProperties._events:
            if event.type == pygame.VIDEORESIZE:
                GlobalSettings._win_res = RendererProperties._window.get_rect().size
                
                self._display.surface = pygame.transform.scale(self._display.surface, GlobalSettings._win_res)
            

        RendererProperties._window.blit(self._display.surface, (0,0))
        pygame.display.update()
        