import pygame
import constants
import logger
from datetime import datetime
from sys import exit
from typing import Tuple, List
from color import Color
from gameField import GameField
from checker import Checker
from geometries.geometry import Geometry
from home import Home


class Application:
    def __init__(self, save: str | None = None):
        pygame.init()
        pygame.display.set_caption("Backgammon")

        self.running: bool = True
        self.clock = pygame.time.Clock()
        self.screenSurface: pygame.SurfaceType = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.gameField: GameField = GameField(save is not None)

        self._blackToMove: bool = True
        self._rolls: Tuple[int, int] = (0, 0)
        self._moved: List[bool] = [False, False]
        self._moves: int = 2

        if save is not None:
            self.loadGame(save)

    def start(self):

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.saveGame()
                    self.running = False
                if self._isLeftMouseDown(event):
                    if self.gameField.dice.inProcess:
                        continue

                    if self.gameField.dice.intersects(
                            pygame.Vector2(pygame.mouse.get_pos())) and not self.gameField.dice.dropped:
                        self.gameField.dice.roll()

                    if not self.gameField.dice.dropped:
                        continue

                    self.gameField.deselectAllCheckers()
                    self.gameField.deselectAllTriangles()
                    self.gameField.deselectAllHomes()

                    if self.gameField.occupyBars[not self._blackToMove].checkers > 0 and self.gameField.checkerToMove is None:
                        self.gameField.checkerToMove = self.gameField.getTopChecker(-2 + self._blackToMove)
                        self._selectValidMoves(11 + 12 * (not self._blackToMove))
                        continue

                    if self.gameField.checkerToMove is not None:
                        validMoves: List[int] = self._getValidMoves(self.gameField.checkerToMove.index)
                        home: Home = self.gameField.homes[self._blackToMove]

                        if home.index in validMoves:
                            if home.intersects(pygame.Vector2(pygame.mouse.get_pos())):
                                logger.logMoveToHome(self._blackToMove, self.gameField.checkerToMove.index)
                                self.gameField.moveCheckerToHome(self.gameField.checkerToMove)
                                home.checkers += 1

                                self._moved[validMoves.index(home.index)] = True
                                self._moves -= 1

                                if home.checkers == 15:
                                    logger.logGameEnd(self._blackToMove)
                                    pygame.quit()

                                if False not in self._moved and self._moves == 0:
                                    self._resetMove()

                                self.gameField.checkerToMove = None
                                continue

                    if self._isCursorOnGeometry(self.gameField.skipButton):
                        logger.logSkipMove(self._blackToMove)
                        self._resetMove()

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

                                self._selectValidMoves(triangle.index)
                            else:
                                validMoves: List[int] = self._getValidMoves(11 + 12 * (not self._blackToMove)
                                                                            if self.gameField.checkerToMove.index < 0
                                                                            else self.gameField.checkerToMove.index)

                                if triangle.index not in validMoves:
                                    self.gameField.checkerToMove = None
                                    break

                                try:
                                    oldIndex: int = self.gameField.checkerToMove.index
                                    self.gameField.moveChecker(self.gameField.checkerToMove, triangle.index)
                                except RuntimeError:
                                    self.gameField.deselectAllCheckers()
                                else:
                                    logger.logMove(self._blackToMove, oldIndex, triangle.index)
                                    self._moved[validMoves.index(triangle.index)] = True
                                    self._moves -= 1

                                    if oldIndex < 0:
                                        self.gameField.occupyBars[not self._blackToMove].checkers -= 1

                                    for checker in self.gameField.checkers:
                                        if checker.index == triangle.index and \
                                                checker.color != self.gameField.checkerToMove.color:
                                            self.gameField.occupyBars[self._blackToMove].checkers += 1
                                            self.gameField.lockChecker(checker)

                                            self.gameField.checkerToMove.height = 0
                                            self.gameField.checkerToMove.recalculateShapePosition()

                                            logger.logOccupy(self._blackToMove, triangle.index)
                                            break

                                    if False not in self._moved and self._moves == 0:
                                        self._resetMove()

                                self.gameField.checkerToMove = None
                            break
                    else:
                        self.gameField.checkerToMove = None

            if self.gameField.dice.canReadRolls:
                self._rolls = self.gameField.dice.readRolls()
                logger.logDice(self._blackToMove, self._rolls)

                if self._rolls[0] == self._rolls[1]:
                    self._moves = 4

            self.screenSurface.fill(Color.Background.toTuple())
            self.gameField.render(self.screenSurface, self.clock.get_time())

            pygame.display.update()

    def _isLeftMouseDown(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def _isLeftMouseUp(self, event: pygame.event.EventType) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1

    def _isCursorOnGeometry(self, geometry: Geometry) -> bool:
        return geometry.intersects(pygame.Vector2(pygame.mouse.get_pos()))

    def _getValidMoves(self, position: int) -> List[int]:
        result: List[int] = []

        for roll in self._rolls:
            if not self._blackToMove and position < 12 < position + roll:
                continue

            move: int = position + roll * (1 - 2 * self._blackToMove) * (1 - 2 * (position > 11))
            if not self._blackToMove and move == 12 and position < 12:
                move = -4
            elif move < 0 or (not self._blackToMove and position > 11 and move < 12):
                move = 11 - move

            result.append(-3 if move == 24 else move)

            if self._rolls[0] == self._rolls[1]:
                self._moved = [False]
                break

        return [x for x in result if x < 24]

    def _selectValidMoves(self, index: int):
        validMoves: List[int] = self._getValidMoves(index)
        for i, move in enumerate(validMoves):
            if self._moved[i]:
                continue

            if move < 0:
                self.gameField.homes[move + 4].select()
            elif self.gameField.isValidMove(self._blackToMove, move):
                self.gameField.triangles[move].select()

    def _resetMove(self):
        self._blackToMove = not self._blackToMove
        self.gameField.dice.dropped = False
        self._moved = [False, False]
        self._moves = 2

    def saveGame(self):
        fileName: str = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        with open(f"saves/{fileName}.bin", "xb") as file:
            file.write(b'\x01' if self._blackToMove else b'\x00')

            rolls: Tuple[int, int] = self.gameField.dice.readRolls()
            for roll in rolls:
                file.write(roll.to_bytes(1, byteorder="big", signed=False))

            file.write(b'\x01' if self.gameField.dice.dropped else b'\x00')

            for moved in self._moved:
                file.write(b'\x01' if moved else b'\x00')

            file.write(self._moves.to_bytes(1, byteorder="big", signed=False))

            for bar in self.gameField.occupyBars:
                file.write(bar.checkers.to_bytes(1, byteorder="big", signed=False))

            for home in self.gameField.homes:
                file.write(home.checkers.to_bytes(1, byteorder="big", signed=False))

            for triangle in self.gameField.triangles:
                topChecker: Checker | None = self.gameField.getTopChecker(triangle.index)
                color: bytes = b'\x01' if topChecker is not None and topChecker.color == Color.White else b'\x00'
                file.write(color)

                count: bytes = triangle.checkersCount.to_bytes(1, byteorder="big", signed=False)
                file.write(count)

    def loadGame(self, fileName: str):
        try:
            with open(f"saves/{fileName}", "rb") as file:
                try:
                    moveByte: bytes = file.read(1)
                    if moveByte == b'\x01':
                        self._blackToMove = True
                    elif moveByte == b'\x00':
                        self._blackToMove = False
                    else:
                        raise RuntimeError

                    rolls: List[int, int] = [0, 0]
                    for i in range(2):
                        rollByte: bytes = file.read(1)
                        rollInt: int = int.from_bytes(rollByte, byteorder="big", signed=False)

                        if rollInt == 0 or rollInt > 6:
                            raise RuntimeError

                        rolls[i] = rollInt
                    self.gameField.dice.loadRolls(tuple(rolls))
                    self._rolls = tuple(rolls)

                    diceDropped: bytes = file.read(1)
                    if diceDropped == b'\x01':
                        self.gameField.dice.dropped = True
                    elif diceDropped == b'\x00':
                        self.gameField.dice.dropped = False
                    else:
                        raise RuntimeError

                    for i in range(2):
                        movedByte: bytes = file.read(1)
                        if movedByte == b'\x01':
                            self._moved[i] = True
                        elif movedByte == b'\x00':
                            self._moved[i] = False
                        else:
                            raise RuntimeError

                    movesByte: bytes = file.read(1)
                    movesInt: int = int.from_bytes(movesByte, byteorder="big", signed=False)

                    if movesInt < 0 or movesInt > 4:
                        raise RuntimeError

                    self._moves = movesInt

                    for i in range(2):
                        occupyCheckersByte: bytes = file.read(1)
                        occupyCheckersInt: int = int.from_bytes(occupyCheckersByte, byteorder="big", signed=False)

                        if occupyCheckersInt < 0:
                            raise RuntimeError

                        self.gameField.occupyBars[i].checkers = occupyCheckersInt

                    for i in range(2):
                        homeCheckersByte: bytes = file.read(1)
                        homeCheckersInt: int = int.from_bytes(homeCheckersByte, byteorder="big", signed=False)

                        if homeCheckersInt < 0 or homeCheckersInt > 15:
                            raise RuntimeError

                        self.gameField.homes[i].checkers = homeCheckersInt

                    for triangle in self.gameField.triangles:
                        colorByte: bytes = file.read(1)
                        if colorByte == b'\x01':
                            isWhite: bool = True
                        elif colorByte == b'\x00':
                            isWhite: bool = False
                        else:
                            raise RuntimeError

                        countByte: bytes = file.read(1)
                        count: int = int.from_bytes(countByte, byteorder="big", signed=False)
                        if count > 5:
                            raise RuntimeError

                        for i in range(count):
                            self.gameField.createChecker(triangle.index, isWhite)
                except RuntimeError:
                    print("Save file is corrupted.")
                    exit(1)
        except FileNotFoundError:
            print("Couldn't find save file.")
            exit(1)
