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

import pygame
from pygame import Vector2

from .settings import GlobalSettings
from .properties import RendererProperties, SceneManagerProperties
from ..components.camera import CameraCatcher
from ..utils.debug import debug_print
from ..utils.subpixel import SubPixelSurface


class Renderer:
    """
    Experimental Renderer
    """
    def __init__(self) -> None:
        self._display = None
        self._window = None


    def render(self) -> None:
        # debug_print(RendererProperties.render_calls,tags=['Renderer', 'Render_calls'])
        display = RendererProperties._display
        
        temp_vec = Vector2(0,0)

        for call in RendererProperties.render_calls:
            renderable = call
            
            
            debug_print(renderable, tags=["Renderer"])

            if RendererProperties._local_default_camera != None:
                temp_vec.x = 0
                temp_vec.y = 0

                pos = CameraCatcher.cameras[RendererProperties._local_default_camera].offset_pos
                debug_print(pos, tags=["Renderer"])

                temp_vec = pos - renderable.pos

                display.blit(renderable.surface, (round(renderable.x + pos.x), round(renderable.y + pos.y - temp_vec.y*2)))
            else:
                display.blit(renderable.surface, (renderable.x , renderable.y))
        
        debug_print(CameraCatcher.cameras, tags=["Renderer", "Camera"])
        
 

# reference only
class Renderer_dep:
    """
    Depracated renderer
    """
    layers = []
    layers_order = None
    camera = None
    target_surf = None # defalut is Renderer._dis
    _display = None
    _window = None


    @staticmethod
    def pass_scene_parameters() -> None:
        ...


    @staticmethod
    def add_layer(
            width: int | None = None,
            height: int | None = None
        ) -> None:
        """
        Either you input the width and the height, or leave it blank.
        """
        if width == None and height == None:
            Renderer.layers += [pygame.Surface(GlobalSettings._disp_res)]
        else:
            Renderer.layers += [pygame.Surface((width, height))]


    @staticmethod
    def add_layers(
            layers: list[pygame.SurfaceType]
        ) -> None:
        """
        Adds multiple layers at once.
        """
        Renderer.layers += layers


    @staticmethod
    def change_layers_order() -> None: ...


    @staticmethod
    def render_surface(
            object: pygame.Surface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area: pygame.Rect = None,
            special_flags: int = 0,
            layer_key: str = None,
            camera: str = None
        ) -> None:

        Renderer.rect.x, Renderer.rect.y = Renderer.offset_pos[0], Renderer.offset_pos[1]
        
        if area != None:
            Renderer._display.blit(object,
                               (game_pos[0]-Renderer.offset_pos[0], 
                                game_pos[1]-Renderer.offset_pos[1]),
                                area,
                                special_flags=special_flags
                              )
        else:
            Renderer._display.blit(object,
                               (game_pos[0], 
                                game_pos[1]),
                                Renderer.rect,
                                special_flags=special_flags
                              )
        # Renderer.draw_rect((255,0,0),Renderer.rect,5) # debug

    @staticmethod
    def render_sub_exp(
            object: SubPixelSurface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area: pygame.Rect = None,
            special_flags: int = 0 
        ) -> None:
        """
        experimental renderer
        """
        Renderer.rect.x, Renderer.rect.y = Renderer.offset_pos[0], Renderer.offset_pos[1]

        # GlobalSettings._display.blit(object,
        #                              (game_pos[0]-Renderer.offset_pos[0], 
        #                               game_pos[1]-Renderer.offset_pos[1]),
        #                               area,
        #                               special_flags=special_flags
        #                             )
        Renderer._display.blit(object.at(game_pos[0], game_pos[1]),
                                     (game_pos[0], 
                                      game_pos[1]),
                                      Renderer.rect,
                                      special_flags=special_flags
                                    )

    @staticmethod
    def draw_rect(
            color: tuple[int,int,int],
            rect: pygame.Rect,
            width: int,
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1,
        ) -> None:
        '''
        Renders the rectangle into the window, with the camera offset.
        '''
        dummy_rect = rect.copy()
        dummy_rect.x -= int(Renderer.offset_pos[0])
        dummy_rect.y -= int(Renderer.offset_pos[1])
        pygame.draw.rect(Renderer._display, 
                        color,
                        dummy_rect,
                        width,
                        border_radius,
                        border_top_left_radius,
                        border_top_right_radius,
                        border_bottom_left_radius,
                        border_bottom_right_radius)

    @staticmethod
    def render_tiles( layer, camera) -> None:
        """
        It will render every single tile in the level that is provided.
        """
        if Renderer.layers == []:
            ...
        else:
            # usage of layer
            ...

    @staticmethod
    def lazy_render_tiles(layer, camera) -> None:
        """
        Will only render where the camera is hovering at from the chunks that are provided (Even if it is rotated).
        """
        # Require the tilemap to be broken up into chunks
