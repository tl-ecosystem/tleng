"""
_________________

for reference
_________________

"""

import sys


__author__ = "Theooking/Theolaos"
__version__ = "v2.2-exp"



__doc__ = f'''
TLeng2.py is a python 2d game engine

Current version is {__version__}

Simplification, with overcomplication update ;D

'''
# _________________________________________________________GAME ENGINE FUNCTIONS ___________________________________________________________________________________

# All these functions below were not tested, so it's unclear if they work or not. And because these are easy functions, i suggest that you type them yourself
#    in the main.py of your game. As it may speed up things a little bit.


def flip(img : pygame.rect.Rect, boolX : bool, boolY : bool):
    '''
    Flips the image according to the booleans

    :param img: the loaded image object 
    :param boolX: The boolean variable that will determine if the image is flipped in the X axis
    :param boolY: The boolean variable that will determine if the image is flipped in the Y axis
    :return: It returns the flipped image
    '''
    return pygame.transform.flip(img, boolX, boolY)


def load_image(img_filepath: str, surface:pygame.Surface):
    '''
    Loading an image

    :param img_filename: the file path of the image
    :return: It returns the loaded image (uses convert to make the game more efficient)
    '''
    return pygame.image.load(img_filepath).convert_alpha(surface)


# _______________________________________________________ Game Engine __________________________________________________________

class TlenGame: 
    def __init__(self,scenes):
        pygame.font.init()
        pygame.mixer.init()
        self.scenes = SceneHandler(scenes)


    def run(self, tleng2_intro:bool=True):
        '''
        to play the game
        '''
        if tleng2_intro:
            pass

        self.running = True
        while self.running:
            # handle the scene from here
            self.scenes.scene_phase()

        pygame.quit()
        sys.exit()