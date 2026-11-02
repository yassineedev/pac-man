"""Main menu and navigation rendering."""
import pygame

from src.services.highscore import ScoreEntry


class MenuView:
    """Draw the start menu, instructions and highscores."""

    def draw_main(self, surface: pygame.Surface) -> None:
        """Draw start, highscores, instructions and exit options."""
        pass

    def draw_highscores(
        self, surface: pygame.Surface, scores: list[ScoreEntry]
    ) -> None:
        """Draw the top ten scores."""
        pass

    def draw_instructions(self, surface: pygame.Surface) -> None:
        """Draw controls and game rules."""
        pass
