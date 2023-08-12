import pygame
from color import *
from abc import ABC, abstractmethod


class Geometry(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def intersects(self, point: pygame.Vector2) -> bool:
        pass

    def __init__(self, color: Color):
        self.color: Color = color
