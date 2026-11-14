from src.models.maze import Maze


class PacgumManager:
    def __init__(self, maze, protected_positions) -> None:
        """init the atrributes needed"""
        self.maze: Maze = maze
        self.cells_42 = protected_positions

    def create_pacgums(self):
        """create pacgums"""
        # here am going to create a new list filtred
        # from invalid positions
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                position = (x, y)

                if position in self.cells_42:
                    continue


    def create_power_pacgums(self):
        """create powerful pacgums"""
        pass

    def eat_pacgum(self, position):
        """mark pacgum eated"""
        pass

    def eat_power_pacgums(self, position):
        """mark powerfull pacgum eated"""
        pass

    def all_pacgums_eaten(self):
        """all pac games eated"""
        pass