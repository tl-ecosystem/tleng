import pygame, sys
from typing import Callable as _Callable 

from .properties import EngineProperties
from ..ecs import *
from ..utils.event_manager import dispatch_event


def pygame_quit_handle(event) -> None:
    pygame.quit()
    sys.exit()


class HandleEventsSystem(System):
    """
    Handles the events by using only one loop.

    The solution avoids multiple loops that are wasted for no reason
    """
    def __init__(self, priority: int = 0) -> None:
        System.__init__(self, priority=priority)
        self.callbacks: list[tuple[int, str]] = []
    

    def append_to_event_callback(self,*events: tuple[int, str]) -> None:
        self.callbacks += [*events]
    

    def update(self) -> None:
        for event in EngineProperties._events:
            for key, callable in self.callbacks:
                if event.type == key:
                    dispatch_event(callable, event)