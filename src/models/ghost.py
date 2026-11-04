"""Ghost classes with simple polymorphism."""

from abc import ABC, abstractmethod

from src.shared.game_data import Direction, Position


class Ghost(ABC):
    """A base class for every ghost."""

    def __init__(self, start: Position, color: str) -> None:
        pass

    @abstractmethod
    def choose_direction(self, player: Position) -> Direction:
        """Choose where to move next."""
        pass

    def move(self, direction: Direction) -> None:
        """Move the ghost."""
        pass

    def return_to_start(self) -> None:
        """Move the ghost back to the start."""
        pass


class FollowGhost(Ghost):
    """A ghost that follows the player."""

    def choose_direction(self, player: Position) -> Direction:
        """Choose a path toward the player."""
        pass


class RandomGhost(Ghost):
    """A ghost that can pick different paths."""

    def choose_direction(self, player: Position) -> Direction:
        """Choose a path."""
        pass
