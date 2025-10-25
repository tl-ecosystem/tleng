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

import pygame

from ..ecs import *
from ..components.engine import FpsComp
from ..components.events import QuitGameEvent, RightMouseClick, LeftMouseClick

from ..engine.methods import EngineMethods
from ..engine.settings import GlobalSettings
from ..engine.properties import EngineProperties 
# from ..engine.settings import GlobalSettings


class ClockTickSystem(System):
    def parameters(self, world: World):
        self.world = world


    def update(self):
        fps = GlobalSettings._fps
        if FpsComp in self.world.resources:
            fps = self.world.resources[FpsComp].fps
        
        EngineMethods.clock_tick_EP_dt(fps)


class EventsTranslation(System):
    # one event loop to rule them all!!1!1!1
    def parameters(self, events: Events) -> None:
        self.events = events
    

    def update(self) -> None:
        for event in EngineProperties._events:
            if event.type == pygame.QUIT:
                self.events.send(QuitGameEvent)
            if event.type == pygame.BUTTON_LEFT:
                self.events.send(LeftMouseClick(*pygame.mouse.get_pos()))
            if event.type == pygame.BUTTON_RIGHT:
                self.events.send(RightMouseClick(*pygame.mouse.get_pos()))


class QuitSystem(System):
    def parameters(self, events: Events):
        self.events = events


    def update(self):
        if self.events.read(QuitGameEvent):
            EngineProperties.GAME_RUNNING = False