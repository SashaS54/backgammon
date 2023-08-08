import pygame
from typing import Tuple
from geometries.rectangle import Rectangle
import constants
from color import Color


class GameField:
    def __init__(self):
        self.leftField: Rectangle = self.createField(False)
        self.leftFieldBorders = self.createFieldBorders(self.leftField)

        self.rightField: Rectangle = self.createField(True)
        self.rightFieldBorders = self.createFieldBorders(self.rightField)

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

    def createField(self, isRight: bool) -> Rectangle:
        return Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.45 * isRight, 0), constants.WINDOW_WIDTH * 0.45,
                         constants.WINDOW_HEIGHT, Color.Red if isRight else Color.Green)  # TODO Change to same color

    def createFieldBorders(self, field: Rectangle) -> Tuple[Rectangle, Rectangle, Rectangle, Rectangle]:
        borderWidth = field.width * 0.05
        return (Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          borderWidth, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y),
                          field.width, borderWidth, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x + field.width - borderWidth, field.point.y),
                          borderWidth, field.height, Color.BorderColor),
                Rectangle(pygame.Vector2(field.point.x, field.point.y + field.height - borderWidth),
                          field.width, borderWidth, Color.BorderColor))

    def render(self, bgSurface: pygame.Surface):
        self.leftField.render(bgSurface)
        self.rightField.render(bgSurface)
        self.thatCubeShit.render(bgSurface)

        for side in self.leftFieldBorders:
            side.render(bgSurface)

        for side in self.rightFieldBorders:
            side.render(bgSurface)
