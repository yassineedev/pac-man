from typing import List, Set, Tuple, Union

from src.models.maze import Maze
from src.shared.game_data import Position


class PacgumManager:
    """Pacgums class manager"""

    def __init__(
            self,
            maze: Maze,
            protected_positions: Set[
                Union[Position, Tuple[int, int]]
            ],
            player_start: Position,
    ) -> None:
        """init the atrributes needed"""
        self.maze: Maze = maze
        self.cells_42: Set[Position] = set()
        for cell in protected_positions:
            if isinstance(cell, Position):
                self.cells_42.add(cell)
            else:
                self.cells_42.add(Position(cell[0], cell[1]))

        self.player: Position = player_start
        self.power_pacgum: Set[Position] = set()
        self.pacgums: Set[Position] = set()
        self.corners: List[Position] = [
            Position(0, 0),
            Position(0, self.maze.height - 1),
            Position(self.maze.width - 1, 0),
            Position(self.maze.width - 1, self.maze.height - 1),
        ]
        self.pacgum_eated = False

    def create_power_pacgums(self) -> None:
        """create powerful pacgums"""
        self.power_pacgum.clear()

        for position in self.corners:
            self.power_pacgum.add(position)

    def create_pacgums(self) -> None:
        """create pacgums"""
        # here am going to create a new set of sets filtred
        # from invalid positions (cleaning the unusefull cells)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                position = Position(x, y)
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

    def eat_pacgum(self, position: Position) -> bool:
        """mark pacgum eated by delting the position from pacgums"""
        try:
            if position in self.pacgums:
                self.pacgums.remove(position)
                return True
            return False
        except (KeyError, RuntimeError):
            return False

    def eat_power_pacgums(self, position: Position) -> bool:
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
