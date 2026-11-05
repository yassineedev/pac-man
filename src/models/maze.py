"""Manage the maze and its movement rules."""

from src.services.maze_generator import MazeGeneratorPanel


class Maze:
    """Represent the maze used by Pac-Man and ghosts."""

    # Wall bitmasks from the 42 maze generator
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze."""
        self.width = width
        self.height = height

        self.grid: list[list[int]] = []

        self.generator = MazeGeneratorPanel((width, height))

    def generate(self, seed: int = 0) -> None:
        """Generate a maze using the given seed."""
        self.grid = self.generator.make_maze(seed)

    def is_inside(self, x: int, y: int) -> bool:
        """Check if a position is inside the maze."""
        pass

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if a wall exists in a direction."""
        pass

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if movement is allowed."""
        pass

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return all reachable neighboring cells."""
        pass