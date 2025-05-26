import pygame

from src.background import Background
from src.constants import DURATION, HEIGHT, WIDTH


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Pygame Window")

    back_ground = Background()
    back_ground.init(screen)  # Initialize the background with rectangles

    running = True

    for _ in range(DURATION):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        back_ground.scroll(2)  # Scroll the background by 1 pixel
        back_ground.fill(screen)
        back_ground.draw(screen)

        pygame.display.update()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()
