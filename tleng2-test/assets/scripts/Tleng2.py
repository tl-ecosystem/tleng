import pygame, os, math
from time import sleep,time
pygame.font.init()
pygame.mixer.init()

# engine report, on the function outline, check if it is indeed right (it is i think)
# basic report: there are a few loops and spagheti in the code, either re-write it, or they are probably alright
# secondary roport, change the coreX or coreY it does nothing 
# TODO: proposal on changing the system will be universal rect x and y cords but other variables are in place to calculate how far of it is from the rect.


# TODO do every todo you have

'''
TLeng2.py a python 2d game engine

Current version is v2.0

Documentation Update

'''

# _____________________________________________________ COLORS THAT I NEEDED THUS FAR  (RGB: RED, GREEN, BLUE)______________________________________________________

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

# TODO: i don't know what to do with this
global animation_database
animation_database = {}

# AREA ______________________________________________#

class Area():
    '''
    Class for area, acts as a static box, also used for "static" hitboxes

    Class variables:
        self.rect: the rectangle class from pygame
        self.coreX: the core x coordinate of the rect (it doesn't store the top left coordinate) #TODO: there is no use for this variable
        self.coreY: the core y coordinta of the rect (it doesn't store the top left coordinate) #TODO: there is no use for this variable
        self.coredWidth: the width of the rectangle
        self.coreHeight: the height of the rectangle
        self.window: the window that the rectangle can be drawn at
        self.color: the color of the rectangle
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
        self.rect = pygame.Rect(float(x-width/2), float(y-height/2), width, height)
        self.coreX = x
        self.coreY = y
        self.coreWidth = width
        self.coreHeight = height
        self.window = window
        self.color = color  
          
    def draw_Area(self):
        '''
        Draws the area in the screen
        '''
        pygame.draw.rect(self.window, self.color, self.rect)

    def outline_Area(self, thic=1, frame_color=BLACK):
        '''
        It draws the outline of the area by creating another rect object
        
        :param thic: it's the thickness of the Area's outline, if it is more than 
        :param frame_color: Specifes the color of the area's outline
        :return: it returns nothing
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
    Label is a class for displaying text.
    '''
    def set_Label(self, text, tsize=12, tcolor=BLACK, tbold=False):
        '''
        Storing the text class in a variable for later usage, The Label is created by using a rectangle 
        To draw the text use drawText

        :param text: Type the text you want to store
        :param tsize: It's the desired size for your text (default size 12)
        :param tcolor: It's the desired color for your text (default color BLACK)
        :param tbold: If you want for your text to be bold set it to True (default to False)
        :return: it returns nothing
        '''

        self.font = pygame.font.SysFont('verdana', tsize, tbold).render(text, True, tcolor)
        self.height = pygame.font.SysFont('verdana', tsize, tbold).render(text, True, tcolor).get_height()

    def draw_Label(self, shift_x=0, shift_y=0,fillbfr=False):
        '''
        Draws text in the screen

        :param shift_x: It's used to know how much it should be shifted in the horizontal axis from the orgin point of a rectangle (default 0)
        :param shift_x: It's used to know how much it should be shifted in the vertical axis from the orgin point of a rectangle (default 0)
        :param fillbfr: it fills the background, outdated paramater
        :return: it returns nothing
        '''
        if fillbfr == True:
            self.fill()
        self.window.blit(self.font , (self.rect.x + shift_x, self.rect.y + shift_y))

# ENTITY ____________________________________________#

class Entity(Area):
    '''
        Entity Class

        Contains Animation handling, Hitbox handling and Image Transformation 
        (animation as of image looping)
        Everything uses pygame, so it may be slow (python is already a slow language)

        class variable usage
            self.idle_image: is the idle image of the entity
            self.rotation: how many degrees should the entity turn
            self.entity_type: what is the entity type
            self.imageX: *for hitbox
            self.imageY: *for hitbox
            self.animBuffer: (it has no usage for now...)
            self.currentAnim: Current animation that is being played (used to change the current animation that is being played, instead of making a class function)
            self.AnimData: It controls when a new image should be shown to the screen, it finds that by using the int( fps/frames ) 
                in short it's making sure that you increment the animation at the desired frames parameter 
                (e.x.: 60/12=5, every frame its goint to be incremented by 5, if it is more that 12
                then the next image of the animation will play and animData will reset)
            self.AnimDict: stores every animation the entity
            self.animDictNewList: Only used once at the initialization of the entity, it stores the newly converted images and then puts them back to the self.AnimDict
            self.animDictNameList: Only used once at the initialization of the entity, it stores the names (keys) of the animations, used to converted them one by one on the loop. 
            self.directions: Used for storing the 2-dimensional vector for the class Entity (expirimental value)

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
        #experimental variables
        self.directions = pygame.math.Vector2()

        #enabling the use of images
        if img_filename != None:
            self.idle_image = pygame.image.load(img_filename).convert() #setting the idle image 
            self.idle_image = pygame.transform.rotate(pygame.transform.scale(self.idle_image, (width,height)), self.rotation) #transforming the idle image
            self.imageX = self.idle_image.get_width() 
            self.imageY = self.idle_image.get_height()
            self.imageX = self.rect.x
            self.imageY = self.rect.y
            # self.imageX = x-self.idle_image.get_width()/2 # getting the center of the image
            # self.imageY = y-self.idle_image.get_height()/2

        #enabling the use of the animations
        if animDict != None: #if there are animations enable them
            if type(animDict) == dict:
                self.animDict = animDict
                self.animDictNameList = animDict.keys()
                #looping through the whole dictianary to change them into pygame images
                for i in self.animDictNameList:
                    for j in range(len(animDict[i])):
                        self.new_image = pygame.image.load(animDict[i][j]).convert()
                        self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width, self.rect.height)), self.rotation)
                        self.animDictNewList += [self.new_image]

                    self.animDict.update({i: self.animDictNewList}) #updating the entitys animation dict
                    self.animDictNewList = [] #resseting the NEW animation list

                    # animation_database.update({self.entity_type: self.animDictNewList}) # TODO: check up on this later
                    
    
    def __del__(self): #                            <- for debugging purposes (maybe could also be used for projectiles and particles?)
            print(f"object entity is deleted")

    def n_hitbox(self, hitboxWidth : float, hitboxHeight : float): #(*performnce issue)
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, wich is a Rect)
        :param hitboxWidth: The new number of the new hitbox width (either a flot or an int)
        :param hitboxHeight: The new number of the new hitbox height (either a flot or an int)
        :return: it returns nothing
        '''
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitboxWidth, hitboxHeight
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2

    def display_idle(self,x:float=0,y:float=0):
        '''
        Displays ONLY the idle image that was given on init of the class (TODO: make the function a bit more safe to use, also make the x and y values to be shifted)

        :param x: The X coordinate of this idle image
        :param y: The y coordinate of this idle image
        :return: it returns nothing
        '''
        self.window.blit(self.idle_image, (x,y))
               
    def display_anim(self, fps : int, animName : str,  frames : int=12): #probably going to delete later, same principles as the function displat_current_anim
        # self.mw.blit(pygame.image.load(self.anim[self.AnimData]),(self.rect.x,self.rect.y))     # <------- old implemantation of displaying stuff to the screen
        self.window.blit(self.animDict[animName][int(self.AnimData)],
                        (self.imageX,self.imageY))
                        
        
        #print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line
        self.AnimData += frames/fps
        if self.AnimData >= len(self.animDict[animName]):
            self.AnimData = 0

    def display_current_anim(self, target_fps : float, fps : float, frames : int=12 ):
        '''
        Displaying the Current Animation that is store in the currenAnim Value (str)

        :param target_fps: These are the targeted fps, it is useful in case the current fps are 0, then we will use the target_fps
        :param fps: The "wanted" fps of the game (it is advised to use get_fps function as it may not work if you have capped at 1000fps but only get 60)
        :param frames: *How many frames will the animation last
        :return: it returns nothing

        For debugging animation use: 
        print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line
        '''
        if self.currentAnim != '': 
            self.window.blit(self.animDict[self.currentAnim][int(self.AnimData)],(self.imageX,self.imageY))

            #(e.x.: 12/60=0.2, every frame its going to be incremented by 0.2, if it is more than the lenght of the animation (4)
            #    then the next image of the animation will play and animData will reset)

            if fps > 0:
                self.AnimData += frames/fps
            else:
                self.AnimData += frames/target_fps #just in case the fps hit 0

            if self.AnimData >= len(self.animDict[self.currentAnim]):
                self.AnimData = 0
        else:
            self.window.blit(self.idle_image, (self.imageX,self.imageY))
        
        #TODO: Experimental: use of imageX/imageY in animation
        self.rect.x, self.rect.y = self.imageX, self.imageY

    def flip_img(self, names : list, flip:tuple = (False,False)): #can help with animations
        '''
        Too flip images in x or y

        :param names: you can give a list on the images names to transform
        :param flip: Tuple (True,True), the 1 cell represents the x axis, and the 2 cell represents the y axis 
        :return: it returns nothing
        '''
        
        for name in names:
            for pic in range(len(self.animDict[name])):
                    self.animDict[name][pic] = pygame.transform.flip(self.animDict[name][pic], flip[0],flip[1])

    def transform_img(self,width : float, height : float, rotation : float, name:str or list = 'all'):
        '''
        Transform the images, change width, height, rotation for the given amount of images (list, a list from the dictionary or the whole dictionary)
        Recomended to use this function only if you want to transform images by bulk, if you want just one type it directly.

        :param width:
        :param height:
        :param rotation:
        :name: str or list, is the name of the files that you want to cahnge, can either be an str or a whole list. 
            Str can be either the keywork "all" meaning it's going to change every animation in the dictionary
            it can also be a specific key on the dictionary of the animations.
            Another specific keyword is "selfImage" which only transforms the self.idle_image of the entity TODO: make this part of the code safe
            List can be a direct transformation of the images in the list (not yet implemented TODO: implement that) 
        '''
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

    # TODO experimental features ________________________#
    def update(self,current_anim, target_fps):
        '''
        Experimental Feature of Entity in Tleng2
        
        It updates everything without the need of the programmer to type out every function of the entity.

        '''
        self.currentAnim = current_anim
        self.display_current_anim(target_fps=target_fps,)
        self.rect.x, self.rect.y = self.imageX, self.imageY
    
    def debug(self, window:pygame.Surface, info:list): # TODO Make it into a Class
        '''
        Experimental Feature of Entity in Tleng2
        
        You can input a list and it will output, if there is a \n like ,"\n", it will output in a new line underneath
        
        WARNING: It sucks performnance like crazy
        WARNING: it doesn't dynamically change lines if it goes out of the screen
        WARNING: Due to it's text attribute in later updates part of it will be moved to the class Label (TODO), and it's own debug class 
        '''
        self.debug_text = []
        last_nl = -1 # last new line 
        list_index = 0
        if type(info) == list:
            for i in range(len(info)):
                if info[i] == '\n':
                    self.debug_text += [Label(window, self.rect.x, self.rect.y, 10, 10)]
                    self.debug_text[list_index].set_Label(str(info[last_nl+1:i]),tcolor=WHITE)
                    last_nl = i
                    list_index +=1

                elif i == len(info) - 1:
                    self.debug_text += [Label(window, self.rect.x, self.rect.y, 10, 10)]
                    self.debug_text[list_index].set_Label(str(info[last_nl+1:i+1]),tcolor=WHITE)

        for i in range(len(self.debug_text)):
            self.debug_text[i].draw_Label(self.rect.width, self.rect.height + i*self.debug_text[0].height, False)
        


# OBJECT ____________________________________________#

class Object(Area):
    pass

# PROJECTILE ________________________________________#

class Projectile():
    pass

# PARTICLES _________________________________________#

class Particles(Projectile):
    pass

# DEBUG _____________________________________________ # TODO: Finish this class

class Debug():
    pass

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

def load_image(img_filepath):
    '''
    Loading an image

    :param img_filename: the file path of the image
    :return: It returns the loaded image (uses convert to make the game more efficient)
    '''
    return pygame.image.load(img_filepath).convert()

def entity_xy_cords(entity : Entity, ): # TODO: do this or delete it
    '''
    Returns the X and Y coordinate of the entity
 
    '''

