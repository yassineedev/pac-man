"""The Pac-Man player."""

from src.shared.game_data import Direction, Position, PlayerData
from .character import Character


class Player(Character):
    """Keep the player's place and movement."""

    def __init__(
            self,
            start: Position,
            direction: Direction
    ) -> None:
        """Create the player with a position and a direction."""
        super().__init__(start, direction)
        self.input_direction: Direction = direction

    # The player direction is selected by input before this method is called.
    def choose_move(self, player_position: Position) -> Direction:
        """Move the player in one direction."""
        return self.input_direction

    def set_direction(self, direction: Direction) -> None:
        """Set the direction chosen by the player."""
        self.input_direction = direction

    def reset_position(self) -> None:
        """Move the player back to the starting position."""
        self.position = self.start_position

    def return_to_start(self) -> None:
        """Move the player back to the start."""
        self.reset_position()

    def player_data(self) -> PlayerData:
        """return player data"""
        return PlayerData(
            position=self.position,
            Direction=self.direction
        )
