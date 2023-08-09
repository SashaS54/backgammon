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

        self.leftFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.leftField)
        self.rightFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.rightField)

        self.triangles: List[Polygon] = [self.createTriangle(i) for i in range(24)]

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

    def createField(self, isRight: bool) -> Rectangle:
        return Rectangle(pygame.Vector2(constants.FIELD_WIDTH * isRight, 0), constants.FIELD_WIDTH,
                         constants.WINDOW_HEIGHT, Color.Red if isRight else Color.Green)  # TODO Change to same color

    def createFieldBorders(self, field: Rectangle) -> Tuple[Rectangle, Rectangle, Rectangle, Rectangle]:
        return (Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          constants.BORDER_WIDTH, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          field.width, constants.BORDER_WIDTH, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x + field.width - constants.BORDER_WIDTH, field.point.y),
                          constants.BORDER_WIDTH, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y + field.height - constants.BORDER_WIDTH),
                          field.width, constants.BORDER_WIDTH, Color.BorderColor))

    def createTriangle(self, index: int) -> Polygon:
        side: bool = False if index < 12 else True
        offset: float = 2 * constants.BORDER_WIDTH if 5 < index < 12 or index > 17 else 0
        triangleHeight: float = constants.TRIANGLES_HEIGHT + constants.BORDER_WIDTH if not side\
            else constants.WINDOW_HEIGHT - constants.TRIANGLES_HEIGHT - constants.BORDER_WIDTH
        yBasePos: float = constants.WINDOW_HEIGHT * side + constants.BORDER_WIDTH * (1 - 2 * side)

        points: List[pygame.Vector2] = [pygame.Vector2(constants.BORDER_WIDTH + constants.TRIANGLES_BASE_LENGTH * (index % 12) + offset, yBasePos),
                                        pygame.Vector2(constants.BORDER_WIDTH + constants.TRIANGLES_BASE_LENGTH * (index % 12 + 1) + offset, yBasePos),
                                        pygame.Vector2(constants.BORDER_WIDTH + constants.TRIANGLES_BASE_LENGTH * (index % 12 + 0.5) + offset,
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
