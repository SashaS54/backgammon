import pygame
from geometries.geometry import Geometry
from color import *


class Rectangle(Geometry):
    def __init__(self, point: pygame.Vector2, width: float, height: float, color: Color):
        super().__init__(color)

        self.point: pygame.Vector2 = point
        self.width: float = width
        self.height: float = height

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color.toTuple(), pygame.Rect(self.point.x, self.point.y, self.width, self.height))
