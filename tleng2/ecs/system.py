from abc import abstractmethod


class System:
    def __init__(self, world) -> None:
        self.priority: int = 0
        self.world = world

    @abstractmethod
    def update(self) -> None:
        ...

"""
class Movement(System):
    update(self):
        for entity, (coordinate, are) in self.world.query(Coordinate2, AreaComponent):
        
"""