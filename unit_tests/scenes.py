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

schedule1 = ecs.Schedule()

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

schedule2 = ecs.Schedule()

schedule2.add_systems( 'Update',
    
)

world2_scene = ecs.SceneComp(
    world2, schedule2
)


def main():
    game = App()

    game.use_plugins(
        tleng_base_plugin
    )

    game.load_scenes(
        start_with = 'scene1',
        scene1 = world1_scene
    )

    game.run()