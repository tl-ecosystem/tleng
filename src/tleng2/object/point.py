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

from pygame import Vector2, draw, surface
from ..components.renderable import Renderable
from ..utils.colors import RED
from ..utils.annotations import Color

class Point:
    """
    Point in 2d space.
    A way to store the x,y values.
    Used to declare the center of smt.
    """
    def __init__(self, 
            x: int | float , 
            y: int | float, 
            radius: int = 1,
            color: Color = RED
        ) -> None:
        self.point = Vector2(x,y)
        self.renderable = Renderable()
        self.renderable.update_cords(x,y)
        self.renderable.update_surf(surface.Surface((radius*2,radius*2)))
        draw.circle(self.renderable.surface,color,(radius, radius), radius)

    def update(self, 
            x: int | float, 
            y: int | float
        ) -> None:
        self.point.x = x
        self.point.y = y
        self.renderable.update_cords(x,y)


    def render(self) -> None:
        self.renderable.render()
