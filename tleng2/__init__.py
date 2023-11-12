from .engine.area import *
from .engine.entity import *
from .ui_elements.label import * 
from .physics.object import *
from .physics.projectile import *
from .engine.scene import *
from .ui_manager import * 

__author__ = "Theooking/Theolaos"
__version__ = "v2.2-exp"

__doc__ = f'''
TLeng2.py is a python 2d game engine

Current version is {__version__}

Simplification, with overcomplication update ;D

'''

# Ideas Report: About the events, you can make the user add the events to a specialised class variable in the abstractbutton class
# Report:
# TODO: proposal on changing the system from based to rect.x and rect.y to being based to a float coordination variable (pygame-ce has frects which allow for floating points)
# TODO: adding the ability to either add the assets from the relative directory or from the whole directory (if one fails use other)
# TODO: Make the code 'safer' , there are a lot of instances where you check if that do that, try using the 'try, except, finally' , maybe gonna ease the pain?
# TODO: If current working directory doesn't work then you also use the global directory, which can be accesed from the constant variable `LOCAL_DIRECTORY` and the current working directory

# TODO: Redo the Label system in update 2.2 and add:
#       capitilize / lower
#       striketrough, underlined
#       left|Center|Right
#       find
#       join
#       change_{smt}
#       __len__, __str__



# Framework/Engine vocab: 
# Draw ~ display ~ render : render to the window
# update : updates the state of the class/object