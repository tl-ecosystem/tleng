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

import os

from math import pi
from time import time

from ..engine.settings import GlobalSettings
from .debug import debug_print
from .annotations import TypeVar


def convert_deg_to_rad(deg) -> float:
    return (deg*pi)/180


def convert_rad_to_deg(rad) -> float:
    return (rad*180)/pi


def timer_func(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 


def timer_func_debug(func): 
    """    
    This function shows the execution time of  
    the function object passed 
    maybe not so optimized
    """
    def wrap_func(*args, **kwargs): 
        result = None
        if GlobalSettings._debug:
            t1 = time() 
            result = func(*args, **kwargs) 
            t2 = time() 
        else:
            result = func(*args, **kwargs) 

        debug_print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 


def get_parent_dir(path, directories=1) -> str:
	path_result = None
	for i in range(directories):
		path_result = get_parent_dir(path.rpartition(os.sep)[0], i)
	return path_result or path


def first(s: set) -> TypeVar:
    """
    Get the first item in a Set()
    """
    for i in s:
        return i