"""Read keys from the player."""

from src.shared.game_data import Direction


class InputHandler:
    """Turn keyboard keys into game commands."""

    def get_direction(self, key: str) -> Direction | None:
        """Get a direction from a key."""
        pass
