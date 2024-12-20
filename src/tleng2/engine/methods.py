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

from .properties import EngineProperties, SceneManagerProperties, RendererProperties
from .settings import GlobalSettings

class EngineMethods:
    """
    A namespace of abstractions made over functions in pygame.

    You can, if you want, to write these functions in your own code as there is a possible speedup.
    But generally this exists to not think to much when writing your game.

    Compatible methods with ECS implementation:
    - `set_caption(caption: str) -> None`
    - `set_icon(image_path: str) -> None`
    - `set_icon_surface(image: pygame.SurfaceType) -> None`
    """

    @staticmethod
    def set_caption(caption: str) -> None:
        pygame.display.set_caption(caption)


    @staticmethod
    def set_icon(image_path: str) -> None:
        """
        Pass as a parameter the location of the icon you want to use.
        """
        pygame.display.set_icon(pygame.image.load(image_path).convert_alpha())
    

    @staticmethod
    def set_icon_surface(image: pygame.SurfaceType) -> None:
        """
        Pass a specific surface you want to use.
        """
        pygame.display.set_icon(image)

    
    @staticmethod
    def clock_tick_dt(target_fps: int) -> float:
        return EngineProperties._clock.tick(target_fps) / 1000
        # return 1 # for debugging purposes
    

    @staticmethod
    def clock_tick_EP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) / 1000


    @staticmethod
    def lazy_clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties. Micro optimization.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) >> 10 # bit shift, clock.tick // 1024
    


class SceneManagerMethods:
    """
    SceneManager Static methods that might be needed across the base game.
    """
    @staticmethod
    def start_with_scene(scene_name: str) -> None:
        """
        Declares the default scene.
        """
        
        SceneManagerProperties._current_scene = scene_name
        
        params = RendererProperties.type_parameters[RendererProperties.scene_parameters[SceneManagerProperties._current_scene]]
        RendererProperties._display = params['display']
        RendererProperties._local_default_camera = params['camera']
        

    @staticmethod
    def change_current_scene(new_scene: str) -> None:
        """
        Changes the value of the SceneManager in tleng2/core_engine/scene_manager.py
        """
        
        SceneManagerProperties._waiting_scene = new_scene
        SceneManagerProperties._changing_scenes = True


    @staticmethod
    def update_scene():
        if SceneManagerProperties._changing_scenes:
            SceneManagerProperties._current_scene = SceneManagerProperties._waiting_scene
            
            params = RendererProperties.type_parameters[RendererProperties.scene_parameters[SceneManagerProperties._current_scene]]
            RendererProperties._display = params['display']
            RendererProperties._local_default_camera = params['camera']
            
            SceneManagerProperties._changing_scenes = False


class RendererMethods:
    """
    Renderer Static methods that might be needed across the base game.
    """

    @staticmethod
    def import_scene_renderer_params(params_key: str, params: dict) -> None:
        RendererProperties.type_parameters.update({params_key: params})

    
    @staticmethod
    def import_scene_renderer_params_dict(params: dict) -> None:
        params_keys = params.keys()
        for key in params_keys:
            RendererProperties.type_parameters.update({key: params[key]})


    @staticmethod
    def clear_render_calls() -> None:
        RendererProperties.render_calls = []


    @staticmethod
    def load_displays(flags: int = 0) -> None:
        """
        Initialize the display fast.
        """
        RendererProperties._default_display = pygame.Surface(GlobalSettings._disp_res) 
        RendererProperties._window = pygame.display.set_mode(GlobalSettings._win_res, flags = flags)
        RendererProperties.type_parameters.update(
            {'default': 
                {
                    'display' : RendererProperties._default_display.copy(),
                    'camera' : None 
                }
            }
        )


    @staticmethod
    def load_local_display(width, height) -> pygame.SurfaceType:
        ...


    @staticmethod
    def load_local_display_ratio(ratio) -> pygame.SurfaceType:
        return pygame.Surface((GlobalSettings._win_res[0]*ratio, GlobalSettings._win_res[1]*ratio)) 


    @staticmethod
    def lazy_upscale_display(new_res: tuple[int,int] = GlobalSettings._win_res) -> None:
        """
        Scaling the display to the size of the window.
        And updates the window with the upscale.
        Warning may be pixelated.
        """
        __temp_disp = pygame.transform.scale(EngineProperties._display, new_res)
        EngineProperties._window.blit(__temp_disp, (0, 0))


    @staticmethod
    def update_window() -> None:
        """
        UpScales or DownScales the display to fit the window. 
        Warning, this might strecth the render. 
        """
        
        RendererProperties._window.blit(pygame.transform.scale(RendererProperties._display, RendererProperties._window.get_size()),(0,0))


    @staticmethod
    def update_window_exp(display: pygame.SurfaceType) -> None:
        """
        UpScales or DownScales the display to fit the window. 
        Warning, this might stretch the render. 
        """
        temp_disp = display if display != None else RendererProperties._display
        RendererProperties._window.blit(pygame.transform.scale(temp_disp, RendererProperties._window),(0,0))


    @staticmethod
    def update_window_disp() -> None:
        """
        Updates the window from _display immedietely. Faster than `RendererMethods.update_window()`
        """
        RendererProperties._window.blit(RendererProperties._display, (0, 0))


    @staticmethod
    def fill_display(color: tuple[int, int, int]) -> None:
        """
        Fill the display with color.
        """
        RendererProperties._display.fill(color)


    @staticmethod
    def load_window(
            flags: int = 0,
            depth: int = 0,
            display: int = 0,
            vsync: int = 0
        ) -> None:
        """
        Initialize the window, with added parameters.
        """
        EngineProperties._window = pygame.display.set_mode(GlobalSettings._win_res, flags, depth, display, vsync)


    @staticmethod
    def load_display(): #TODO
        EngineProperties._display = pygame.display.set_mode(GlobalSettings._disp_res)
