import pygame

import constants


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    close = False

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
        pygame.display.flip()


if __name__ == "__main__":
    main()
