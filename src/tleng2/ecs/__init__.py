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

# ECS implementation inspired from Esper ECS : https://github.com/benmoran56/esper
# Naming schemes inspired from Bevy ECS : https://docs.rs/bevy_ecs/latest/bevy_ecs/

from dataclasses import dataclass as component

from .world import World
from .schedule import Scheduler
from .system import System, RunCondition, SystemSet
from .sequence import Sequence
from .scenes_manager import ScenesManager
from .events import EventsComp, Events, EventManagerSystem
from .ecs_scene import SceneComp

__all__ = [
    "component",
    "World",
    "Scheduler",
    "System", "RunCondition", "SystemSet",
    "Sequence",
    "ScenesManager",
    "EventsComp", "Events", "EventManagerSystem",
    "SceneComp",
]