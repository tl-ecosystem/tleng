'''
Testing ECS components
'''

from tleng2 import * 
from dataclasses import dataclass
from pygame import Surface, SurfaceType, FRect

# Components ______

@dataclass
class Transform:
    x: float
    y: float
    rot: float
    s: int


@dataclass
class Animation:
    frames: list[SurfaceType]


@dataclass
class Renderable:
    renderable: SurfaceType
    rect: FRect


# Systems ______

class LogicTransform(ecs.System):
    ...

# SCENE 1 ___________
world1 = ecs.World()

e1 = world1.spawn(
    Transform(1,2,3,4),
    Renderable(
        Surface((10,10)),
        FRect(0,0,10,10)
    )
)

e2 = world1.spawn(
    Transform(4,3,2,1)
)

e3 = world1.spawn(
    Transform(4,3,2,1),
    Animation([])
)


e4 = world1.spawn(
    Transform(4,3,2,1),
    Renderable(
        Surface((10,10)),
        FRect(0,0,10,10)
    ),
)

e_list = [
    e1,
    e2,
    e3,
    e4,
]

def test_components() -> bool:
    '''Testing ECS components'''
    __name__ = 'components'

    c = world1.fast_query(Transform)
    assert len(c) == len(e_list)
    
    c = world1.fast_query(Animation)
    assert len(c) == 1

    
    c = world1.fast_query(Renderable)
    assert len(c) == 2


if __name__ == '__main__':
    print(test_components())