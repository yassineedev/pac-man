from src.models.maze import Maze
from src.shared.game_data import Position

class PacgumManager:

    def __init__(self, maze, protected_positions, player_start: Position) -> None:
        """init the atrributes needed"""
        self.maze: Maze = maze
        self.cells_42 = protected_positions
        self.player = (player_start.x, player_start.y)
        self.power_pacgum = set()
        self.pacgums = set()
        self.corners = [
            (0, 0),
            (0, self.maze.height - 1),
            (self.maze.width - 1, 0),
            (self.maze.width - 1, self.maze.height - 1)
        ]

    def create_power_pacgums(self):
        """create powerful pacgums"""
        for position in self.corners:
            x, y = position

            if not self.maze.is_inside(x, y):
                continue
            if len(self.maze.get_neighbors(x, y)) == 0:
                continue
            if position in self.cells_42:
                continue
            if position == self.player:
                continue

            self.power_pacgum.add(position)

        # this logic going to check if the position are 4 if not
        # they are going to add one valid randomly from the maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if len(self.power_pacgum) == 4:
                    return

                position = (x, y)

                if position in self.power_pacgum:
                    continue
                if position in self.cells_42:
                    continue
                if position == self.player:
                    continue
                if len(self.maze.get_neighbors(x, y)) == 0:
                    continue

        self.power_pacgum.add(position)
    def create_pacgums(self) -> None:
        """create pacgums"""
        # here am going to create a new list filtred
        # from invalid positions (cleaning the unusefull cells)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                position = (x, y)
                if not self.maze.is_inside(x, y):
                    continue
                if len(self.maze.get_neighbors(x, y)) == 0:
                    continue
                if position in self.cells_42:
                    continue
                if position == self.player:
                    continue
                if position in self.power_pacgum:
                    continue
                self.pacgums.add(position)

    def eat_pacgum(self, position):
        """mark pacgum eated"""
        pass

    def eat_power_pacgums(self, position):
        """mark powerfull pacgum eated"""
        pass

    def all_pacgums_eaten(self):
        """all pac games eated"""
        pass
