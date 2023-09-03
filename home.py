import pygame
import constants
from geometries.rectangle import Rectangle
from color import Color


class Home:
    def __init__(self, isBlack: bool):
        self.isBlack: bool = isBlack
        self.index: int = -3 - 1 * (not isBlack)
        self.checkers: int = 0

        self._defaultColor = Color.Black if isBlack else Color.White

        self._rect: Rectangle = Rectangle(pygame.Vector2(constants.WINDOW_WIDTH * 0.9,
                                                         isBlack * (constants.WINDOW_WIDTH * 0.1 + (constants.WINDOW_HEIGHT - constants.WINDOW_WIDTH * 0.1) / 2 )),
                                          constants.WINDOW_WIDTH * 0.1,
                                          (constants.WINDOW_HEIGHT - constants.WINDOW_WIDTH * 0.1) / 2,
                                          self._defaultColor)
        self._text: pygame.font.FontType = pygame.font.Font("freesansbold.ttf", 32)

    def select(self):
        self._rect.color = Color(236, 45, 250)

    def deselect(self):
        self._rect.color = self._defaultColor

    def render(self, surface: pygame.Surface):
        self._rect.render(surface)

        textSurface: pygame.Surface = self._text.render(str(self.checkers), True,
                                                        (255, 255, 255) if self.isBlack else (0, 0, 0))
        textRect: pygame.Rect = textSurface.get_rect()
        textRect.center = (self._rect.point.x + self._rect.width / 2, self._rect.point.y + self._rect.height / 2)

        surface.blit(textSurface, textRect)

    def intersects(self, point: pygame.Vector2) -> bool:
        return self._rect.intersects(point)
