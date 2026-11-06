from models.maze import Maze


class SpawnManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze: Maze = None


    def __get_protected_cells(self) -> None | list[set[int, int]]:
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
        for y in range(self.maze.height):
            for x in range(len(self.maze.width)):
                if ft_small[y][x]:
                    new_y = y + posy
                    new_x = x + posx
                    protected_cells.add((new_x, new_y))

    def find_player_spawn(self) -> set[int, int]:
        """find the start position of the player."""
        if not self.maze.grid:
            raise ValueError("no grid inserted to get start position method.")
        mid_x = self.width // 2
        mid_y = self.height // 2
        # handle odd x odd
        if self.width % 2 == 0 and self.height % 2 == 0:

    def find_ghost_spawn(self):
        """find the start position of each ghost."""
        if not self.grid:
            raise ValueError("No grid found to get start ghosts position start.")
