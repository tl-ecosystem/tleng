'''
Scene handler
It justs puts the stuff on the screen and it handles scene changes like menu->game->pause screen etc.
'''

class Scene:
    def __init__(self): 
        raise NotImplementedError

# Scene grouping?
# Dictionary of scenes that upon render will be rendered the "cureent_scene, just like the animation"