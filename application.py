import pygame
import constants


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon")

        self.running: bool = True
        self.screenSurface: pygame.surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.imageSurface: pygame.Surface = pygame.image.load("assets/sashki.png")

    def start(self):
        while self.running:
            self.screenSurface.fill(constants.BACKGROUND_COLOR)
            self.screenSurface.blit(self.imageSurface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    keyName: str = pygame.key.name(event.key)
                    print(f"Yoo! {keyName.upper()} just got pressed.")
            pygame.display.update()
