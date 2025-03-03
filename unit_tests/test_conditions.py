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

from tleng2 import * 

output = []

ctx = {
    'run_a':True,
    'run_b':True,
    'run_c':True,
    'set_a':True,
    'set_b':True,
    'set_c':True,
}

temp_ctx = ctx.copy()

class System_a(ecs.System):
    def update(self) -> None:
        output.append(1)

    def params(self):
        ...
        

class System_b(ecs.System):
    def update(self) -> None:
        output.append(2)

    def params(self):
        ...


class System_c(ecs.System):
    def update(self) -> None:
        output.append(3)

    def params(self):
        ...


class Run_a(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['run_a']


class Run_b(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['run_b']
    

class Run_c(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['run_c']

# Nested Sets

class Level3(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['set_c']


class Level2(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['set_b']


class Level1(ecs.RunCondition):
    def params(self,):
        ...    
    
    def update(self):
        return ctx['set_a']


set_level_1 = ecs.SystemSet(condition=Level1())
set_level_2 = ecs.SystemSet(condition=Level2()).in_set(set_level_1)
set_level_3 = ecs.SystemSet(condition=Level3()).in_set(set_level_2)

# Systems with conditions
system_a_instance = System_a(conditions=[Run_a()]).in_set(set_level_1)
system_b_instance = System_b(conditions=[Run_b()]).in_set(set_level_2)
system_c_instance = System_c(conditions=[Run_c()]).in_set(set_level_3)


# Sequence
sequence = ecs.Sequence()
sequence.add_set(set_level_1)
sequence.init()

# Testing run conditions
sequence.execute()
assert output == [1,2,3]

ctx['run_a'] = False
output = []
sequence.execute()
assert output == [2,3]

ctx['run_b'] = False
output = []
sequence.execute()
assert output == [3]

# Resetting
output = []
ctx = temp_ctx.copy()

# Testing set conditions
ctx['set_a'] = False
output = []
sequence.execute()
assert output == []

ctx['set_a'] = True
ctx['set_b'] = False
output = []
sequence.execute()
assert output == [1]

ctx['set_b'] = True
ctx['set_c'] = False
output = []
sequence.execute()
assert output == [1,2]

ctx['set_c'] = True
output = []
sequence.execute()
assert output == [1,2,3]

# TODO: Testing lazy conditions