import pygame
from typing import Tuple, List
from geometries.rectangle import Rectangle
from triangle import Triangle
import constants
from color import Color
from checker import Checker


class GameField:
    def __init__(self):
        self.leftField: Rectangle = self.createField(False)
        self.rightField: Rectangle = self.createField(True)

        self.leftFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.leftField)
        self.rightFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(self.rightField)

        self.triangles: List[Triangle] = [Triangle(i) for i in range(24)]

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

        self.checkers = [Checker(12, 2, True), Checker(0, 1, True), Checker(0, 2, True), Checker(1, 0, False),
                         Checker(1, 1, False), Checker(1, 2, False)]

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

        for checker in self.checkers:
            checker.render(bgSurface)
