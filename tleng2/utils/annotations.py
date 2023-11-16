import pygame
from typing import AnyStr, Dict, Int, Sequence, Tuple, Union

Coordinate = Union[Tuple[float, float], Sequence[float], pygame.math.Vector2]
# {"%name_anim1%" : {"anim":[str,str,...], "frames" : int}, "%name_anim2%" : {"anim":[str,str,...], "frames" : int}, ...}