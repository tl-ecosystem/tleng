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

from inspect import signature
from dataclasses import dataclass, field

from .system import System, SystemSet, RunCondition

from typing import Any as _Any


class LazyConditionTable(dict):
    ...


# TODO: some information here doesn't make sense...
@dataclass
class SequenceComp:
    system_sets: list[SystemSet] = field(default_factory=list)
    unique_systems: dict[type, System] = field(default_factory=dict)
    look_up: LazyConditionTable[_Any, bool] = field(default_factory=LazyConditionTable)
    lazy_conditions: dict[type, RunCondition] = field(default_factory=dict)  


class Sequence:
    def __init__(self):
        self.system_sets: list[SystemSet] = []
        self.unique_systems: dict[type, System] = {}
        self.look_up: LazyConditionTable[_Any, bool] = LazyConditionTable()
        self.lazy_conditions: dict[type, RunCondition] = {}


    def add_set(self, system_set):
        self.system_sets.append(system_set)


    # TODO: try to de couple plain systems to sets, but this will do for now
    def add_systems(self, *systems) -> None:
        system_set = SystemSet()
        system_set.add_systems(*systems)
        self.add_set(system_set)


    def __collect_unique_systems(self):
        all_systems = []
        for system_set in self.system_sets:
            all_systems.extend(system_set.collect_all_systems())

        # deduplication
        unique_systems = {}
        for system in all_systems:
            if system not in unique_systems:
                unique_systems[system] = system
            else:
                # Merge conditions if the system is reused
                # I am fairly certain that the first if is useless
                if unique_systems[system].conditions != system.conditions:
                    unique_systems[system].conditions.extend(system.conditions)

                if unique_systems[system].lazy_conditions != system.lazy_conditions:
                    unique_systems[system].lazy_conditions.extend(system.lazy_conditions)

        self.unique_systems = unique_systems
        

    def __collect_unique_lazy_conditions(self) -> None:
        """
        Must always run after the collect_systems
        """
        all_lazy_conditions = []

        for system in self.unique_systems.values():
            all_lazy_conditions.extend(system.lazy_conditions)


        # Could easily be combined into one dictionary... (idk why I implemented it this way...)
        unique_lazy_conditions = {}
        look_up_table: LazyConditionTable[_Any, bool] = LazyConditionTable()

        for lazy_condition in all_lazy_conditions:
            if lazy_condition not in unique_lazy_conditions and lazy_condition != None:
                unique_lazy_conditions[lazy_condition] = lazy_condition
                look_up_table[lazy_condition] = False

        self.lazy_conditions = unique_lazy_conditions
        self.look_up = look_up_table


    def update(self) -> None:
        if self.lazy_conditions:
            for run_condition in self.lazy_conditions.values():
                self.look_up[run_condition] = run_condition.update()
        
        for system in self.unique_systems.values():
            system.executor()


    def __inject_dependecies(self, system: System | RunCondition, parameters: dict[type, _Any]) -> list:
        syst_param_signature = signature(system.parameters)
        params = syst_param_signature.parameters

        # Determine which parameters to inject based on type annotations
        injection_args = []

        for param in params.values():
            annotation = param.annotation

            injection_args.append(parameters[annotation])
        
        return injection_args


    def init(self, parameters: dict[type, _Any]) -> None:
        """
        Instantiates the systems on their parameters. It analyzes the parameters 
        and injects what they asked for.
        """
        # this algo needs to run in all the unique systems!
        self.__collect_unique_systems()
        self.__collect_unique_lazy_conditions()

        
        parameters[LazyConditionTable] = self.look_up

        try:
            for system in self.unique_systems.values():
                system.init()
                # come up with a better solution for this...
                system._lazy_look_up = self.look_up
                system.parameters(*self.__inject_dependecies(system, parameters))

                for run_condition in system.conditions:
                    run_condition.parameters(*self.__inject_dependecies(run_condition, parameters))
                              

        except KeyError as key:
            print(f"""KeyError occured, 
                      - <{key}> was wrongly typed in the parameters of the systems
                      - key: <{key}> was either not initialized in app or 
                      - <{key}> was not properly put in the parameter of the app"""
            )