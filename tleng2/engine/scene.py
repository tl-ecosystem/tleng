'''
Scene handler
It justs puts the stuff on the screen and it handles the <scene changes> like menu->game->pause screen etc.
'''
import pygame
from abc import ABC, abstractmethod
#import pygame

"""
Idea:
SceneHandler will get layers, that the dev can assign multiple scenes to play.
Scene will just handle the updates of the objects that it draws. After they were updated and drawn to the buffer screen then they will be flipped and start again onto the next frame.
Scene should also change the scene state when neceasery.

SceneHandler should recognise the state of the app for the right scene to play.

Pseudo code:

scene_dict = menu : menu_scene, game : game_scene  ...
game_state = menu

gameloop
    scene_phase(game_state)
    clock.tick(fps)
    buffer.flip()

fn scene_phase:
    sceneloop
        events()
        update()
        render()


"""

from abc import ABC, abstractmethod

class SceneCatcher:
    scenes = {}

    def __init__(self, scene_key):
        self.scenes.update({scene_key:[self]})


class Scene(SceneCatcher, ABC):
    def __init__(self,scene_name)-> None:
        SceneCatcher.__init__(self,scene_key=scene_name)
        self.scene_name = scene_name

    @abstractmethod
    def event_handling(self):
        '''
        To handle the events of mouse and other
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''

    @abstractmethod
    def update(self):
        '''
        game logic
        '''

    @abstractmethod
    def render(self):
        '''
        what to render to the screen
        '''


class SceneManager:
    def __init__(self, ) -> None: 
        """
        :param scenes: The dictionary should have Scene classes, or classes that have the structure of a scene class.
        :return: None
        """
        self.scenes = None
        self.current_scene = ''
        self.layers = []

    def return_scene_phase(self, key:str) -> Scene:
        """
        Returns the entire scene class.
        :param key: Must be a string
        :return: Scene Class
        """
        return self.scenes[key]
    

    def load_scenes(self, scenes: dict[str,Scene]) -> None:
        self.scenes = scenes
    

    def render_current_scene(self) -> None:
        try:
            for scene in SceneCatcher.scenes[self.current_scene]:
                scene.update_stuff()
                scene.render_stuff()
        except: 
            for scene in self.scenes[self.current_scene]:
                scene.event_handling()
                scene.update_stuff()
                scene.render_stuff()
# the general idea that the scene can be controlled by the scene itself is kinda stupid.


# Scene grouping?
# Dictionary of scenes that upon render will be rendered the "current_scene, just like the animation"
# the whole idea is that the original scene is going to be created in another class, which will be stored here so the engine knows what to run.