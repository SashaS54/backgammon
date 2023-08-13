import pygame
import constants
from color import Color
from gameField import GameField
from checker import Checker
from geometries.geometry import Geometry


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon")

        self.running: bool = True
        self.screenSurface: pygame.SurfaceType = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.gameField: GameField = GameField()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self._isLeftMouseDown(event):
                    self.gameField.deselectAllCheckers()
                    for triangle in self.gameField.triangles:
                        if self._isCursorOnGeometry(triangle):
                            if self.gameField.checkerToMove is None:
                                topChecker: Checker | None = self.gameField.getTopChecker(triangle.index)
                                if topChecker is None:
                                    break
                                self.gameField.selectTopChecker(triangle.index)
                                self.gameField.checkerToMove = topChecker
                            else:
                                try:
                                    self.gameField.moveChecker(self.gameField.checkerToMove, triangle.index)
                                except AssertionError:
                                    self.gameField.deselectAllCheckers()
                                self.gameField.checkerToMove = None
                            break

            self.screenSurface.fill(Color.Background.toTuple())
            self.gameField.render(self.screenSurface)

            pygame.display.update()

    def _isLeftMouseDown(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def _isLeftMouseUp(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1

    def _isCursorOnGeometry(self, geometry: Geometry) -> bool:
        return geometry.intersects(pygame.Vector2(pygame.mouse.get_pos()))
