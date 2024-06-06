from abc import abstractmethod


class System:
    def __init__(self, world) -> None:
        self.world = world

    @abstractmethod
    def update(self) -> None:
        ...

"""
class Movement(System):
    update(self):
        for entity, (coordinate, are) in self.world.get_component(Coordinate2, AreaComponent):
        
"""


class system(object):
    def __init__(self, query, world) -> None:
        self.query = query
        self.world = world
        self.priority: int = 0


    def __call__(self, func):
        def wrapped():
            return func(self.world.get_component(*self.query))
        return wrapped


"""
# a function based system (more dynamic than the class based one)

@system(query=(Coordinates2, AreaComponent), world = world)
def HitboxSystem(items) -> None:
    for entity, (coordinate, area) in items:
        ...     
"""