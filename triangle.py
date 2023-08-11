import pygame
from typing import Tuple
import constants
from color import Color
from geometries.polygon import Polygon


class Triangle:
    def __init__(self, index: int):
        self.index: int = index
        self.color: Color = Color(71, 71, 71) if index % 2 == 0 else Color(15, 15, 15)
        self._geometry = Polygon(self.calculateGeometryPoints(), self.color)

    def calculateGeometryPoints(self) -> Tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]:
        side: bool = False if self.index < 12 else True
        borderOffset: float = constants.BORDER_WIDTH + (constants.BORDER_WIDTH * 2 * (5 < self.index < 12 or self.index > 17))
        triangleHeight: float = constants.TRIANGLES_HEIGHT + constants.BORDER_WIDTH if not side \
            else constants.WINDOW_HEIGHT - constants.TRIANGLES_HEIGHT - constants.BORDER_WIDTH
        yBasePos: float = constants.WINDOW_HEIGHT * side + constants.BORDER_WIDTH * (1 - 2 * side)

        return (pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12), yBasePos),
                pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12 + 1), yBasePos),
                pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12 + 0.5), triangleHeight))

    def render(self, surface: pygame.Surface):
        self._geometry.render(surface)
