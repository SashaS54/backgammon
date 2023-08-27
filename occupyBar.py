import pygame
import constants
from color import Color


class OccupyBar:
    def __init__(self, isBlack: bool):
        self._isBlack = isBlack
        self._color = Color.Black if isBlack else Color.White

        self.checkers: int = 0
        self._font: pygame.font.FontType = pygame.font.Font("freesansbold.ttf", 32)

    def render(self, surface: pygame.Surface):
        if self.checkers > 0:
            textSurface: pygame.Surface = self._font.render(str(self.checkers), True, self._color.toTuple())
            textRect: pygame.Rect = textSurface.get_rect()
            textRect.center = ((constants.FIELD_WIDTH * 2) / 2,
                               constants.WINDOW_HEIGHT / 2 + constants.WINDOW_HEIGHT / 10 * (1 - 2 * (not self._isBlack)))

            surface.blit(textSurface, textRect)
