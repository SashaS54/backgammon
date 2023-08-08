import pygame
from typing import Tuple, Sequence
from geometries.geometry import Geometry
from color import Color


class Polygon(Geometry):
    def __init__(self, points: Sequence[pygame.Vector2], color: Color):
        super().__init__(color)

        self.points: Sequence[pygame.Vector2] = points

    def render(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.color.toTuple(), self.points)
