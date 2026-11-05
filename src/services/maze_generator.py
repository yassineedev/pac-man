"""Connect our game to the required maze generator."""
from mazegenerator import MazeGenerator


# from src.models.maze import Maze

class MazeGenerartorError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class MazeGeneratorPanel:
    """Use the external maze tool without changing it."""
    def __init__(self, size: tuple[int, int], seed: int = 0):
        self.size = size
        self.seed = seed

        self.maze = None

    """Connect our game to the required maze generator."""

from mazegenerator import MazeGenerator


class MazeGeneratorError(Exception):
    """Error when maze generation fails."""


class MazeGeneratorPanel:
    """Use the external maze generator."""

    def __init__(self, size: tuple[int, int], seed: int = 42):
        self.size = size
        self.seed = seed
        self.maze: list[list[int]] = []

    def make_maze(
        self,
        level: int,
        seed: int | None = None
    ) -> list[list[int]]:
        """Generate a maze for the given level."""

        try:
            if seed is not None:
                current_seed = seed
            elif level == 1:
                current_seed = self.seed
            else:
                current_seed = 0

            generator = MazeGenerator(
                size=self.size,
                perfect=False,
                seed=current_seed
            )

            self.maze = generator.maze

            return self.maze

        except Exception as e:
            raise MazeGeneratorError(
                f"Maze generation failed: {e}"
            ) from e