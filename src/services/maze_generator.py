"""Connect our game to the required maze generator."""

from src.models.maze import Maze


class MazeGenerator:
    """Use the external maze tool without changing it."""

    def make_maze(self, level: int, seed: int | None = None) -> Maze:
        """Ask the external tool for a maze."""
        pass
