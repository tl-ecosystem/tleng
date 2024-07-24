# Event System from EsperECS :: https://github.com/benmoran56/esper.git

# The MIT License (MIT)

# Copyright (c) 2024 Benjamin Moran

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from weakref import ref as _ref
from weakref import WeakMethod as _WeakMethod
from types import MethodType as _MethodType
from typing import Callable as _Callable
from typing import Any as _Any

class EventManager:
    sdasdads
    event_registry = {}

    def dispatch_event(name: str, *args: _Any) -> None:
        """Dispatch an event by name, with optional arguments.

        Any handlers set with the :py:func:`esper.set_handler` function
        will recieve the event. If no handlers have been set, this
        function call will pass silently.

        :note:: If optional arguments are provided, but set handlers
                do not account for them, it will likely result in a
                TypeError or other undefined crash.
        """
        for func in event_registry.get(name, []):
            func()(*args)


    def _make_callback(name: str) -> _Callable[[_Any], None]:
        """Create an internal callback to remove dead handlers."""

        def callback(weak_method: _Any) -> None:
            event_registry[name].remove(weak_method)
            if not event_registry[name]:
                del event_registry[name]

        return callback


    def set_handler(name: str, func: _Callable[..., None]) -> None:
        """Register a function to handle the named event type.

        After registering a function (or method), it will receive all
        events that are dispatched by the specified name.

        .. note:: A weak reference is kept to the passed function,
        """
        if name not in event_registry:
            event_registry[name] = set()

        if isinstance(func, _MethodType):
            event_registry[name].add(_WeakMethod(func, _make_callback(name)))
        else:
            event_registry[name].add(_ref(func, _make_callback(name)))


    def remove_handler(name: str, func: _Callable[..., None]) -> None:
        """Unregister a handler from receiving events of this name.

        If the passed function/method is not registered to
        receive the named event, or if the named event does
        not exist, this function call will pass silently.
        """
        if func not in event_registry.get(name, []):
            return

        event_registry[name].remove(func)
        if not event_registry[name]:
            del event_registry[name]