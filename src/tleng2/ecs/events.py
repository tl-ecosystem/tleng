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

from .system import System
from .world import World

from ..engine.properties import GlobalProperties
from ..engine.properties import EngineProperties

from ..components.events import *

from types import MethodType as _MethodType

from typing import Any as _Any
from typing import Callable as _Callable
from typing import Iterable as _Iterable
from typing import TypeVar

from weakref import WeakMethod as _WeakMethod
from weakref import ref as _ref

# def pygame_quit_handler(event) -> None:
#     EngineProperties.GAME_RUNNING = False


T = TypeVar('T')


def load_event_list_to_dict(keys_list: _Iterable) -> dict[_Any, list]:
    """
    Creates a dictionary from a list. (it is faster than using dict.fromkeys(...,...))
    """
    return {key: [] for key in keys_list}


class EventsComp:
        """
        When creating a world, you need to provide all the events you will be using in your current world.

        .. note:: Memory intensive. 
        """
        def __init__(self,
            event_types: _Iterable,
        ) -> None:
            # Producing an event with a short lifetime.
            self.event_types: dict[type, _Any] = {key: [] for key in event_types} 
            self.prev_events: dict[type, _Any] = {}
            self.curr_events: dict[type, _Any] = {}

            # for dispatching events.
            self.event_registry: dict[type, _Any] = {}
            
            # consumption_events: dict = {}


class EventManagerSystem(System):
    def parameters(self, world: World, properties: GlobalProperties):
        self.world = world
        self.properties = properties
    
    def update(self):
        properties = self.properties.properties

        if EventsComp in properties:
            events = properties[EventsComp]

            # moving the new events to the old events to be "deleted" in the next call of this system 
            events.prev_events = {}
            events.prev_events.update(events.curr_events)
            events.curr_events = {}
            events.curr_events.update(events.event_types)


class Events:
    """
    ECS System
    """
    def __init__(self, events_comp: EventsComp) -> None:
        self.events_comp = events_comp
    

    def send(self, event) -> None:
        try:
            self.events_comp.curr_events[type(event)] += [event]
        except KeyError:
            raise KeyError (f'Event Type {type(event)} is not found in the Properties EventsComp')
    

    def read(self, event_type: T) -> list[T]:
        try:
            return self.events_comp.prev_events[event_type]
        except KeyError:
            return self.events_comp.prev_events.get(event_type, [])

        
    
    def read_consume(self, event_type) -> _Any:
        """
        Instead of just reading the event, it also consumes it. Meaning that if there is no other sender after consumption
        any other system that tries to read this event_type will not find anything. WIP
        """
        ...


    def produce(self, event) -> None:
        """
        Produces consumable events. Infinite lifespan WIP
        """        
        ...


    def consume(self, event_type) -> None:
        """
        Consumes consumable events. WIP
        """
        ...


    def dispatch_event(self, event_type: type, *args: _Any) -> None:
        """Dispatch an event by event_type, with optional arguments.

        Any handlers set with the `self.set_handler` function
        will recieve the event. If no handlers have been set, this
        function call will pass silently.

        :note:: If optional arguments are provided, but set handlers
            do not account for them, it will likely result in a
                TypeError or other undefined crash.
        """
        for func in self.components_comp.event_registry.get(event_type, []):
            func()(*args)


    def _make_callback(self, event_type: type) -> _Callable[[_Any], None]:
        """Create an internal callback to remove dead handlers."""

        def callback(weak_method: _Any) -> None:
            event_registry = self.components_comp.event_registry

            event_registry[event_type].remove(weak_method)
            if not event_registry[event_type]:
                del event_registry[event_type]

        return callback


    def set_handler(self, event_type: type, func: _Callable[..., None]) -> None:
        """Register a function to handle the event_typed event type.

        After registering a function (or method), it will receive all
        events that are dispatched by the specified event_type.

        .. note:: A weak reference is kept to the passed function,
        """
        event_registry = self.components_comp.event_registry
        
        if event_type not in event_registry:
            event_registry[event_type] = set()

        if isinstance(func, _MethodType):
            event_registry[event_type].add(_WeakMethod(func, self._make_callback(event_type)))
        else:
            event_registry[event_type].add(_ref(func, self._make_callback(event_type)))


    def remove_handler(self, event_type: type, func: _Callable[..., None]) -> None:
        """Unregister a handler from receiving events of this event_type.

        If the passed function/method is not registered to
        receive the event_typed event, or if the event_typed event does
        not exist, this function call will pass silently.
        """
        event_registry = self.components_comp.event_registry

        if func not in event_registry.get(event_type, []):
            return

        event_registry[event_type].remove(func)
        if not event_registry[event_type]:
            del event_registry[event_type]