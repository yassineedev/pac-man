# from .src.models.maze import Maze


class SpawnManager:
    def __init__(self, maze):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height

    def get_protected_cells(self) -> None | list[set[int, int]]:
        """get protected 42 cells to using giving layouts"""
        ft_small = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        if len(ft_small)*2 > self.maze.height or len(ft_small[0])*2 > self.maze.width:
            return None
        protected_cells = set()
        posy = int((self.maze.height - len(ft_small)) / 2)
        posx = int((self.maze.width - len(ft_small[0])) / 2)
        for y in range(len(ft_small)):
            for x in range(len(ft_small[y])):
                if ft_small[y][x]:
                    new_y = y + posy
                    new_x = x + posx
                    protected_cells.add((new_x, new_y))
        return protected_cells

    def find_player_spawn(self) -> tuple[int, int]:
        """Find the starting position of Pac-Man."""

        if not self.maze.grid:
            raise ValueError("Maze not generated.")

        mid_x = self.width // 2
        mid_y = self.height // 2

        protected_cells = self.get_protected_cells()

        # Case 1: Odd X, Odd Y
        if self.width % 2 == 1 and self.height % 2 == 1:
            positions = [
                (mid_x, mid_y),
            ]

        # Case 2: Even X, Even Y
        elif self.width % 2 == 0 and self.height % 2 == 0:
            positions = [
                (mid_x - 1, mid_y),
                (mid_x, mid_y),
                (mid_x - 1, mid_y - 1),
                (mid_x, mid_y - 1),
            ]

        # Case 3: Odd X, Even Y
        elif self.width % 2 == 1 and self.height % 2 == 0:
            positions = [
                (mid_x, mid_y - 1),
                (mid_x, mid_y),
            ]

        # Case 4: Even X, Odd Y
        elif self.width % 2 == 0 and self.height % 2 == 1:
            positions = [
                (mid_x - 1, mid_y),
                (mid_x, mid_y),
            ]

        # maze to small
        else:
            positions = [
                (mid_x, mid_y)
            ]
        for position in positions:
            if not protected_cells:
                return (mid_x, mid_y)
            if position not in protected_cells:
                return position

    def find_ghost_spawn(self) -> dict[str, set]:
        """find the start position of each ghost."""
        if not self.maze.grid or not self.height or not self.width:
            raise ValueError("No grid found to get start ghosts position start.")
        ghost_sets = {
            "ghost_0": (0, 0),
            "ghost_1": (0, self.height - 1),
            "ghost_2": (self.width - 1, 0),
            "ghost_3": (self.width - 1, self.height - 1)
        }
        return ghost_sets
