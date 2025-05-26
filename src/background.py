import random

from pydantic import BaseModel

from src.background_rect import BackgroundRect
from src.constants import COLORS, WIDTH


class Background(BaseModel):
    rects: list[BackgroundRect] = []

    def scroll(self, dx: int):
        """
        Scroll the background by a given horizontal distance.
        :param dx: The distance to scroll horizontally.
        """
        for rect in self.rects:
            rect.left -= dx

    def draw(self, surface):
        """
        Draw the background on the given surface.
        :param surface: The Pygame surface to draw on.
        """
        for rect in self.rects:
            rect._draw(surface)

    def fill(self, surface):
        """
        Fill the background with the first rectangle's color.
        :param surface: The Pygame surface to fill.
        """
        for rect in self.rects:
            if rect.left + rect.width < 0:
                self.rects.remove(rect)

        while self.rects[-1].left + self.rects[-1].width < WIDTH:
            self.rects.append(
                BackgroundRect(
                    left=self.rects[-1].left + self.rects[-1].width,
                    top=0,
                    width=random.randint(20, WIDTH // 6),
                    height=surface.get_height(),
                    color=COLORS[random.randint(0, len(COLORS) - 1)],
                )
            )

    def init(self, surface):
        """
        Initialize the background by filling it with rectangles.
        :param surface: The Pygame surface to fill.
        """
        complete_background_width = 0
        cpt = 0
        while complete_background_width < WIDTH:
            single_background_width = random.randint(20, WIDTH // 6)
            self.rects.append(
                BackgroundRect(
                    left=complete_background_width,
                    top=0,
                    width=single_background_width,
                    height=surface.get_height(),
                    color=COLORS[cpt % len(COLORS)],  # Background color
                )
            )
            complete_background_width += single_background_width
            cpt += 1
