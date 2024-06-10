from abc import abstractmethod
from .world import World


class System:
    def __init__(self, priority: int = 0) -> None:
        self.priority: int = priority
        self.world: World = None


    def change_world(self, world) -> None:
        self.world = world


    @abstractmethod
    def update(self) -> None:
        ...

"""
class Movement(System):
    update(self):
        for entity, (coordinate, are) in self.world.query(Coordinate2, AreaComponent):
        
"""