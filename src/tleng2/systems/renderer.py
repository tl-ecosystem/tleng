# Copyright (c) 2023 Theolaos

# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to 
# whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the 
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from dataclasses import dataclass
from time import time
import pygame


from ..ecs import *
from ..components.renderable import DisplayCanvasComp, RenderableComp
from ..components.events import ResizeWindowEvent
from ..engine.properties import EngineProperties, GlobalProperties, RendererProperties
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

    
    def resize_window(self) -> None:
        GlobalSettings._win_res = RendererProperties._window.get_rect().size
        
        self._display.surface = pygame.transform.scale(self._display.surface, GlobalSettings._win_res)
    

    def parameters(self, world: World, events: Events, properties: GlobalProperties):
        self.world = world
        self.events = events
        self.properties = properties

        if DisplayCanvasComp in self.world.resources:
            self._display = self.world.get_resource(DisplayCanvasComp)


    def update(self) -> None:
        # TODO renderer parameters such as scaling, camera et cetera
        events = self.events.read(ResizeWindowEvent)
        if events:        
            self.resize_window()


        self._display.surface.fill(RendererProperties.fill_screen_color)
        # RendererProperties._window.fill(RendererProperties.fill_screen_color)

        # Basically render_calls but on steroids
        components = self.world.single_fast_query(
            RenderableComp
        )

        blit_seq = [(rc.surface, rc.rect.topleft) for e, rc in components]

        self._display.surface.fblits(blit_seq)
        # RendererProperties._window.fblits(blit_seq)
        # for e, rc in blit_seq:
        #     self._display.surface.blit(e,rc)


        RendererProperties._window.blit( pygame.transform.scale(self._display.surface, GlobalSettings._win_res), (0,0))
        pygame.display.flip()
        