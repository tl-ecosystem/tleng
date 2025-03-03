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

from abc import abstractmethod

from typing import Optional as _Optional
from typing import List as _List

class RunCondition:
    def __init__(self) -> None:
        """
        A Run Condition is needed by system to determine if it should run in the current frame or not.
        The same thing applies to sets.
        """
        pass

    @abstractmethod
    def parameters(self,) -> None:
        ...

    @abstractmethod
    def update(self) -> bool:
        ...


class System:
    def __init__(self, conditions: _Optional[_List[RunCondition]] = None):
        self.conditions = conditions if conditions else []
        self.lazy_conditions = [] # A list with the RunConditions of the set 
        self._lazy_look_up = []
        # this system belongs, to look up if the set is runnable. 
        self.enabled = True
        self.priority = 0


    def add_conditions(self, *conditions: RunCondition) -> None:
        self.conditions.extend(conditions)

    
    def add_lazy_conditions(self, *lazy_conditions: RunCondition) -> None:
        self.lazy_conditions.extend(lazy_conditions)

    
    def in_set(self, set):
        set.add_systems(self)
        self.lazy_conditions.append(set.condition)
        return self


    def init(self):
        if self.conditions and self.lazy_conditions:
            self.executor = self._execute
        elif self.conditions:
            self.executor = self._update
        else:
            self.executor = self.update


    def _execute(self):
        if all(condition.update() for condition in self.conditions) and \
            all(self._lazy_look_up[condition] for condition in self.lazy_conditions):
            self.update()

    
    def _update(self):
        if all(condition.update() for condition in self.conditions):
            self.update()


    @abstractmethod
    def parameters(self) -> None:
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
            ...

system = Movement().in_set(<some_set>)
"""

class SystemSet:
    def __init__(self, condition: _Optional[RunCondition] = None):
        self.condition = condition
        self.systems: _List[System] = []
        self.subsets: _List = []  # For nested sets


    def in_set(self, set):
        """
        Puts the current set into the passed set.

        Returns self
        """
        set.subsets.append(self)
        return self
    

    def add_systems(self, *systems) -> None:
        self.systems.extend(systems)

    
    def add_subsets(self, *subsets) -> None:
        """
        A subset is a set within a set :)
        """
        self.subsets.extend(subsets)

    # TODO: Maybe this could be simplified, idk
    def collect_all_systems(self, parents_set_conditions: _Optional[_List[RunCondition]] = None):
        set_conditions = [self.condition]
        if parents_set_conditions:
            set_conditions.extend(parents_set_conditions)

        all_systems = []
        # Add systems with combined conditions
        for system in self.systems:
            # merged_conditions = system.conditions + [combined_condition]
            system.lazy_conditions.extend(set_conditions)
            all_systems.append(system)

        # Collect systems from subsets
        for subset in self.subsets:
            all_systems.extend(subset.collect_all_systems(set_conditions))

        return all_systems