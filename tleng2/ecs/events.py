import pygame
import sys
from dataclasses import dataclass

from ..engine.properties import EngineProperties
from . import *
from ..utils.event_manager import dispatch_event

from weakref import ref as _ref
from weakref import WeakMethod as _WeakMethod
from types import MethodType as _MethodType
from typing import Callable as _Callable
from typing import Any as _Any
from typing import Callable as _Callable 


@dataclass
class EventComp:
    


def pygame_quit_handler(event) -> None:
    EngineProperties.GAME_RUNNING = False


class EventComp:
    def __init__(self, *event: tuple[int, str]) -> None:
        self.events = list(event)
        

class HandleEventsSystem(System):
    """
    Handle pygame events by using only one loop.

    The solution avoids multiple loops that are wasted for no reason
    """
    def __init__(self, priority: int = 0) -> None:
        System.__init__(self, priority=priority)
        self.event_registry = {}
    

    def update(self) -> None:
        # print(component[0][1].events)
        if EventComp in self.world.unique_components:
            for event in EngineProperties._events:
                for key, callable in self.world.unique_components[EventComp].events:
                    if event.type == key:
                        self.dispatch_event(callable, event)


    def dispatch_event(self, name: str, *args: _Any) -> None:
        """Dispatch an event by name, with optional arguments.
        Any handlers set with the :py:func:`esper.set_handler` function
        will recieve the event. If no handlers have been set, this
        function call will pass silently.
        :note:: If optional arguments are provided, but set handlers
                do not account for them, it will likely result in a
                TypeError or other undefined crash.
        """
        for func in self.event_registry.get(name, []):
            func()(*args)


    def _make_callback(self, name: str) -> _Callable[[_Any], None]:
        """Create an internal callback to remove dead handlers."""
        def callback(weak_method: _Any) -> None:
            self.event_registry[name].remove(weak_method)
            if not self.event_registry[name]:
                del self.event_registry[name]
        return callback


    def set_handler(self, name: str, func: _Callable[..., None]) -> None:
        """Register a function to handle the named event type.
        After registering a function (or method), it will receive all
        events that are dispatched by the specified name.
        .. note:: A weak reference is kept to the passed function,
        """
        if name not in self.event_registry:
            self.event_registry[name] = set()
        if isinstance(func, _MethodType):
            self.event_registry[name].add(_WeakMethod(func, self._make_callback(name)))
        else:
            self.event_registry[name].add(_ref(func, self._make_callback(name)))


    def remove_handler(self, name: str, func: _Callable[..., None]) -> None:
        """Unregister a handler from receiving events of this name.
        If the passed function/method is not registered to
        receive the named event, or if the named event does
        not exist, this function call will pass silently.
        """
        if func not in self.event_registry.get(name, []):
            return
        self.event_registry[name].remove(func)
        if not self.event_registry[name]:
            del self.event_registry[name]