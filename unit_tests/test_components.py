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
    test_components()