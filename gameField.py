import pygame
from typing import Tuple, List
from geometries.rectangle import Rectangle
from geometries.polygon import Polygon
import constants
from color import Color


class GameField:
    def __init__(self):
        self.leftField: Rectangle = self.createField(False)
        self.rightField: Rectangle = self.createField(True)

        self.__bordersWidth: float = self.leftField.width * constants.BORDER_WIDTH_PERCENT
        self.leftFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.leftField)
        self.rightFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.rightField)

        self.__trianglesHeight: float = (self.leftField.height - 2 * self.__bordersWidth) * 0.3
        self.__trianglesBaseLength: float = (self.leftField.width + self.rightField.width
                                             - 4 * self.__bordersWidth) / 12
        self.triangles: List[Polygon] = [self.createTriangle(i) for i in range(24)]

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

    def createField(self, isRight: bool) -> Rectangle:
        return Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.45 * isRight, 0), constants.WINDOW_WIDTH * 0.45,
                         constants.WINDOW_HEIGHT, Color.Red if isRight else Color.Green)  # TODO Change to same color

    def createFieldBorders(self, field: Rectangle) -> Tuple[Rectangle, Rectangle, Rectangle, Rectangle]:
        return (Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          self.__bordersWidth, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          field.width, self.__bordersWidth, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x + field.width - self.__bordersWidth, field.point.y),
                          self.__bordersWidth, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y + field.height - self.__bordersWidth),
                          field.width, self.__bordersWidth, Color.BorderColor))

    def createTriangle(self, index: int) -> Polygon:
        side: bool = False if index < 12 else True
        offset: float = 2 * self.__bordersWidth if 5 < index < 12 or index > 17 else 0
        triangleHeight: float = self.__trianglesHeight + self.__bordersWidth if not side\
            else constants.WINDOW_HEIGHT - self.__trianglesHeight - self.__bordersWidth
        yBasePos: float = constants.WINDOW_HEIGHT * side + self.__bordersWidth * (1 - 2 * side)

        points: List[pygame.Vector2] = [pygame.Vector2(self.__bordersWidth + self.__trianglesBaseLength * (index % 12) + offset, yBasePos),
                                        pygame.Vector2(self.__bordersWidth + self.__trianglesBaseLength * (index % 12 + 1) + offset, yBasePos),
                                        pygame.Vector2(self.__bordersWidth + self.__trianglesBaseLength * (index % 12 + 0.5) + offset,
                                                       triangleHeight)]

        return Polygon(points, Color(15, 15, 15) if index % 2 == 1 else Color(71, 71, 71))

    def render(self, bgSurface: pygame.Surface):
        self.leftField.render(bgSurface)
        self.rightField.render(bgSurface)
        self.thatCubeShit.render(bgSurface)

        for side in self.leftFieldBorders:
            side.render(bgSurface)

        for side in self.rightFieldBorders:
            side.render(bgSurface)

        for triangle in self.triangles:
            triangle.render(bgSurface)
