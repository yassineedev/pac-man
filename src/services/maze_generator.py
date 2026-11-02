"""Adapter for the externally assigned A-Maze-ing package."""
from src.models.maze import Maze


class MazeGeneratorAdapter:
    """Convert external generator output to the internal Maze model."""

    def generate(self, width: int, height: int, seed: int | None) -> Maze:
        """Request a non-perfect maze and normalize its representation."""
        pass

    def convert(self, external_maze: object) -> Maze:
        """Convert the assigned package's output to a Maze."""
        pass

    def validate(self, maze: Maze) -> bool:
        """Check that spawns and required corridors are accessible."""
        pass
