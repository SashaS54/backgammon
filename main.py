import pygame

import constants


def main():
    pygame.init()
    pygame.display.set_caption("Backgammon")
    screen_surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    close = False
    image = pygame.image.load("assets/sashki.png")

    while not close:
        screen_surface.fill(constants.BACKGROUND_COLOR)
        screen_surface.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
        pygame.display.update()


if __name__ == "__main__":
    main()
