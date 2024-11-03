from dataclasses import dataclass

from ..ecs import *

"""
A collection of components needed to declare the world, for the game.
"""

class SettingsComp: ...


@dataclass
class FpsComp:
    fps: int


# maybe not needed
@dataclass
class RendererParamsComp:
    """
    parameters syntax:
    {
        "scene_name" : {
            "display" : pygame.Surface
            "camera" : "camera_name"
        }
    }
    """
    params: dict
        