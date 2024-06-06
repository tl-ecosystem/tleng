from abc import abstractmethod

class Component:
    @abstractmethod
    def __init__(self) -> None:
        """
        Needs to have the self.id variable
        """
        self.id: int = -1
        

class ComponentManager: ...