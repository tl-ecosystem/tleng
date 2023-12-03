import pygame, json


class GlobalSettings:
    _win_res = (1280,720)
    _disp_res = (1280,720)
    _display_scaling = 1
    _scalable_window = False
    _display_ratio_lock = True #if the game only supports 500x500 then the window will ony scale to that ration
    _window = None # the window that you see
    _display = None # the inner display of the window
    # _platform = 'pc' # on what platform is the game for, if for mobile then the display should be changed

    _clock = pygame.time.Clock()
    _fps = 60

    _font = None # global font for the whole game.
    _debug = False

    # _index_event = 1

    # animation_database = {} # probably not to use

    @staticmethod
    def update_bresolution(new_res:tuple[int,int]) -> None:
        """
        Update the resolution of *both* the window, and the display.
        """
        GlobalSettings._win_res = new_res
        GlobalSettings._disp_res = new_res


    @staticmethod
    def load_display( bg_color: tuple[int,int,int] = (200,200,255) ) -> None:
        """
        Initialize the display.
        """
        GlobalSettings._display = pygame.Surface(GlobalSettings._disp_res) 
        GlobalSettings._window = pygame.display.set_mode(GlobalSettings._win_res)
        GlobalSettings._display.fill(bg_color)


    @staticmethod
    def load_settings_json():
        """
        Pass the saved settings from json.
        """
        pass


def scaling_display(width, height):
    #GlobalSettings._display = pygame.transform.scale(GlobalSettings._display, (width,height))
    GlobalSettings._window.blit(GlobalSettings._display,(0,0))


def fill_display(color:tuple[int,int,int]):
    GlobalSettings._display.fill(color)