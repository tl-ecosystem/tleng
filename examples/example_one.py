# Copyright (c) 2023 Theolaos

# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to 
# whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the 
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from tleng2 import *
from tleng2.utils.colors import *
import pygame 
import os

W_WIDTH, W_HEIGHT = 1280,720
SPEED = 4

GlobalSettings.update_bresolution((W_WIDTH, W_HEIGHT))
RendererMethods.load_displays()
EngineMethods.set_caption("Example One Of Tleng2")

GlobalSettings._debug = False

class ExampleSceneOne(Scene):
    def __init__(self, scene_name) -> None:
        super().__init__(scene_name)
        image_assets_dir = os.path.join(get_parent_dir(__file__, 2), 'assets/images')

        self.zero_vector = pygame.math.Vector2(0,0)

        self.player_vector = pygame.math.Vector2(0,0)

        self.player_sprite = LazyAnimationService()
        self.player_sprite.scale_animation(70, 70)
        self.player_sprite.load_animation(anim_db={
            "WalkingLeft": {
                "anim" : [
                    os.path.join(image_assets_dir, 'walking', 'walkingman1.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman2.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman3.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman4.png')
                    ],
                "anim_fps" : 12
            },
            "WalkingRight": {
                "anim" : [
                    os.path.join(image_assets_dir, 'walking', 'walkingman1.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman2.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman3.png'),
                    os.path.join(image_assets_dir, 'walking', 'walkingman4.png')
                    ],
                "anim_fps" : 12
            },
            "Standing" : {
                "anim" : [
                    os.path.join(image_assets_dir, 'standingman.png')
                ],
                "anim_fps" : 1
            }
        },
        alpha_conversion=True)
        self.player_sprite.flip_animation(True, False, "WalkingRight")

        self.player_sprite.current_anim = "WalkingRight"
        self.player_sprite.set_colorkey_animation((255,255,255))

    
    def event_handling(self, keys_pressed) -> None:
        self.player_vector.x = 0
        self.player_vector.y = 0
        if keys_pressed[pygame.K_w] and self.player_sprite.rect.y > 0 :
            self.player_vector.y = -1
        if keys_pressed[pygame.K_s] and self.player_sprite.rect.y < W_HEIGHT - self.player_sprite.rect.height:
            self.player_vector.y = 1
        if keys_pressed[pygame.K_a] and self.player_sprite.rect.x > 0:
            self.player_vector.x = -1
            self.player_sprite.change_current_animation('WalkingLeft')
        if keys_pressed[pygame.K_d] and self.player_sprite.rect.x < W_WIDTH - self.player_sprite.rect.width:
            self.player_vector.x = 1
            self.player_sprite.change_current_animation('WalkingRight')

        if self.player_vector != self.zero_vector:
            self.player_sprite.rect.center += self.player_vector.normalize() * SPEED
            # print(self.player_vector.length())
        else:
            self.player_sprite.change_current_animation('Standing')
    
    
    def update(self) -> None:
        self.player_sprite.update()
    
    
    def render(self) -> None:
        RendererMethods.fill_display(color=(TLENG2_BLUE))
        self.player_sprite.render()


def main():
    game = App()
    example_scene_one = ExampleSceneOne("Example")
    SceneManagerMethods.start_with_scene("Example")
    game.run_old()


if __name__ == "__main__":
    main()