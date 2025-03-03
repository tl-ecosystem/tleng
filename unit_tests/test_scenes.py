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

from tleng2 import * 
from dataclasses import dataclass
from pygame import Surface, SurfaceType, FRect
import pygame as pg


# Testing Variable ______
class TestingVars:
    scene_changed = False

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

world1.spawn(
    Transform(1,2,3,4),
    Renderable(
        Surface((10,10)),
        FRect(0,0,10,10)
    )
)

world1.spawn(
    Transform(4,3,2,1)
)

world1.spawn(
    Transform(4,3,2,1),
    Animation([])
)

schedule1 = ecs.Scheduler()

# TODO add some systems here >:(
schedule1.add_systems( 'Update',
    
)

world1_scene = ecs.SceneComp(
    world1, schedule1
)

# SCENE 2 ___________
world2 = ecs.World()

world2.spawn(
    Transform(1,2,3,4),
    Renderable(
        Surface((10,10)),
        FRect(0,0,10,10)
    )
)

world2.spawn(
    Transform(4,3,2,1)
)

world2.spawn(
    Transform(4,3,2,1),
    Animation([])
)

schedule2 = ecs.Scheduler()

class System2(ecs.System):
    def parameters(self):
        ...

    def update(self):
        TestingVars.scene_changed = True

schedule2.add_systems( 'Update',
    System2()
)

world2_scene = ecs.SceneComp(
    world2, schedule2
)


def test_scenes():
    """Testing ECS scenes with App"""
    __name__ = "scenes"

    pg.init()
    
    game = App()

    game.load_scenes(
        start_with = 'scene1',
        scene1 = world1_scene,
        scene2 = world2_scene
    )

    game._init_run()

    game._running()
    game.scenes_manager.change_scene('scene2')
    game._running()
    game._running()

    assert TestingVars.scene_changed
    
if __name__ == '__main__':
    test_scenes()