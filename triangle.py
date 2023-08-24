import pygame
from typing import Tuple, List
import constants
from color import Color
from geometries.polygon import Polygon


class Triangle(Polygon):
    def __init__(self, index: int):
        self.index: int = index

        self._checkersCount: int = 0

        self._selectionShape: Polygon = Polygon(self.calculateSelectionShapePoints(), Color(236, 45, 250))
        self._selected: bool = False

        super().__init__(self.calculateGeometryPoints(), Color(71, 71, 71) if index % 2 == 0 else Color(40, 40, 40))

    @property
    def checkersCount(self):
        return self._checkersCount

    @checkersCount.setter
    def checkersCount(self, value: int):
        assert(value < 6)
        self._checkersCount = value

    def select(self):
        self._selected = True

    def deselect(self):
        self._selected = False

    def calculateGeometryPoints(self) -> Tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]:
        side: bool = self.index > 11
        borderOffset: float = constants.BORDER_WIDTH + (constants.BORDER_WIDTH * 2 * (5 < self.index < 12 or self.index > 17))
        triangleHeight: float = constants.TRIANGLES_HEIGHT + constants.BORDER_WIDTH if not side \
            else constants.WINDOW_HEIGHT - constants.TRIANGLES_HEIGHT - constants.BORDER_WIDTH
        yBasePos: float = constants.WINDOW_HEIGHT * side + constants.BORDER_WIDTH * (1 - 2 * side)

        return (pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12), yBasePos),
                pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12 + 1), yBasePos),
                pygame.Vector2(borderOffset + constants.TRIANGLES_BASE_LENGTH * (self.index % 12 + 0.5), triangleHeight))

    def calculateSelectionShapePoints(self) -> Tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]:
        points: List[pygame.Vector2] = list(self.calculateGeometryPoints())

        points[0].x -= constants.BORDER_WIDTH * 0.05
        points[1].x += constants.BORDER_WIDTH * 0.1
        points[2].y *= 0.95 if self.index > 11 else 1.05

        return tuple(points)

    def render(self, surface: pygame.Surface):
        if self._selected:
            self._selectionShape.render(surface)
        super().render(surface)
