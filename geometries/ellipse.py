import pygame
from geometries.geometry import Geometry
from color import Color


class Ellipse(Geometry):
    def __init__(self, center: pygame.Vector2, width: float, height: float, color: Color):
        super().__init__(color)

        self.center: pygame.Vector2 = center
        self.width: float = width
        self.height: float = height

    def render(self, surface: pygame.Surface):
        x: float = self.center.x - self.width / 2
        y: float = self.center.y - self.height / 2
        pygame.draw.ellipse(surface, self.color.toTuple(), pygame.Rect(x, y, self.width, self.height))

    def intersects(self, point: pygame.Vector2) -> bool:
        return (((point.x - self.center) ** 2) / (self.width / 2 ** 2) +
                ((point.y - self.center.y) ** 2) / (self.height / 2 ** 2)) <= 1
