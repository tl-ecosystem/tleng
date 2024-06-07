from itertools import count

from .system import System
from .component import Component


class Schedule:
    def __init__(self) -> None:
        self.system_schedule: list[System] = []
    

    def add_systems(self, *systems) -> None:
        self.system_schedule.append(*systems)


class EntityManager:
    """
    Id should only be positive numbers.

    free entities are the entities that have been deleted. 
    But their components still have their id.
    """
    def __init__(self) -> None:
        self.id: int = count(start=-1)
        self.free_entities: set[int] = set()
        self.entities: set[int] = set()

        self.caches: dict = {}


    def spawn(self) -> int:
        if self.free_entities:
            temp_id = self.free_entities[0]
            self.entities.add(temp_id) 
            self.free_entities.remove(temp_id)
            return temp_id
        else:
            next(self.id)
        
            return self.id
        
    
    def despawn(self, _id: int) -> None:
        try:
            self.free_entities.remove(_id)
        except KeyError:
            # TODO: Log the error
            print(f"(logger is not implemented) Unssuccesfull despawn of Entity with id: #{_id}")


    def clear_cache(self) -> None:
        self.caches = {}


class ComponentManager:
    def __init__(self) -> None:
        pass


class World:
    """
    The ECS iplementation of the Scene class.

    The world contains every entity with it's respective components.
    """
    def __init__(self) -> None:
        self.entity_manager = EntityManager()

        self.component_manager = ComponentManager()

        self.archetypes_table: list = []


    # i don't really like this code
    def create_entities(self, *components: list[Component]) -> list[int]:
        self.entities += components
        return self.id
    

    def spawn(self, *components: Component) -> int:
        _id = self.entity_manager.spawn()


        return _id


    def despawn(self, id) -> None:
        """
        Despawns an entity from the id given.
        Every component that was associated with the entity is not deleted.

        Logs if the despawn was not succesfull
        :returns: Nothing
        """
        self.entity_manager.despawn(id)


    def clear(self, id) -> None: 
        """
        Clears all the components from the given id
        :returns: Nothing
        """
        ...

    
    def kill(self, id) -> None:
        """
        Despawns the Entity and clears all the components that it had.
        """
        ...


    def use_schedule(self, schedule: Schedule) -> None:
        """
        Use the schedule works best with the world created.
        """
        self.schedule = schedule


    def query(self, *components: Component, optional: list[Component] = None) -> tuple[int, list[Component]]:
        ...

    
    def clear_cache(self) -> None:
        """
        Clears the caches from the Component Manager and the Entity Manager.
        """
        self.entity_manager.clear_cache()
        self.component_manager.clear_cache()