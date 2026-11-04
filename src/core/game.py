"""Control the game rules."""

from src.shared.game_data import Direction, GameData


class Game:
    """Keep all game objects and game rules together."""

    def __init__(self) -> None:
        pass

    def start_game(self) -> None:
        """Start a new game."""
        pass

    def update(self, time_passed: float) -> None:
        """Update the game after some time."""
        pass

    def move_player(self, direction: Direction) -> None:
        """Ask the player to move."""
        pass

    def pause_game(self) -> None:
        """Pause the game."""
        pass

    def continue_game(self) -> None:
        """Continue a paused game."""
        pass

    def get_game_data(self) -> GameData:
        """Give the UI the data it needs."""
        pass

    def use_cheat(self, cheat_name: str) -> None:
        """Use a cheat for testing."""
        pass
