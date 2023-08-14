import pygame
from typing import Sequence, Tuple
import random


class Dice:
    def __init__(self):
        self._images: Sequence[pygame.Surface] = ()
        self._currentImage: int = 0
        self._rolls: Tuple[int, int] = (0, 0)
        self._render: bool = False

        self._loadImages()

    def _loadImages(self):
        numbers: Sequence[str] = ("one", "two", "three", "four", "five", "six")
        self._images = tuple([pygame.image.load(f"assets/dice-{num}.png") for num in numbers])

    def roll(self) -> Tuple[int, int]:
        self._rolls = (random.randrange(1, 6), random.randrange(1, 6))
        return self._rolls

    def render(self, bgSurface: pygame.Surface):
        if self._render:
            bgSurface.blit(self._images[self._currentImage], (0, 0))  # TODO Find proper coordinates
