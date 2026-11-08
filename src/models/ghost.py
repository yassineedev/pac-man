import random

from src.shared.game_data import Direction, Position
from .character import Character


class Ghost(Character):
    """Base class for ghosts."""

    def __init__(self, start: Position, color: str) -> None:
        super().__init__(start)
        self.color = color


class FollowGhost(Ghost):
    """Ghost that follows Pac-Man."""

    def choose_move(self, maze, player_position: Position) -> Direction:
        """Choose direction toward Pac-Man."""
        # BFS implementation comes later.
        return self.direction


class RandomGhost(Ghost):
    """Ghost that chooses random directions."""

    def choose_move(self, maze, player_position: Position) -> Direction:
        """Choose a random valid direction."""
        directions = list(Direction)

        valid = [
            direction
            for direction in directions
            if maze.can_move(
                self.position.x,
                self.position.y,
                direction.value
            )
        ]

        return random.choice(valid) if valid else self.direction