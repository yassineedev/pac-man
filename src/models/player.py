"""The Pac-Man player."""

from src.shared.game_data import Direction, Position
from .character import Character


class Player(Character):
    """Keep the player's place and movement."""

    def __init__(self, start: Position) -> None:
        super.__init__(start, Direction.LEFT)
        self.lives = 0
        self.score = 0

    # forced method for direction moves.
    def choose_move(self, direction: Direction) -> None:
        """Move the player in one direction."""
        pass

    # this method return the player to the start position.
    def return_to_start(self) -> None:
        """Move the player back to the start."""
        pass

    # lose life method if the player killed by the ghost.
    def lose_life():
        """ Lose one life if the player dead"""
        pass