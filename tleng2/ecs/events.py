from dataclasses import dataclass

from .system import System

# from ..engine.properties import EngineProperties

from typing import Any as _Any


# def pygame_quit_handler(event) -> None:
#     EngineProperties.GAME_RUNNING = False

def load_event_list_to_dict(keys_list: list) -> dict:
    """
    Creates a dictionary from a list. (it is faster than using dict.fromkeys(...,...))
    """
    return {key: [] for key in keys_list}


class EventsComp:
        """
        When creating a world, you need to provide all the events you will be using in your current world.
        Warning: Memory intensive. 
        """
        def __init__(self,
            event_types: list,
        ) -> None:
        
            self.event_types = {key: [] for key in event_types} 
            self.prev_events = {}
            self.curr_events = {}
            
            # consumption_events: dict = {}


class EventManagerSystem(System):
    def update(self):
        wuc = self.world.unique_components
        if EventsComp in wuc:
            events = wuc[EventsComp]

            # moving the new events to the old events to be "deleted" in the next call of this system 
            events.prev_events = {}
            events.prev_events.update(events.curr_events)
            events.curr_events = {}
            events.curr_events.update(events.event_types)


class Events:
    def __init__(self, world) -> None:
        self.world = world
    

    def send(self, event) -> None:
        wuc = self.world.unique_components
        if EventsComp in wuc:
            events = wuc[EventsComp]
            try:
                events.curr_events[type(event)] += [event]
            except:
                raise KeyError (f'Event Type {type(event)} is not found in the Unique Component EventsComp')
    

    def read(self, event_type) -> _Any:
        wuc = self.world.unique_components
        if EventsComp in wuc:
            events = wuc[EventsComp]

            return events.prev_events.get(event_type, []) + events.curr_events.get(event_type, [])
        
    
    # def read_consume(self, event_type) -> _Any:
    #     """
    #     Instead of just reading the event, it also consumes it. Meaning that if there is no other sender after consumption
    #     any other systme that tries to read this event_type will not find anything.
    #     """
    #     ...


    # def produce(self,) -> None:
    #     """
    #     Produces consumable events. Infinite lifespan
    #     """        
    #     ...


    # def consume(self,) -> None:
    #     """
    #     Consumes consumable events. 
    #     """
    #     ...
