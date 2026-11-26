"""Manage the game score."""

from src.shared.errors import BackendError


class ScoreManager:
    """Keep the player's score."""

    def __init__(
        self,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int
    ) -> None:
        """init the needed attrubites inside score manager"""
        points = (
            points_per_pacgum,
            points_per_super_pacgum,
            points_per_ghost,
        )
        if any(isinstance(value, bool) or not isinstance(value, int)
               for value in points):
            raise BackendError("Score values must be integers.")
        if any(value < 0 for value in points):
            raise BackendError("Score values cannot be negative.")
        self.total_score = 0
        self.normal_pg_point = points_per_pacgum
        self.power_pg_point = points_per_super_pacgum
        self.ghost_point = points_per_ghost

    def add_pacgum_score(self) -> None:
        """Add normal pacgum score to total score."""
        self.total_score += self.normal_pg_point

    def add_power_pacgum_score(self) -> None:
        """Add power pacgum score to total score."""
        self.total_score += self.power_pg_point

    def add_ghost_score(self) -> None:
        """Add ghost score to total score."""
        self.total_score += self.ghost_point

    def reset_score(self) -> None:
        """Set the score back to zero."""
        self.total_score = 0
