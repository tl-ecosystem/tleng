import os
import pygame

print(type(os.path.join('assets','art')))
animdict = {}

# key = input("what is the name of your list \n")
# list = []

# while True:
#     s = input("type what the list has - type 0 to exit \n")
#     if s == '0':
#         break
#     else:
#         list += [s]

# animdict.update({key:list}) 
# print(animdict[key][1])
# print(animdict)

image = pygame.image.load(os.path.join('assets','art','pictures','walkingman1.png'))

image =pygame.transform.scale( image, (100, 80))

print(image.get_height(),image.get_width())
                    
WIDTH, HEIGTH = 500, 700
WIN = pygame.display.set_mode((WIDTH,HEIGTH))
WIN.fill((0,0,0))

width, height = 10,10
x, y = 0,0

box = pygame.Rect(x-width/2,y-height/2,width,height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()


    pygame.draw.rect(WIN, (255,255,255), box)
    pygame.display.update()

# do nor delete, might need later ________________________________________________________________________________________________________________________________________________

    # def animation(self, nameAnim, listAnim):
    #     if len(listAnim) >=1 and type(listAnim) is list:
    #         for i in range(len(listAnim)):
    #             #loading each animation frame
    #             self.new_image = pygame.image.load(listAnim[i]).convert()
    #             self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width,self.rect.height)), self.rotation)
    #             self.animDictNewList += [self.new_image]
    #         self.animDict.update({nameAnim: self.animDictNewList})
    #         self.animDictNewList = []
    #         self.animDictNameList += [nameAnim]
    #         # print(self.animDict)                                                #<----- Debug Line
    #     else:
    #         raise Exception("ListAnim is not a list, it needs to be a list")

# MAN.animation('Walking_Left',[
#     os.path.join('assets','art','pictures','walkingman1.png'),
#     os.path.join('assets','art','pictures','walkingman2.png'),
#     os.path.join('assets','art','pictures','walkingman3.png'),
#     os.path.join('assets','art','pictures','walkingman4.png')]
# )
# MAN.animation('Jumping',[
#     os.path.join('assets','art','pictures','jumping1.png'),
#     os.path.join('assets','art','pictures','jumping2.png'),
#     os.path.join('assets','art','pictures','jumping3.png'),
#     os.path.join('assets','art','pictures','jumping4.png')]
# )



