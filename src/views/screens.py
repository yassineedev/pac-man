"""Pause, result and name-entry screens."""
import pygame


class ScreenView:
    """Render secondary screens and overlays."""

    def draw_pause(self, surface: pygame.Surface) -> None:
        """Draw resume and return-to-menu options."""
        pass

    def draw_game_over(self, surface: pygame.Surface, score: int) -> None:
        """Draw the final score after defeat."""
        pass

    def draw_victory(self, surface: pygame.Surface, score: int) -> None:
        """Draw the final score after victory."""
        pass

    def draw_name_entry(self, surface: pygame.Surface, name: str) -> None:
        """Draw the highscore name input."""
        pass
