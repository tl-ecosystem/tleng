"""
All the Events that tleng2 uses
"""

class QuitGameEvent: ...

class ResizeWindowEvent: ...

def default_events_bundle() -> list:
    return [
        QuitGameEvent,
        ResizeWindowEvent
    ]
