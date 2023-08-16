from assets.scripts.engine.utils.TlengArea import * # pygame
from assets.scripts.engine.utils.TlengEntity import *
from assets.scripts.engine.utils.TlengLabel import * 
from assets.scripts.engine.utils.TlengObject import *
from assets.scripts.engine.utils.TlengProjectile import *
from assets.scripts.engine.TlengUI import * 
import sys



__author__ = "Theolaos"
__version__ = "2.2-exp"

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
# update : updates the state of the class


'''
TLeng2.py a python 2d game engine

Current version is v2.2-exp

Simplification, with overcomplication update ;D

'''
# _________________________________________________________GAME ENGINE FUNCTIONS ___________________________________________________________________________________

# All these functions below were not tested, so it's unclear if they work or not. And because these are easy functions, i suggest that you type them yourself
#    in the main.py of your game. As it may speed up things a little bit.


def collidepoint(rect : pygame.rect.Rect, x : float, y : float):
    '''
    Checks if the rectangle collided with a point

    :param rect:
    :param x: The X coordinate of the point
    :param y: The Y coordinate of the point
    :return: It returns if the rectangle collided with the point
    '''
    return rect.collidepoint(x,y)
        
def colliderect(rect : pygame.rect.Rect, rect2 : pygame.rect.Rect):
    '''
    Checks if the rectangels collided

    :param rect: the rect that you are currently using
    :param rect2: the other rect that you want to check
    :return: It returns if the rectangles collided
    '''

    return rect.colliderect(rect2)

def flip(img : pygame.rect.Rect, boolX : bool, boolY : bool):
    '''
    Flips the image according to the booleans

    :param img: the loaded image object 
    :param boolX: The boolean variable that will determine if the image is flipped in the X axis
    :param boolY: The boolean variable that will determine if the image is flipped in the Y axis
    :return: It returns the flipped image
    '''
    return pygame.transform.flip(img, boolX, boolY)

def load_image(img_filepath,surface:pygame.Surface):
    '''
    Loading an image

    :param img_filename: the file path of the image
    :return: It returns the loaded image (uses convert to make the game more efficient)
    '''
    return pygame.image.load(img_filepath).convert_alpha(surface)

def entity_xy_cords(entity : Entity, entity2 :Entity): # TODO: do this or delete it
    '''
    Returns the X and Y coordinate of the entity
 
    '''

# _______________________________________________________ Game Engine __________________________________________________________

class TlenGame: 
    def __init__(self):
        pygame.font.init()
        pygame.mixer.init()
        self.running = False


    def on_init():
        '''
        Class objects, Entities, 
        '''
        pass

    def handle_events(self):
        '''
        To handle the events of mouse and other
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''
    def render(self):
        '''
        what to render to the screen
        '''

    def update(self):
        '''
        game logic
        '''


    def run(self, intro:bool=True):
        '''
        to play the game
        '''
        self.running = True
        while self.running:
            # first handle the events
            self.handle_events()
            # after we get the events then update
            self.update()
            # then you can render
            self.render()

        pygame.quit()
        sys.exit()


# global indexEvent
# indexEvent = 1

# global animation_database
# animation_database = {}