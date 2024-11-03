from .world import World

class Commands:
    def __init__(self):
        # private members are written like this
        self.__command_queue = []
        self.__world: World = None


    def qspawn(self, *components) -> int:
        entity_id = self.__world.id_count
        self.__command_queue.append(
            (
                (entity_id, *components) , self.__world._spawn_id
            )
        )
        return entity_id


    def spawn(self, *components) -> int:
        return self.__world.spawn(*components)
    

    def qdespawn(self, entity_id) -> None:
        self.__command_queue.append(
            (
                (entity_id,) , self.__world.despawn
            )
        )
    
    
    def despawn(self, entity, immediate) -> None:
        self.__world.despawn(entity=entity, immediate=immediate)


    def update(self):
        command_queue = self.__command_queue

        for args, command in command_queue:
            command(*args)

        command_queue.clear()
