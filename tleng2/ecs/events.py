from dataclasses import dataclass

from ..engine.properties import EngineProperties


def pygame_quit_handler(event) -> None:
    EngineProperties.GAME_RUNNING = False
        

class EventInstance:
    def __init__(self, event_id, event):
        self.event_id = event_id
        self.event = event


class Events:
    def __init__(self):
        self.prev_events = []
        self.curr_events = []
        self.event_count = 0

    def send(self, event):
        event_id = self.event_count
        event_instance = EventInstance(event_id, event)
        self.curr_events.append(event_instance)
        self.event_count += 1
        return event_id
    

class EventIterator:
    def __init__(self, iter_with_id):
        self.iter_with_id = iter_with_id

    def __iter__(self):
        return self

    def __next__(self):
        event_instance = next(self.iter_with_id.chain)
        return event_instance.event

    def size_hint(self):
        return self.iter_with_id.unread

    def count(self):
        return sum(1 for _ in self)

    def last(self):
        # last_event_instance = None
        # for event_instance in self.iter_with_id.chain:
        # iter_id_chain = self.iter_with_id.chain
        last_event_instance = tuple(self.iter_with_id.chain)[-1]
        return last_event_instance.event if last_event_instance else None

    def nth(self, n):
        iten_id_chain = self.iter_with_id.chain
        return tuple(iten_id_chain)[n].event
    

class EventIteratorWithId:
    def __init__(self, reader, events):

        prev_index = max(0, reader.last_event_count - len(events.prev_events))
        curr_index = max(0, reader.last_event_count - len(events.curr_events))
        
        self.prev = events.prev_events[prev_index:]
        self.curr = events.curr_events[curr_index:]

        self.unread = len(self.prev) + len(self.curr)

        assert self.unread == reader.len(events), "Unread count mismatch"
        reader.last_event_count = events.event_count - self.unread
        self.chain = iter(self.a + self.b)


    def without_id(self):
        return EventIterator(self)
    

class EventCursor:
    def __init__(self):
        self.last_event_count = 0

    

    def len(self, events):
        return len(events.prev_events) + len(events.curr_events) - self.last_event_count


    def read_with_id(self, events):
        return EventIteratorWithId(self, events)


    def read(self, events):
        return self.read_with_id(events).without_id()
    

    def read_with_id(self, events):
        return self.read_with_id(events)


    def find(self, events, event_type):
        combined_events = events.prev_events + events.curr_events
        # for event_instance in combined_events:
        #     if isinstance(event_instance.event, event_type):
        #         return event_instance.event
        
        return [event_instance.event for event_instance in combined_events \
                if isinstance(event_instance.event, event_type)]