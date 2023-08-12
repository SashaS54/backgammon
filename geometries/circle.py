import pygame
from geometries.geometry import Geometry
from color import Color


class Circle(Geometry):
    def __init__(self, center: pygame.Vector2, radius: float, color: Color):
        super().__init__(color)

        self.center: pygame.Vector2 = center
        self.radius: float = radius

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color.toTuple(), self.center, self.radius)

    def intersects(self, point: pygame.Vector2) -> bool:
        return self.center.x - self.radius <= point.x <= self.center.x + self.radius and\
               self.center.y - self.radius <= point.y <= self.center.y + self.radius
