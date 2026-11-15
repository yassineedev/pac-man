from typing import Set, Tuple, List

from src.models.maze import Maze
from src.shared.game_data import Position


class PacgumManager:
    """Pacgums class manager"""

    def __init__(
        self,
        maze: Maze,
        protected_positions: Set[Tuple[int, int]],
        player_start: Position,
    ) -> None:
        """init the atrributes needed"""
        self.maze: Maze = maze
        self.cells_42 = protected_positions
        self.player = (player_start.x, player_start.y)
        self.power_pacgum: Set[Tuple[int, int]] = set()
        self.pacgums: Set[Tuple[int, int]] = set()
        self.corners: List[Tuple[int, int]] = [
            (0, 0),
            (0, self.maze.height - 1),
            (self.maze.width - 1, 0),
            (self.maze.width - 1, self.maze.height - 1),
        ]
        self.pacgum_eated = False

    def create_power_pacgums(self) -> None:
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
        # here am going to create a new set of sets filtred
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

    def eat_pacgum(self, position: Tuple[int, int]) -> bool:
        """mark pacgum eated by delting the position from pacgums"""
        try:
            if position in self.pacgums:
                self.pacgums.remove(position)
                return True
            return False
        except (KeyError, RuntimeError):
            return False

    def eat_power_pacgums(self, position: Tuple[int, int]) -> bool:
        """
        mark powerfull pacgum eated.
        by delting the position from power_pacgum"""
        try:
            if position in self.power_pacgum:
                self.power_pacgum.remove(position)
                return True
            return False
        except (KeyError, RuntimeError):
            return False

    def all_pacgums_eaten(self) -> bool:
        """all pac gums earted means the level is done"""
        return not self.power_pacgum and not self.pacgums
