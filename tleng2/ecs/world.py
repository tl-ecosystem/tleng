from itertools import count

from .events import Events
# from ..engine.properties import EngineProperties


from typing import Any as _Any
from typing import Iterable as _Iterable


class Component:
    """
    here for symbolic reasons
    """


class World:
    """
    The ECS iplementation of the Scene class.

    The world contains every entity with it's respective components.
    """
    def __init__(self, events = False) -> None:
        self.id_count = count(start=0)
        self.dead_entities: set[int] = set()
        self.entity_db: dict[int, dict[_Any, set]] = {}

        #  a sparse list of every entities pointing to their respective components
        self.components_db: dict[_Any, set] = {} 

        self.components_caches = {}
        self.component_caches = {}

        self.unique_components = {}

        if events:
            self.events = Events(self)


    
    def append_unique_components(self, info: dict[type, _Any]) -> None:
        """
        Appends unique components to the world itself.
        
        Example:
        {
            ComponentType: Compoenent, ...
        }
        """
        self.unique_components.update( info )


    def spawn(self, *components: Component) -> int:
        """
        Spawns an entity with the components provided and returns the id of the entity. 
        """
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
        for component_type in self.entity_db[entity]:
            self.components_db[component_type].discard(entity)

            # if in turn the sparse list of that component type is empty then delete it
            if not self.components_db[component_type]:
                del self.components_db[component_type]

        self.clear_cache()

    
    def remove_component(self, entity: int, component_type: Component) -> None:
        """
        Removes component by type.
        """
        self.components_db[component_type].discard(entity)

        if not self.components_db[component_type]:
            del self.components_db[component_type]

        self.clear_cache()

    def remove_components(self, entity: int, *components: Component) -> None:
        """
        Removes components by type from a given entity id.
        """
        raise NotImplementedError
    

    def add_component(self, entity: int, component: Component) -> None: 
        """
        Adds a component to the given entity id.
        :returns: Nothing
        """
        component_type = type(component)

        if component_type not in self.components_db:
            self.components_db[component_type] = set()

        self.components_db[component_type].add(entity)

        self.entity_db[entity][component_type] = component
        self.clear_cache()
    

    def has_component(self, entity: int, component_type: Component) -> bool:
        assert type(entity) == int, 'The entity need to be an integer'
        return component_type in self.entity_db[entity]
    
    
    def has_components(self, entity: int, *component_types: Component) -> bool:
        """Check if an Entity has all the specified Component types."""
        return all(comp_type in self.entity_db[entity] for comp_type in component_types)


    def __get_components_has_without(self, 
            component_types: tuple, 
            has: tuple[Component] = (),
            without: tuple[Component] = ()
        ) -> _Iterable[tuple[int, list[Component]]]:

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
                    has: tuple[Component] = (),  
                    without: tuple[Component] = ()
                ) -> _Iterable[tuple[int, list[Component]]]:
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


    def __get_components(self, *component_types) -> _Iterable[tuple[int, list[Component]]]: 
        component_db = self.components_db
        entity_db = self.entity_db


        # for e in [{Comp1 e,e,e},{Comp2 e,e,e,e}]
        #   entity_db[e][ct] for ct in component_types
        try:
            for entity in set.intersection(*[component_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except:
            pass

    
    def fast_query(self, *component_types: Component,) -> _Iterable[tuple[int, list[Component]]]:
        """
        Relatively to world.query() the fast_query is a faster implementation. as there are not more for loops while finding. 
        """
        try:
            return self.components_caches[component_types]
        except KeyError:
            return self.components_caches.setdefault(component_types, list(self.__get_components(*component_types)))
    

    def __get_component(self, component_type) -> _Iterable[tuple[int, Component]]:
        entity_db = self.entity_db

        for entity in self.components_db.get(component_type, []):
            yield entity, entity_db[entity][component_type]


    def single_fast_query(self, component_type: Component) -> _Iterable[tuple[int, Component]]:
        try:
            return self.components_caches[component_type]
        except KeyError:
            return self.components_caches.setdefault(component_type, list(self.__get_component(component_type)))
        

    def clear_cache(self) -> None:
        """
        Clears the caches from the Component caches and the Entity caches.
        """
        self.components_caches = {}
        self.component_caches = {}
    

    def use_schedule(self, schedule) -> None:
        """
        Use the schedule that works best with the world created.
        """
        self.schedule = schedule
        self.schedule.init_systems(self)


    def run_schedule(self) -> None:
        self.schedule.update()

