import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    close = False

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
        pygame.display.flip()


if __name__ == "__main__":
    main()
