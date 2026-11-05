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
        return True if 0 <= x < self.width and 0 <= y < self.height else False

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if a wall exists in a direction."""
        if not self.grid:
            raise ValueError("No grid found, Maze not generated.")
        if not self.is_inside(x, y):
            raise ValueError("X or Y is outsid of the grid.")
        directions = {
            "UP": self.NORTH,
            "RIGHT": self.EAST,
            "DOWN": self.SOUTH,
            "LEFT": self.WEST,
        }
        if direction not in directions:
            raise ValueError("direction not in dirictions, please check again.")
        cell = self.grid[x][y]
        wall = directions[direction]
        return bool(cell & wall)

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if movement is allowed."""
        pass

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return all reachable neighboring cells."""
        pass