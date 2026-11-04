"""Other game screens."""

from abc import ABC, abstractmethod


class Screen(ABC):
    """A base class for game screens."""

    @abstractmethod
    def draw(self) -> None:
        """Draw this screen."""
        pass


class PauseScreen(Screen):
    """Show the pause screen."""

    def draw(self) -> None:
        """Draw the pause screen."""
        pass


class EndScreen(Screen):
    """Show the win or game-over screen."""

    def draw(self) -> None:
        """Draw the end screen."""
        pass


class HelpScreen(Screen):
    """Show how to play."""

    def draw(self) -> None:
        """Draw the help screen."""
        pass


class HighScoreScreen(Screen):
    """Show the best scores."""

    def draw(self) -> None:
        """Draw the highscore screen."""
        pass
