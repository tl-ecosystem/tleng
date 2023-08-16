# for ceratin class functions that reuire a constant variable from this page
import pygame, json


class Settings:
    def __init__(self):
        self._width = 700
        self._height = 700
        self._win = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Sample Version 2.2-exp")

        self._clock = pygame.time.Clock()
        self._fps = 2000      