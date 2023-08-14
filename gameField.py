import pygame
from typing import Tuple, List
from geometries.rectangle import Rectangle
from triangle import Triangle
import constants
from color import Color
from checker import Checker
from dice import Dice


class GameField:
    def __init__(self):
        self.leftField: Rectangle = self.createField(False)
        self.rightField: Rectangle = self.createField(True)

        self.leftFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(
            self.leftField)
        self.rightFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(
            self.rightField)

        self.triangles: List[Triangle] = [Triangle(i) for i in range(24)]

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

        self.dice = Dice()

        self.checkers: List[Checker] = []
        self.checkerToMove: Checker | None = None

        self._initCheckers()

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

    def _createChecker(self, index: int, isWhite: bool):
        self.checkers.append(Checker(index, self.triangles[index].checkersCount, isWhite))
        self.triangles[index].checkersCount += 1

    def _initCheckers(self):
        for i in range(5):
            self._createChecker(0, True)
            self._createChecker(6, False)
            self._createChecker(12, False)
            self._createChecker(18, True)

        for i in range(3):
            self._createChecker(4, False)
            self._createChecker(16, True)

        for i in range(2):
            self._createChecker(11, True)
            self._createChecker(23, False)

    def moveChecker(self, checker: Checker, index: int):
        assert(checker.index != index)
        if self.triangles[index].checkersCount > 1:
            for ch in self.checkers:
                if ch.index == index:
                    assert(ch.color == checker.color)
        self.triangles[checker.index].checkersCount -= 1
        checker.height = self.triangles[index].checkersCount
        checker.move(index)
        self.triangles[index].checkersCount += 1

    def getTopChecker(self, index: int) -> Checker | None:
        result: Checker | None = None

        height: int = 0
        for checker in self.checkers:
            if checker.index != index:
                continue
            if checker.height < height:
                continue

            result = checker
            height = checker.height

        return result

    def selectTopChecker(self, index: int):
        topChecker: Checker | None = self.getTopChecker(index)
        if topChecker is None:
            return
        topChecker.select()

    def deselectAllCheckers(self):
        for checker in self.checkers:
            checker.deselect()

    def render(self, bgSurface: pygame.Surface):
        self.leftField.render(bgSurface)
        self.rightField.render(bgSurface)
        self.thatCubeShit.render(bgSurface)
        self.dice.render(bgSurface)

        for side in self.leftFieldBorders:
            side.render(bgSurface)

        for side in self.rightFieldBorders:
            side.render(bgSurface)

        for triangle in self.triangles:
            triangle.render(bgSurface)

        for checker in self.checkers:
            checker.render(bgSurface)
