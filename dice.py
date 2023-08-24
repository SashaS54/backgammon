import pygame
from typing import Sequence, Tuple
import random
import constants


class Dice:
    def __init__(self):
        self._images: Sequence[pygame.Surface] = ()
        self._rolls: Tuple[int, int] = (0, 0)
        self._inProcess: bool = False
        self._canReadRolls = False

        self._elapsedTime: int = 1
        self._iterations: int = 1
        self._timeDelay: int = 100
        self._reset: bool = True

        self.dropped: bool = False

        self._loadImages()
        self._scaleImage()

    def _loadImages(self):
        numbers: Sequence[str] = ("one", "two", "three", "four", "five", "six")
        self._images = tuple([pygame.image.load(f"assets/dice-{num}.png") for num in numbers])

    def _scaleImage(self):
        self._images = tuple(
            [pygame.transform.scale(img, (constants.DICE_LENGTH, constants.DICE_LENGTH)) for img in self._images])

    @property
    def inProcess(self):
        return self._inProcess

    @property
    def canReadRolls(self):
        return self._canReadRolls

    def readRolls(self) -> Tuple[int, int]:
        self._canReadRolls = False
        return self._rolls

    def loadRolls(self, rolls: Tuple[int, int]):
        self._rolls = rolls

    def _roll(self):
        while True:
            rolls: Tuple[int, int] = (random.randrange(1, 6), random.randrange(1, 6))
            if self._rolls[0] != rolls[0] and self._rolls[1] != rolls[1]:
                self._rolls = rolls
                break

    def roll(self):
        self._inProcess = True

    def render(self, bgSurface: pygame.Surface, deltaTime: int):
        self._elapsedTime += deltaTime / 60

        bgSurface.blit(self._images[self._rolls[0] - 1], constants.DICE_POSITION)
        bgSurface.blit(self._images[self._rolls[1] - 1], (constants.DICE_POSITION[0] + constants.DICE_LENGTH,
                                                          constants.DICE_POSITION[1]))

        if self._inProcess:
            if self._iterations < 10:
                if self._reset:
                    self._elapsedTime = 0
                    self._reset = False
                if self._elapsedTime >= self._timeDelay:
                    self._roll()
                    self._timeDelay += 100
                    self._iterations += 1
                    self._elapsedTime = 0
            else:
                self._reset = True
                self._timeDelay = 100
                self._iterations = 0
                self._inProcess = False
                self._canReadRolls = True
                self.dropped = True

    def intersects(self, point: pygame.Vector2):
        return constants.DICE_POSITION[0] + constants.DICE_LENGTH * 2 >= point.x >= constants.DICE_POSITION[0] and\
            constants.DICE_POSITION[1] + constants.DICE_LENGTH >= point.y >= constants.DICE_POSITION[1]
