from pydantic import BaseModel


class BackgroundRect(BaseModel):
    left: int
    top: int
    width: int
    height: int  # Coordinates and dimensions of the rectangle
    color: tuple[int, int, int]  # RGB color as a tuple of integers

    def _draw(self, surface):
        """
        Draw the rectangle on the given surface.
        :param surface: The Pygame surface to draw on.
        """
        import pygame

        pygame.draw.rect(
            surface=surface,
            color=self.color,
            rect=(self.left, self.top, self.width, self.height),
        )
