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

from ..engine.settings import GlobalSettings

class Debugging:
    """
    Debugging component, used inside the properties of the app.
    """

def debug_print(
        *values: object, 
        sep: str | None = " ", 
        end: str | None = "\n", 
        file: None = None, 
        flush = False, 
        tags:list = []
    ) -> None:
    """
    Print statement that gets called only when the debug of the application is equal to `True`.
    Basically the Print function, but only print when `GlobalSettings._debug == True`
    """
    if GlobalSettings._debug and DebugTags.debug_tags is not []:
        for i in tags:
            if i in DebugTags.debug_tags:
                print(*values, sep=sep, end=end, file=file, flush=flush)
    elif GlobalSettings._debug:
        print(*values, sep=sep, end=end, file=file, flush=flush)


class DebugTags:
    '''
    Stores an active dictionary that upon called it will try to match what the 
    programmer wants to debug and subsequently approve calls that come from that source.
    '''

    debug_tags = []

    @staticmethod
    def import_tags(tags:list) -> None:
        DebugTags.debug_tags += tags  

# ScreenDebug is a UI element 
#        go find it in ui_elements/label.py 