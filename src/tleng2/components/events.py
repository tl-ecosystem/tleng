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

"""
All the Events that tleng2 uses
"""

from dataclasses import dataclass


class QuitGameEvent: ...


class ResizeWindowEvent: ...


@dataclass
class LeftMouseClick:
    """
    The position is relative to the window not to the world.
    """
    x: float
    y: float
    

@dataclass
class RightMouseClick:
    """
    The position is relative to the window not to the world.
    """
    x: float
    y: float


class PygameEvent:
    """
    All the events in pygame are presented with an integer number.
    """
    e: int


def default_events_bundle() -> list:
    """
    All the default events that tleng2 uses.
    """
    return [
        QuitGameEvent,
        ResizeWindowEvent,
        LeftMouseClick,
        RightMouseClick,
    ]
