"""The Pac-Man player."""

from src.shared.game_data import Direction, Position


class Player:
    """Keep the player's place and movement."""

    def __init__(self, start: Position) -> None:
        pass

    def move(self, direction: Direction) -> None:
        """Move the player in one direction."""
        pass

    def return_to_start(self) -> None:
        """Move the player back to the start."""
        pass
