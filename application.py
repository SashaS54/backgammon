import pygame
import constants
import logger
from color import Color
from gameField import GameField
from checker import Checker
from geometries.geometry import Geometry


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon")

        self.running: bool = True
        self.clock = pygame.time.Clock()
        self.screenSurface: pygame.SurfaceType = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.gameField: GameField = GameField()

        self._blackToMove: bool = True

    def start(self):
        self.clock.tick(60)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self._isLeftMouseDown(event):
                    if self.gameField.dice.inProcess:
                        continue
                    self.gameField.deselectAllCheckers()
                    for triangle in self.gameField.triangles:
                        if self._isCursorOnGeometry(triangle):
                            if self.gameField.checkerToMove is None:
                                topChecker: Checker | None = self.gameField.getTopChecker(triangle.index)
                                if topChecker is None:
                                    break

                                if self._blackToMove and topChecker.color != Color.Black:
                                    break
                                if not self._blackToMove and topChecker.color != Color.White:
                                    break

                                self.gameField.selectTopChecker(triangle.index)
                                self.gameField.checkerToMove = topChecker
                            else:
                                try:
                                    oldIndex: int = self.gameField.checkerToMove.index
                                    self.gameField.moveChecker(self.gameField.checkerToMove, triangle.index)
                                except RuntimeError:
                                    self.gameField.deselectAllCheckers()
                                else:
                                    logger.logMove(self._blackToMove, oldIndex, triangle.index)
                                    self._blackToMove = not self._blackToMove
                                self.gameField.checkerToMove = None
                            break

            self.screenSurface.fill(Color.Background.toTuple())
            self.gameField.render(self.screenSurface, self.clock.get_time())

            pygame.display.update()

    def _isLeftMouseDown(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def _isLeftMouseUp(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1

    def _isCursorOnGeometry(self, geometry: Geometry) -> bool:
        return geometry.intersects(pygame.Vector2(pygame.mouse.get_pos()))
