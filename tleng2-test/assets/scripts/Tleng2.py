import pygame, os, math
from time import sleep,time
pygame.font.init()
pygame.mixer.init()


# _____________________________________________________ COLORS THAT I NEEDED THUS FAR  (RGB: RED, GREEN, BLUE)______________________________________________________

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

# _________________________________________________________GAME ENGINE FUNCTIONS ___________________________________________________________________________________

def collidepoint(rect, x, y):
    return rect.collidepoint(x,y)
        
def colliderect(rect, rect2):
    return rect.colliderect(rect)

def flip(img, boolX : bool, boolY : bool):
    return pygame.transform.flip(img,boolX,boolY)

def load_image(img_filename):
    return pygame.image.load(img_filename).convert()

def entity_xy_cords():
    pass

global animation_database
animation_database = {}

# AREA ______________________________________________#

class Area():
    '''
    Class for area
    '''
    def __init__(self, window:pygame.Surface, x:float = 0, y:float = 0, width:float = 10, height:float = 10,  color:tuple = WHITE):
        '''
        Initialising the Area
        
        :param window: It is the window that you want the area to be drew at (pygame Surface)
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the area (float)
        :param height: The height of the area (float)
        :param color: The color of the Area (tuple)
        '''
        self.rect = pygame.Rect(x-width/2, y-height/2, width, height)
        self.coreX = x
        self.coreY = y
        self.coreWidth = width
        self.coreHeight = height
        self.window = window
        self.color = color  
          
    def draw_Area(self):
        '''Draws the area in the screen'''
        pygame.draw.rect(self.window, self.color, self.rect)

    def outline_Area(self, thic=1, frame_color=BLACK):
        '''
        It draws the outline of the area by creating another rect object
        
        :param thic: it's the thickness of the Area's outline, if it is more than 
        :param 
        '''

        if thic > 0:
            pygame.draw.rect(self.window, frame_color, pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2),thic) #outside outline (*performnce issue)
        elif thic <= 0:
            pygame.draw.rect(self.window, frame_color, self.rect, abs(thic)) # inside outline (*performnce issue)
            if thic == 0:
                print("the thickness of the outline is zero, you can not see it") #giving a "warning" that the thickness of the outline is zero (for performance reasons we could remove it in production)


# TEXT ______________________________________________#

class Label(Area):
    '''
    Label is for displaying text.
    '''
    def set_Label(self, text, tsize=12, tcolor=BLACK, tbold=False):
        '''
        Storing the text class in a variable for later usage, The Label is created by using a rectangle 
        To draw the text use drawText

        :param text: Type the text you want to store
        :param tsize: It's the desired size for your text (default size 12)
        :param tcolor: It's the desired color for your text (default color BLACK)
        :param tbold: If you want for your text to be bold set it to True (default to False)
        :return: Nothing
        '''

        self.font = pygame.font.SysFont('verdana', tsize, tbold).render(text, True, tcolor)

    def draw_Label(self, shift_x=0, shift_y=0,fillbfr=True):
        '''
        Draws text in the screen
        :param shift_x: It's used to know how much it should be shifted in the horizontal axis from the orgin point of a rectangle (default 0)
        :param shift_x: It's used to know how much it should be shifted in the vertical axis from the orgin point of a rectangle (default 0)
        :param fillbfr: it fills the background, outdated paramater
        :return: Nothing
        '''
        if fillbfr == True:
            self.fill()
        self.window.blit(self.font, (self.rect.x + shift_x, self.rect.y + shift_y))

# ENTITY ____________________________________________#

class Entity(Area):
    '''
        Entity Class

        Contains Animation handling, Hitbox handling and Image Transformation 
        (animation as of image looping)
        Everything uses pygame, so it my me slow (python is already a slow language)

        class variable usage
            self.idle_image: is the idle image of the entity
            self.rotation: how many degrees should the entity turn
            self.entity_type: what is the entity type
            self.imageX: *for hitbox
            self.imageY: *for hitbox
            self.animBuffer: (it has no usage for now...)
            self.currentAnim: Current animation that is being played (used to change the current animation that is being played, instead of making a class function)
            self.AnimData: It controls when a new image should be shown to the screen, it finds that by using the int( fps/frames ) in short it's making sure that you increment the animation at the desired frames parameter
            self.AnimDict: stores every animation

    '''
    def __init__(self, window:pygame.Surface, x:float, y:float, width:float, height:float, entity_type:str, color:tuple=WHITE, animDict:dict=None, img_filename=None):
        '''
        Initializing the entity

        :param window: It is the window that you want the Entity to be drew at (pygame Surface)
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the Entity (float)
        :param height: The height of the Entity (float)
        :param entity_type: What typ of Entity is your entity (e.x. Player, Enemy, Npc etc) (string)
        :param color: The color of the Entity (tuple)
        :param animDict: The dictionary of every animation (a loop of images) that the enetity has (Dictionary, that shows the img path)
        :param img_filename: The idle image of the entity (String, that show the img path)
        '''
        Area.__init__(self, window=window,x=x, y=y, width=width, height=height)
        self.idle_image = None
        self.rotation = 0
        self.entity_type = entity_type
        self.imageX = 0                     #for hitbox
        self.imageY = 0                     #for hitbox
        self.animBuffer = 0
        self.currentAnim = ''
        self.AnimData = 0                   #declaring the variables for the animation function
        self.animDict = None
        self.animDictNewList = []
        self.animDictNameList = []

        #enabling the use of images
        if img_filename != None:
            self.idle_image = pygame.image.load(img_filename).convert() #setting the idle image 
            self.idle_image = pygame.transform.rotate(pygame.transform.scale(self.idle_image, (width,height)), self.rotation) #transforming the idle image
            self.imageX = x-self.idle_image.get_width()/2 # getting the center of the image
            self.imageY = y-self.idle_image.get_height()/2

        #enabling the use of the animations
        if animDict != None:
            if type(animDict) == dict:
                self.animDict = animDict
                self.animDictNameList = animDict.keys()
                #looping through the whole dictianary to change them into pygame images
                for i in self.animDictNameList:
                    for j in range(len(animDict[i])):
                        self.new_image = pygame.image.load(animDict[i][j]).convert()
                        self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width, self.rect.height)), self.rotation)
                        self.animDictNewList += [self.new_image]

                    self.animDict.update({i: self.animDictNewList})
                    # animation_database.update({self.entity_type: self.animDictNewList}) #check up on this later
                    self.animDictNewList = []
                    
    
    def __del__(self): #                            <- for debugging purposes (maybe could also be used for projectiles and particles?)
            print(f"object entity is deleted")

    def n_hitbox(self, hitboxWidth : float, hitboxHeight : float): #(*performnce issue)
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, wich is a Rect)
        :param hitboxWidth: The new number of the new hitbox width (either a flot or an int)
        :param hitboxHeight: The new number of the new hitbox height (either a flot or an int)
        '''
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitboxWidth, hitboxHeight
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2

    def display_idle(self,x:float=0,y:float=0):
        self.window.blit(self.idle_image, (x,y))
               
    def display_anim(self, fps : int, animName : str,  frames : int=12): #probably going to delete later 
        # self.mw.blit(pygame.image.load(self.anim[self.AnimData]),(self.rect.x,self.rect.y))     
        self.window.blit(self.animDict[animName][int(self.AnimData)],
                        (self.imageX,self.imageY))
                        
        
        #print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line
        self.AnimData += frames/fps
        if self.AnimData >= len(self.animDict[animName]):
            self.AnimData = 0

    def display_current_anim(self, fps : int, frames : int=12):
        '''
        Displaying the Current Animation that is store in the currenAnim Value (str)

        :param fps: The "wanted" fps of the game (it is advised to use get_fps function as it may not work if you have capped at 1000fps but only get 60)
        :param frames: *How many frames will the animation last

        For debugging animation use: 
        print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line
        '''
        # self.mw.blit(pygame.image.load(self.anim[self.AnimData]),(self.rect.x,self.rect.y))
        if self.currentAnim != '': 
            self.window.blit(self.animDict[self.currentAnim][int(self.AnimData)],(self.imageX,self.imageY))
        
            
            self.AnimData += frames/fps
            if self.AnimData >= len(self.animDict[self.currentAnim]):
                self.AnimData = 0
        else:
            self.window.blit(self.idle_image, (self.coreX,self.coreY))

    def flip_img(self, names : list, flip:tuple = (False,False)): #can help with animations
        '''
        Too flip images in x or y

        :param names: you can give a list on the images names to transform
        :param flip: Tuple (True,True), the 1 cell represents the x axis, and the 2 cell represents the y axis 
        :return: Nothing
        '''
        
        for name in names:
            for pic in range(len(self.animDict[name])):
                    self.animDict[name][pic] = pygame.transform.flip(self.animDict[name][pic], flip[0],flip[1])

    def transform_img(self,width : float, height : float, rotation : float, name:str or list = 'all'):
        #checking what the coder wants to change in the animations, either just one "slide" or everything or some but not all of the animations
        if name == 'all':
            for names in self.animDictNameList:
                for pic in range(len(self.animDict[names])):
                    self.animDict[names][pic] = pygame.transform.rotate(pygame.transform.scale(self.animDict[names][pic], (width, height)), float)

        elif type(name) == list:
            print("sorry i can't do that now")
            raise Exception('The programmer is too lazy to code this task')

        elif type(name) == str and name == 'selfImage':
                pygame.transform.rotate(pygame.transform.scale( self.idle_image, (width,height)), rotation)

        elif type(name) == str and len(self.animDict[name]) != 0:
            for pic in range(len(self.animDict[name])):
                self.animDict[name][pic] = pygame.transform.rotate(pygame.transform.scale( self.animDict[name][pic], (width, height)), rotation)
            pygame.transform.rotate(pygame.transform.scale( self.idle_image, (width,height)), rotation)

        self.rect.width = width
        self.rect.height = height
        self.rotation = rotation

# OBJECT ____________________________________________#

class Object(Area):
    pass

# PROJECTILE ________________________________________#

class Projectile():
    pass

# PARTICLES _________________________________________#

class Particles(Projectile):
    pass


# engine report, on the function outline, check if it is indeed right (it is i think), ti sto poutso grafeis sto display_anim?
# basic report: there are a few loops and spagheti in the code, either re-write it, or idk
#secondary roport, change the coreX or coreY and imageX and imageY system, it does nothing 
                    # proposal on chenging the system will be universal rect x and y cords but other variables are in place to calculate how far of it is from the rect.

# documantation of the algorithms

"""
area class variables uses:
    coreX is used to know the exact center of the area
        so if we want to use it for drawing the outline we will calculate where is the ouline based on the core
        which in the end is going to give us the possibility of creating our own "family system of multiple htiboxes based on one 
        core cordinate"
    functions
        outline:
            outside outline: 
                (left: float, top: float, width: float, height: float)

entity class variables:
        self.idle_image = None
        self.rotation = 0
            how much should the image rotate

        self.entity_type = entity_type
            probable use to know what type the entity is

        self.imageX = 0                     #for hitbox
        self.imageY = 0                     #for hitbox
            created to know the x and y cordinate of the image

        self.animBuffer = 0

        self.currentAnim = ''
            current Animation that is playing, it makes it easier to change the animation that is currently playing by just changing the variable to another existing 
            animation loop from the entity

        self.AnimData = 0                   #declaring the variables for the animation function
        self.animDict = None
        self.animDictNewList = []
        self.animDictNameList = []

AnimDict = dictionairy syntax 
    dict = {"animName":[list, of, the, images]}

transform_img self,width : float, height : float, rotation : float, name = 'all' 
    name can be anything from a string that is 'all', a list, a certain image name
    default is "all"
"""