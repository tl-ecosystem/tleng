# ECS implementation inspired from Esper ECS : https://github.com/benmoran56/esper
# Naming schemes inspired from Bevy ECS : https://docs.rs/bevy_ecs/latest/bevy_ecs/

from dataclasses import dataclass as component

from .world import World
from .schedule import Schedule
from .system import System
# from .worlds_manager import WorldsManager
from .scenes_manager import ScenesManager
from .events import EventsComp, Events, EventManagerSystem
from .ecs_scene import SceneComp

__all__ = [
    "component",
    "World",
    "Schedule",
    "System",
    "EventsComp", "Events", "EventManagerSystem",
    "SceneComp",
]