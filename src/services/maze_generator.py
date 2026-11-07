"""Connect our game to the required maze generator."""
from mazegenerator import MazeGenerator



class MazeGeneratorError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MazeGeneratorPanel:
    """Use the external maze generator."""

    def __init__(self, width: int = 15, height: int = 15, seed: int = 42) -> None:
        self.width = width
        self.height = height
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
            s = (self.width, self.height)
            print("WIDTH:", self.width, "HEIGHT:", self.height)
            generator = MazeGenerator(
                size=s,
                perfect=False,
                seed=current_seed
            )

            self.maze = generator.maze
            return self.maze
        except Exception as e:
            raise MazeGeneratorError(
                f"Maze generation failed: {e}"
            ) from e
