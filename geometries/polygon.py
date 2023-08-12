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

    def intersects(self, point: pygame.Vector2) -> bool:
        result: bool = False
        i = 0
        j = len(self.points) - 1
        while i < len(self.points):
            if ((self.points[i].y < point.y <= self.points[j].y)
                    or (self.points[j].y < point.y <= self.points[i].y)):
                if self.points[i].x + (point.y - self.points[i].y) / (
                        self.points[j].y - self.points[i].y) * (self.points[j].x - self.points[i].x) < \
                        point.x:
                    result = not result
            j = i
            i += 1
        return result
