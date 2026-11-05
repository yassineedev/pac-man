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
        self.directions = {
            "UP": self.NORTH,
            "RIGHT": self.EAST,
            "DOWN": self.SOUTH,
            "LEFT": self.WEST,
        }

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

        if direction not in self.directions:
            raise ValueError("direction not in dirictions, please check again.")
        cell = self.grid[y][x]
        wall = self.directions[direction]
        return bool(cell & wall)

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if movement is allowed."""
        if direction not in self.directions:
            return False
        if not self.is_inside(x, y):
            return False
        movements = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "RIGHT": (1, 0),
            "LEFT": (-1, 0)
        }
        mx, my = movements[direction]
        new_x = x + mx
        new_y = y + my
        if not self.is_inside(new_x, new_y):
            return False
        return not self.has_wall(x, y, direction)

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return all reachable neighboring cells."""
        neighbors = []
        movements = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "RIGHT": (1, 0),
            "LEFT": (-1, 0)
        }
        for drs in movements:
            if not self.can_move(x, y, drs):
                continue
            mx, my = movements[drs]
            new_x = x + mx
            new_y = y + my
            neighbors.append((new_x, new_y))
        return neighbors
