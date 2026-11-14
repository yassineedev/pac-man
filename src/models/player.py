"""The Pac-Man player."""

from src.shared.game_data import Direction, Position
from .character import Character


class Player(Character):
    """Keep the player's place and movement."""

    def __init__(
            self,
            start: Position,
            direction: Direction,
            lives: int
    ) -> None:
        super().__init__(start, direction)
        self.lives = lives
        self.score = 0
        self.input_direction: Direction = direction

    # The player direction is selected by input before this method is called.
    def choose_move(self, player_position: Position) -> Direction:
        """Move the player in one direction."""
        return self.input_direction

    # this method return the player to the start position.
    def return_to_start(self) -> None:
        """Move the player back to the start."""
        self.position = self.start_position

    # lose life method if the player killed by the ghost.
    def lose_life(self) -> None:
        """ Lose one life if the player dead"""
        if self.lives > 0:
            self.lives -= 1

    def add_score(self, points: int) -> None:
        """Add scoore for each ghost called"""
        if points > 0:
            self.score += points
