# Copyright (c) 2023 Theolaos

# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to 
# whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the 
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .schedule import Schedule
from .world import World

class Commands:
    def __init__(self):
        # private members are written like this
        self.__command_queue = []
        self.__world: World = None

        self.__schedule: Schedule = None


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
                (entity_id,), self.__world.despawn
            )
        )
    
    
    def despawn(self, entity, immediate) -> None:
        self.__world.despawn(entity=entity, immediate=immediate)

    
    def enable_state(self, state_name: str) -> None:
        """
        Enables a specific state.
        """
        ...
    

    def disable_state(self, state_name: str) -> None:
        """
        Disables a specific state that isn't one of the default states:
        ['First', 'PreUpdate', 'Update', 'PostUpdate', 'PreRenderer', 'Renderer', 'Last']
        """
        ...

    
    def change_state(self, state_group: str, state_name: str) -> None:
        """
        From the passed state group, it changes the state to the one passed.
        Frees the programmer from constantly checking to disable the other active state from
        the state group.
        
        Example:
        'MyPausedState' = ['Paused', 'Running']
        current_state = 'Paused'
        # with change_state you can change 'Paused' to 'running'
        """
        ...


    def update(self):
        if self.__command_queue:
            command_queue = self.__command_queue

            for args, command in command_queue:
                command(*args)

            command_queue.clear()
