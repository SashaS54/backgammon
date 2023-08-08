import pygame
from color import *
from abc import ABC, abstractmethod


class Geometry(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    def __init__(self, color: Color):
        self.color: Color = color
