import pygame
import constants
from color import Color
from gameField import GameField


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon")

        self.running: bool = True
        self.screenSurface: pygame.SurfaceType = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.gameField: GameField = GameField()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    keyName: str = pygame.key.name(event.key)
                    print(f"Yoo! {keyName.upper()} just got pressed.")

            self.screenSurface.fill(Color.Background.toTuple())
            self.gameField.render(self.screenSurface)

            pygame.display.update()
