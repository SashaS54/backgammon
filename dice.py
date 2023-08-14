import pygame
from typing import Sequence, Tuple
import random
import constants


class Dice:
    def __init__(self):
        self._images: Sequence[pygame.Surface] = ()
        self._rolls: Tuple[int, int] = (0, 0)
        self._inProcess: bool = False

        self._elapsedTime: int = 0
        self._iterations: int = 0
        self._timeDelay: int = 500
        self._reset: bool = True

        self._loadImages()
        self._scaleImage()

    def _loadImages(self):
        numbers: Sequence[str] = ("one", "two", "three", "four", "five", "six")
        self._images = tuple([pygame.image.load(f"assets/dice-{num}.png") for num in numbers])

    def _scaleImage(self):
        self._images = tuple([pygame.transform.scale(img, (constants.DICE_LENGTH, constants.DICE_LENGTH)) for img in self._images])

    @property
    def rolls(self):
        return self._rolls

    @property
    def inProcess(self):
        return self._inProcess

    def _roll(self):
        while True:
            rolls: Tuple[int, int] = (random.randrange(1, 6), random.randrange(1, 6))
            if self._rolls[0] != rolls[0] and self._rolls[1] != rolls[1]:
                self._rolls = rolls
                break

    def roll(self):
        self._inProcess = True

    def render(self, bgSurface: pygame.Surface, elapsedTime: int):  # TODO Add some delay at the end
        self._elapsedTime += elapsedTime
        if self._inProcess:
            bgSurface.blit(self._images[self._rolls[0]], constants.DICE_POSITION)
            bgSurface.blit(self._images[self._rolls[1]], (constants.DICE_POSITION[0] + constants.DICE_LENGTH,
                                                          constants.DICE_POSITION[1]))
            if self._iterations < 10:
                if self._reset:
                    self._elapsedTime = 0
                    self._reset = False
                if self._elapsedTime >= self._timeDelay:
                    self._roll()
                    self._timeDelay += 2000
                    self._iterations += 1
                    self._elapsedTime = 0
            else:
                self._reset = True
                self._timeDelay = 0
                self._iterations = 0
                self._inProcess = False