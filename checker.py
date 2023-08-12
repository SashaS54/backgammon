import pygame
import constants
from geometries.circle import Circle
from color import Color


class Checker(Circle):
    def __init__(self, index: int, height: int, isWhite: bool):
        assert(index < 24)
        self._index = index
        self.height = height

        super().__init__(self.calculateGeometryCenter(), constants.TRIANGLES_BASE_LENGTH / 2,
                         Color.White if isWhite else Color.Black)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value: int):
        assert(value < 24)
        self._index = value

    def calculateGeometryCenter(self) -> pygame.Vector2:
        borderOffset: float = constants.BORDER_WIDTH + (constants.BORDER_WIDTH * 2 * (5 < self.index < 12 or self.index > 17))
        side: bool = self.index > 11
        heightOffset: float = (self.height + 0.5) * constants.TRIANGLES_BASE_LENGTH
        return pygame.Vector2(
            self.index % 12 * constants.TRIANGLES_BASE_LENGTH + constants.TRIANGLES_BASE_LENGTH / 2 + borderOffset,
            constants.WINDOW_HEIGHT * side + (constants.BORDER_WIDTH + heightOffset) * (1 - 2 * side))
