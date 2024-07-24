from itertools import count

# from ..engine.properties import EngineProperties
from typing import Any, Iterable


class Component: 
    """
    Here for symbolic reasons
    """


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
        self.components_caches
    

    def add_components(self, entity: int, components: Component) -> None: 
        """
        Adds components to the given entity id
        :returns: Nothing
        """
        raise NotImplementedError


    def __get_components_has_without(self, 
                                          component_types: tuple, 
                                          has: tuple[Component] = (),
                                          without: tuple[Component] = ()
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
                    has: tuple[Component] = (),  
                    without: tuple[Component] = ()
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
    

    def __get_component(self, component_type) -> Iterable[tuple[int, Component]]:
        entity_db = self.entity_db

        for entity in self.components_db.get(component_type, []):
            yield entity, entity_db[entity][component_type]


    def single_fast_query(self, component_type: Component) -> Iterable[tuple[int, Component]]:
        try:
            return self.components_caches[component_type]
        except KeyError:
            return self.components_caches.setdefault(component_type, list(self.__get_component(component_type)))


    def clear_cache(self) -> None:
        """
        Clears the caches from the Component Manager and the Entity Manager.
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

