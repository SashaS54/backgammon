import pygame
from typing import Tuple, List
from geometries.rectangle import Rectangle
from occupyBar import OccupyBar
from triangle import Triangle
from home import Home
import constants
from color import Color
from checker import Checker
from dice import Dice


class GameField:
    def __init__(self, loadSave: bool = False):
        self.leftField: Rectangle = self.createField(False)
        self.rightField: Rectangle = self.createField(True)

        self.leftFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(
            self.leftField)
        self.rightFieldBorders: Tuple[Rectangle, Rectangle, Rectangle, Rectangle] = self.createFieldBorders(
            self.rightField)

        self.triangles: List[Triangle] = [Triangle(i) for i in range(24)]

        self.thatCubeShit: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9, 0),
                                                 constants.WINDOW_WIDTH * 0.1, constants.WINDOW_HEIGHT, Color.Blue)

        self._skipButtonBorder: Rectangle = Rectangle(pygame.Vector2(self.thatCubeShit.point.x,
                                                                     self.thatCubeShit.height / 2
                                                                     - self.thatCubeShit.width / 2),
                                                      self.thatCubeShit.width, self.thatCubeShit.width,
                                                      Color.White)
        self.skipButton: Rectangle = Rectangle(pygame.Vector2(self._skipButtonBorder.point.x
                                                              + self.thatCubeShit.width / 18,
                                                              self._skipButtonBorder.point.y
                                                              + self._skipButtonBorder.width / 18),
                                               self._skipButtonBorder.width - self._skipButtonBorder.width / 10,
                                               self._skipButtonBorder.width - self._skipButtonBorder.width / 10,
                                               Color.Black)
        self._skipButtonText: pygame.font.FontType = pygame.font.Font("freesansbold.ttf", 32)

        self.dice = Dice()

        self.checkers: List[Checker] = []
        self.checkerToMove: Checker | None = None

        self.occupyBars: Tuple[OccupyBar, OccupyBar] = (OccupyBar(True), OccupyBar(False))

        if not loadSave:
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

    def createChecker(self, index: int, isWhite: bool):
        self.checkers.append(Checker(index, self.triangles[index].checkersCount, isWhite))
        self.triangles[index].checkersCount += 1

    def _initCheckers(self):
        for i in range(5):
            self.createChecker(0, True)
            self.createChecker(6, False)
            self.createChecker(12, False)
            self.createChecker(18, True)

        for i in range(3):
            self.createChecker(4, False)
            self.createChecker(16, True)

        for i in range(2):
            self.createChecker(11, True)
            self.createChecker(23, False)

    def moveChecker(self, checker: Checker, index: int):
        if checker.index == index:
            raise RuntimeError
        if not self.isValidMove(checker.color == Color.Black, index):
            raise RuntimeError

        if checker.index > 0:
            self.triangles[checker.index].checkersCount -= 1
        checker.height = self.triangles[index].checkersCount
        checker.move(index)
        self.triangles[index].checkersCount += 1

    def lockChecker(self, checker: Checker):
        self.triangles[checker.index].checkersCount -= 1
        checker.lock()
        checker.height = self.occupyBars[checker.color == Color.Black].checkers

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

    def isValidMove(self, isBlack: bool, index: int) -> bool:
        if self.triangles[index].checkersCount == 5:
            return False

        if self.triangles[index].checkersCount == 1:
            return True

        topChecker: Checker | None = self.getTopChecker(index)
        if topChecker is None:
            return True

        return topChecker.color == (Color.Black if isBlack else Color.White)

    def selectTopChecker(self, index: int):
        topChecker: Checker | None = self.getTopChecker(index)
        if topChecker is None:
            return
        topChecker.select()

    def deselectAllCheckers(self):
        for checker in self.checkers:
            checker.deselect()

    def deselectAllTriangles(self):
        for triangle in self.triangles:
            triangle.deselect()

    def render(self, bgSurface: pygame.Surface, deltaTime: int):
        self.leftField.render(bgSurface)
        self.rightField.render(bgSurface)
        self.thatCubeShit.render(bgSurface)
        self.dice.render(bgSurface, deltaTime)

        self._skipButtonBorder.render(bgSurface)
        self.skipButton.render(bgSurface)
        skitButtonTextSurface: pygame.Surface = self._skipButtonText.render("Skip", True, (255, 255, 255))
        skipButtonTextRect: pygame.Rect = skitButtonTextSurface.get_rect()
        skipButtonTextRect.center = (self.skipButton.point.x + self.skipButton.width / 2,
                                     self.skipButton.point.y + self.skipButton.height / 2)
        bgSurface.blit(skitButtonTextSurface, skipButtonTextRect)

        for side in self.leftFieldBorders:
            side.render(bgSurface)

        for side in self.rightFieldBorders:
            side.render(bgSurface)

        for triangle in self.triangles:
            triangle.render(bgSurface)

        for checker in self.checkers:
            checker.render(bgSurface)

        for bar in self.occupyBars:
            bar.render(bgSurface)
