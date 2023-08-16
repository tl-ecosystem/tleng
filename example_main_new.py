# from assets.scripts.Tleng2 import *
# import assets.scripts.engine.Tleng2 as TL
from assets.scripts.engine.Tleng2 import *

# from time import time
# import numpy as np
# import matplotlib.pyplot as plt


class Game(TlenGame, Settings):
    def __init__(self):
        TlenGame.__init__(self)
        Settings.__init__(self)
        
    def on_start(self):
        '''
        The init of the objects that are going to be used in game
        '''
        self.BOX = Area(self._win, 100, 100, 50, 50)

    def handle_events(self):
        '''
        the handling of basic events
        '''
        for event in pygame.event.get(): #optimazation (i think it can be written better)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
    
    def render(self):
        '''
        what the app should render, this should be better be done in a scene class that is going to inherit from TlengScene 
        '''
        self._win.fill(BLACK)
        self.BOX.render()
        self._clock.tick(self._fps)
        pygame.display.update()

    def update(self):
        self.BOX.coreX += 0.5 
        self.BOX.update()

if __name__ == "__main__":
    game = Game()
    game.on_start()
    game.run()