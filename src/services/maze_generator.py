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

    def make_maze(self, level: int, seed: int | None = None):
        """Ask the external tool for a maze."""
        try:
            maze_generator = MazeGenerator(
                seed=self.seed
            )
            maze_generator.generate(self.seed)
            self.maze = maze_generator.maze
            return self.maze
        except Exception as e:
            raise MazeGenerartorError(f"MazeGeneratorError: {e}")