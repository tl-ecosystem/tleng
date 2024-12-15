import json
import warnings

from os import path, getcwd
from abc import abstractmethod, ABC
# from .debug import debug_print

debug_tags = ['JSON_debug']


class GlobalSettings:
    """
    Global settings, used across the game.
    Can be overwritten with the LocalSettings class.
    """

    # _platform = 'pc' # on what platform is the game for, if for mobile then the display should be changed
    _win_res = (1280, 720)
    _disp_res = (1280, 720)
    _display_scaling = 1
    _scalable_window = False
    _display_ratio_lock = True #if the game only supports 500x500 then the window will ony scale to that ratio (1:1)
    _fps = 60
    _physics_target_fps = 60 # for dt dependant values (delta-time)

    _debug = False

    _jsettings = {}

    @staticmethod
    def update_bresolution(new_res:tuple[int,int]) -> None:
        """
        Updates the variable of the resolution of *both* the window, and the display.
        It doesn't update the surfaces themselves.
        """
        warnings.warn(
                "DEPRECATION WARNING: update_bresolution will be depracated in >v2.2.1 " 
                "please change to update_resolutions()",
                FutureWarning,
                stacklevel=2
            )
        GlobalSettings._win_res = new_res
        GlobalSettings._disp_res = new_res


    @staticmethod
    def update_resolutions(new_window_res: tuple[int, int], new_display_res: tuple[int, int] = None) -> None:
        """
        It updates the global variables that store the resolution of the Window and the Display (Canvas for pixel art).

        If you pass only a resolution for the Window, then the Window and the Wisplay resolution will get updated with the resolution you passed.
        But if you pass resolutions for the Window and the Display then they will get updated respectively.  

        It doesn't update the surfaces themselves.
        """
        GlobalSettings._win_res = new_window_res
        if new_display_res:
            print('yea')
            GlobalSettings._disp_res = new_display_res
        else:
            print('noo')
            GlobalSettings._disp_res = new_window_res


    @staticmethod
    def update_resolution(new_res:tuple[int,int]) -> None:
        warnings.warn(
                "DEPRECATION WARNING: update_resolution will be depracated in >v2.2.0 "
                "please change to update_window_resolution()",
                FutureWarning,
                stacklevel=2
            )
        GlobalSettings._win_res = new_res


    @staticmethod
    def update_window_resolution(new_res:tuple[int,int]) -> None:
        GlobalSettings._win_res = new_res


    @staticmethod
    def update_display_resolution(new_res:tuple[int,int]) -> None:
        GlobalSettings._disp_res = new_res


    @staticmethod
    def load_settings_json():
        """
        Pass the saved settings from json.
        """
        for file_name in ["settings.json", path.join("..","settings.json") ,path.join("tleng2","settings.json"), path.join(getcwd(), "tleng2","settings.json")]:
            try:
                with open(file_name, "r") as settings_json:
                    data = json.load(settings_json)
                    #debug_print(data, tags=debug_tags)
                    # TODO: Write the load_settings_json to actually use the settings that are in json.
                    break
            except Exception as e:
                #debug_print(e, tags=debug_tags)
                #debug_print(f"Could not find the settings.json file, moving on. (Tried {file_name})", tags=debug_tags)
                #debug_print(path.exists(file_name), tags=debug_tags)
                ...