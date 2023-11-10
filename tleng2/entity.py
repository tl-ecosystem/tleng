from .engine.area import *


class Entity(Area):
    '''
        Entity Class

        Contains Animation handling, Hitbox handling and simple Image Transformation 
        (animation as of image looping)
        Everything uses pygame, so it may be slow (python is already a slow language)

        class variable usage
            self.idle_image: is the idle image of the entity
            self.rotation: how many degrees should the entity turn
            self.entity_type: what is the entity type (used to see e.x. if the collided entity is an enemy or an NPC)
            self.imageX: *for image float position
            self.imageY: *for image float position
            self.animBuffer: (it has no usage for now...)
            self.currentAnim: Current animation that is being played (used to change the current animation that is being played, instead of making a class function)
            self.AnimData: It controls when a new image should be shown to the screen, it finds that by using the int( fps/frames ) 
                in short it's making sure that you increment the animation at the desired frames parameter 
                (e.x.: 60/12=5, every frame its going to be incremented by 5, if it is more that 12
                then the next image of the animation will play and animData will reset)
            self.AnimDict: stores every animation the entity
            self.animDictNewList: Only used once at the initialization of the entity, it stores the newly converted images and then puts them back to the self.AnimDict
            self.animDictNameList: Only used once at the initialization of the entity, it stores the names (keys) of the animations, used to converted them one by one on the loop. 
            self.directions: Used for storing the 2-dimensional vector for the class Entity (expirimental value)

    '''
    def __init__(self, window:pygame.Surface, x:int|float, y:int|float,  width:int|float, height:int|float, entity_type:str, color:tuple=WHITE, animDict:dict=None, img_filename:str=None)->None:
        '''
        Initializing the entity

        :param window: It is the window that you want the Entity to be drew at (pygame Surface)
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the Entity (float)
        :param height: The height of the Entity (float)
        :param entity_type: What type of Entity is your entity (e.x. Player, Enemy, Npc etc) (Can be used to see if the colliding entity is an enemy) (string)
        :param color: The color of the Entity (tuple)
        :param animDict: The dictionary of every animation (a loop of images) that the enetity has (Dictionary, that shows the img path)
        :param img_filename: The idle image of the entity (String, that show the img path)
        '''
        Area.__init__(self, window=window,x=x, y=y, width=width, height=height)
        self.idle_image = None
        self.rotation = 0
        self.entity_type = entity_type
        self.imageX = 0                     #for image, for hitbox it's the coreX
        self.imageY = 0                     #for image, for hitbox it's the coreY
        #declaring the variables for the animation function                     
        self.animBuffer = 0
        self.currentAnim = ''
        self.AnimData = 0                   
        self.animDict = None
        self.animDictNewList = []
        self.animDictNameList = []
        #experimental variables
        self.directions = pygame.math.Vector2()

        #enabling the use of images
        if img_filename != None:
            self.idle_image = pygame.image.load(img_filename).convert_alpha() #setting the idle image 
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
                        self.new_image = pygame.image.load(animDict[i][j]).convert_alpha()
                        self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width, self.rect.height)), self.rotation)
                        self.animDictNewList += [self.new_image]

                    self.animDict.update({i: self.animDictNewList}) #updating the entitys animation dict
                    self.animDictNewList = [] #resseting the NEW animation list

                    # animation_database.update({self.entity_type: self.animDictNewList}) # TODO: check up on this later
                    
    
    def __del__(self): #                            <- for debugging purposes (maybe could also be used for projectiles and particles?)
            print(f"object entity is deleted")


    def n_hitbox(self, hitboxWidth : float, hitboxHeight : float) -> None: # TODO : hitbox/coordination system
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, wich is a Rect)
        :param hitboxWidth: The new number of the new hitbox width (either a flot or an int)
        :param hitboxHeight: The new number of the new hitbox height (either a flot or an int)
        :return: it returns nothing
        '''
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitboxWidth, hitboxHeight
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2


    def display_idle(self,x:float=0,y:float=0) -> None: # TODO : hitbox/coordination system
        '''
        Displays ONLY the idle image that was given on init of the class (TODO: make the function a bit more safe to use, also make the x and y values to be shifted)

        :param x: The X coordinate of this idle image
        :param y: The y coordinate of this idle image
        :return: it returns nothing
        '''
        self.window.blit(self.idle_image, (x,y))


    def draw_anim(self, fps : int, animName : str,  frames : int = 12) -> None: #probably going to delete later, same principles as the function displat_current_anim 
        # TODO : hitbox/coordination system
        # self.mw.blit(pygame.image.load(self.anim[self.AnimData]),(self.rect.x,self.rect.y))     # <------- old implemantation of displaying stuff to the screen
        self.window.blit(self.animDict[animName][int(self.AnimData)],
                        (self.imageX,self.imageY))
                        
        
        #print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line
        self.AnimData += frames/fps
        if self.AnimData >= len(self.animDict[animName]):
            self.AnimData = 0


    def draw_current_anim(self, target_fps : float, fps : float, frames : int = 12) -> None:
        # TODO : hitbox/coordination system
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


    def flip_img(self, names : list, flip:tuple = (False,False)) -> None: #can help with animations
        # TODO : hitbox/coordination system
        '''
        Too flip images in x or y

        :param names: you can give a list on the images names to transform
        :param flip: Tuple (True,True), the 1 cell represents the x axis, and the 2 cell represents the y axis 
        :return: it returns nothing
        '''
        
        for name in names:
            for pic in range(len(self.animDict[name])):
                    self.animDict[name][pic] = pygame.transform.flip(self.animDict[name][pic], flip[0],flip[1])


    def transform_img(self,width : float, height : float, rotation : float, name:str or list = 'all') -> None:
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


    def update(self,current_anim, target_fps):
        '''
        Experimental Feature of Entity in Tleng2

        It updates everything without the need of the programmer to type out every function of the entity.

        '''
        self.currentAnim = current_anim
        self.display_current_anim(target_fps=target_fps,)
        self.rect.x, self.rect.y = self.imageX, self.imageY
