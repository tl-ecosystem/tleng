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

from pygame.math import Vector2
#from pygame._common import RectValue
from typing import IO, Callable, Tuple, Union, TypeVar
# from typing_extensions import Literal as Literal, SupportsIndex as SupportsIndex
# from typing_extensions import Protocol
from typing import Sequence, Tuple, Union, overload

# Coordinate = Union[Tuple[float, float], Vector2()]
Color = Union[Tuple[int,int,int, int], Tuple[int,int,int]]
# {"%name_anim1%" : {"anim":[str,str,...], "frames" : int}, "%name_anim2%" : {"anim":[str,str,...], "frames" : int}, ...}

Coordinate = Sequence[float]
Vertex = Vector2
VertRect = Sequence[Vertex]