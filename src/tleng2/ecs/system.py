from abc import abstractmethod


class System:
    def __init__(self, priority: int = 0) -> None:
        self.priority: int = priority
        self.enabled = True

    @abstractmethod
    def parameters(self,) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...


"""
class Movement(System):
    parameters(query: Query, commands: Commands)
        self.commands = commands
        self.query = query

    update(self):
        for entity, (coordinate, area) in self.query(Coordinate2, AreaComponent):
        
"""