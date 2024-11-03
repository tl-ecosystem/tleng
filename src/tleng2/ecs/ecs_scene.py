from dataclasses import dataclass

from .world import WorldComp
from .schedule import Schedule


@dataclass
class SceneComp:
    world: WorldComp
    schedule: Schedule