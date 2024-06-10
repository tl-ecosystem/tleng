# ECS implementation inspired from Esper ECS : https://github.com/benmoran56/esper
# Naming schemes inspired from Bevy ECS : https://docs.rs/bevy_ecs/latest/bevy_ecs/

from dataclasses import dataclass
from itertools import count

# from ..engine.properties import EngineProperties
from typing import Any, Iterable
from ..utils.utils import first
from .system import System
from .component import Component


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        self.system_schedule: list[System] = []
    

    def add_systems(self, *systems) -> None: 
        for system in systems:
            self.system_schedule.append(system)
        
        self.system_schedule.sort(key=lambda syst: syst.priority, reverse=True)

    
    def init_systems(self, world) -> None:
        for system in self.system_schedule:
            system.change_world(world)


    def update(self) -> None:
        for system in self.system_schedule:
            system.update()


class ComponentManager:
    def __init__(self) -> None:
        self.cache = {}


    def get_components(self) -> None: 
        raise NotImplementedError


    def clear_cache(self) -> None:
        self.cache = {}


class World:
    """
    The ECS iplementation of the Scene class.

    The world contains every entity with it's respective components.
    """
    def __init__(self) -> None:

        self.id_count = count(start=0)
        self.dead_entities: set[int] = set()
        self.entity_db: dict[int, dict[Any, set]] = {}

        #  a sparse list of every entities pointing to their respective components
        self.components_db: dict[Any, set] = {} 


        self.components_caches = {}
        self.component_caches = {}


    def spawn(self, *components: Component) -> int:
        entity = next(self.id_count)

        if entity not in self.entity_db:
            self.entity_db[entity] = {}

        for component_instance in components:
            component_type = type(component_instance)

            if component_type not in self.components_db:
                self.components_db[component_type] = set()
            
            # we add the component type to the sparse list
            self.components_db[component_type].add(entity)

            # we create the entity with his components
            self.entity_db[entity][component_type] = component_instance

        return entity


    def despawn(self, entity: int, immediate: bool) -> None:
        """
        Despawns an entity from the id given.
        Every component that was associated with the entity is not deleted.

        Logs if the despawn was not succesfull
        :returns: Nothing
        """
        if immediate:
            for component_type in self.entity_db[entity]:
                self.components_db[component_type].discard(entity)

                # if in turn the sparse list of that component type is empty then delete it
                if not self.components_db[component_type]:
                    del self.components_db[component_type]

            del self.entity_db[entity]

            self.clear_cache()
        else:
            self.dead_entities.add(entity)


    def clear_components(self, entity: int) -> None: 
        """
        Clears all the components from the given entity id
        :returns: Nothing
        """
        raise NotImplementedError

    
    def kill(self, entity: int) -> None:
        """
        Despawns the Entity and clears all the components that it had.
        """
        raise NotImplementedError


    def use_schedule(self, schedule: Schedule) -> None:
        """
        Use the schedule that works best with the world created.
        """
        self.schedule = schedule
        self.schedule.init_systems(self)


    def run_schedule(self) -> None:
        self.schedule.update()


    def __get_components_has_without(self, 
                                          component_types: tuple, 
                                          has: tuple,
                                          without: tuple = ()
                                    ) -> Iterable[tuple[int, list[Component]]]:
        component_db = self.components_db
        entity_db = self.entity_db

        # for e in [e,e,e,e,e] - [ex,ex,ex] 
        #   entity_db[e][ct] for ct in component_types
        try:
            for entity in set.intersection(*[component_db[ct] for ct in (component_types + has)]) \
            .difference(*[component_db[ct] for ct in (without)]):
                
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except:
            pass

    
    def query(self, 
                    *component_types: Component, 
                    has: tuple[Component],  
                    without: tuple = ()
                ) -> Iterable[tuple[int, list[Component]]]:
        """
        Query in the same tuple all the wanted and `has` (tries to see if they 
        exists and only then it adds them to the tuple without adding the `has`)
        """
        
        try:
            return self.components_caches[(component_types, has, without)]
        except KeyError:
            return self.components_caches.setdefault(
                component_types, list(
                    self.__get_components_has_without(component_types, has, without=without)
                    )
                )


    def __get_components(self, *component_types) -> Iterable[tuple[int, list[Component]]]: 
        component_db = self.components_db
        entity_db = self.entity_db


        # for e in [{Comp1 e,e,e},{Comp2 e,e,e,e}]
        #   entity_db[e][ct] for ct in component_types
        try:
            for entity in set.intersection(*[component_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except:
            pass

    
    def fast_query(self, *component_types: Component,) -> Iterable[tuple[int, list[Component]]]:
        """
        Relatively to world.query() the fast_query is a faster implementation. as there are not more for loops while finding. 
        """
        try:
            return self.components_caches[component_types]
        except KeyError:
            return self.components_caches.setdefault(component_types, list(self.__get_components(*component_types)))
        


    def clear_cache(self) -> None:
        """
        Clears the caches from the Component Manager and the Entity Manager.
        """
        self.components_caches = {}
        self.component_caches = {}
    


