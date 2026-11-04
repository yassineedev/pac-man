"""Keep the maze walls and pacgums."""

from src.shared.game_data import Position


class Maze:
    """Keep maze data and check open paths."""

    def __init__(self) -> None:
        pass

    def can_move_to(self, place: Position) -> bool:
        """Check if a place is open."""
        pass

    def get_nearby_paths(self, place: Position) -> list[Position]:
        """Get open places next to this place."""
        pass

    def eat_pacgum(self, place: Position) -> str | None:
        """Remove a pacgum and return its type."""
        pass

    def is_finished(self) -> bool:
        """Check if all pacgums are gone."""
        pass
