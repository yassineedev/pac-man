"""Ghost classes for the game."""

import random

from src.models.character import Character
from src.models.maze import Maze
from src.services.pathfinding import BFS
from src.shared.game_data import Direction, GhostStatu, Position


class Ghost(Character):
    """Basic class used by every ghost."""

    def __init__(self, start: Position, color: str, maze: Maze) -> None:
        """Create a ghost."""
        super().__init__(start, Direction.LEFT)
        self.color = color
        self.maze = maze
        self.pathfinder = BFS()
        self.state = GhostStatu.NORMAL

    def make_weak(self) -> None:
        """Make the ghost weak."""
        if self.state != GhostStatu.EATEN:
            self.state = GhostStatu.WEAK

    def make_normal(self) -> None:
        """Make the ghost normal again."""
        self.state = GhostStatu.NORMAL

    def get_eaten(self) -> None:
        """Set the ghost as eaten."""
        self.state = GhostStatu.EATEN

    def reset(self) -> None:
        """Put the ghost back at its first position."""
        self.return_to_start()
        self.make_normal()

    def get_valid_directions(self) -> list[Direction]:
        """Return directions where the ghost can move."""
        directions = []
        for direction in Direction:
            can_move = self.maze.can_move(
                self.position.x,
                self.position.y,
                direction.value,
            )
            if can_move:
                directions.append(direction)
        return directions

    def get_direction_from_path(
        self, path: list[Position] | None
    ) -> Direction:
        """Get the direction of the first step in a path."""
        if path is None or len(path) < 2:
            return self.direction

        next_position = path[1]
        difference_x = next_position.x - self.position.x
        difference_y = next_position.y - self.position.y

        if difference_x == 1:
            return Direction.RIGHT
        if difference_x == -1:
            return Direction.LEFT
        if difference_y == 1:
            return Direction.DOWN
        if difference_y == -1:
            return Direction.UP
        return self.direction

    def go_to_position(self, target: Position) -> Direction:
        """Choose a direction that goes to a target position."""
        try:
            path = self.pathfinder.find_path(
                self.position,
                target,
                self.maze,
            )
            return self.get_direction_from_path(path)
        except (ValueError, IndexError, TypeError):
            return self.direction

    def get_distance(self, position: Position, target: Position) -> int:
        """Return a simple distance between two positions."""
        return abs(position.x - target.x) + abs(position.y - target.y)

    def run_away(self, player_position: Position) -> Direction:
        """Choose the valid direction farthest from Pac-Man."""
        directions = self.get_valid_directions()
        if not directions:
            return self.direction

        best_direction = directions[0]
        best_distance = -1

        for direction in directions:
            new_position = self.get_next_position(direction)
            distance = self.get_distance(new_position, player_position)
            if distance > best_distance:
                best_distance = distance
                best_direction = direction

        return best_direction

    def get_next_position(self, direction: Direction) -> Position:
        """Return the position after moving one cell."""
        x = self.position.x
        y = self.position.y

        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.RIGHT:
            x += 1

        return Position(x, y)

    def get_position_ahead(
        self, player_position: Position, cells: int
    ) -> Position:
        """Return a position ahead of Pac-Man."""
        x = player_position.x
        y = player_position.y

        if self.direction == Direction.UP:
            y -= cells
        elif self.direction == Direction.DOWN:
            y += cells
        elif self.direction == Direction.LEFT:
            x -= cells
        elif self.direction == Direction.RIGHT:
            x += cells

        x = max(0, min(x, self.maze.width - 1))
        y = max(0, min(y, self.maze.height - 1))
        return Position(x, y)

    def choose_move(self, player_position: Position) -> Direction:
        """Choose a basic movement for the ghost."""
        if self.state == GhostStatu.WEAK:
            return self.run_away(player_position)
        if self.state == GhostStatu.EATEN:
            return self.go_to_position(self.start_position)
        return self.go_to_position(player_position)


class FirstGhost(Ghost):
    """Ghost that follows Pac-Man."""

    def choose_move(self, player_position: Position) -> Direction:
        """Follow Pac-Man."""
        return super().choose_move(player_position)


class SecondGhost(Ghost):
    """Ghost that tries to go in front of Pac-Man."""

    def choose_move(self, player_position: Position) -> Direction:
        """Go to a position two cells ahead."""
        if self.state == GhostStatu.WEAK:
            return self.run_away(player_position)
        if self.state == GhostStatu.EATEN:
            return self.go_to_position(self.start_position)

        target = self.get_position_ahead(player_position, 2)
        return self.go_to_position(target)


class ThirdGhost(Ghost):
    """Ghost that targets a position far from Pac-Man."""

    def choose_move(self, player_position: Position) -> Direction:
        """Go to a position four cells ahead."""
        if self.state == GhostStatu.WEAK:
            return self.run_away(player_position)
        if self.state == GhostStatu.EATEN:
            return self.go_to_position(self.start_position)

        target = self.get_position_ahead(player_position, 4)
        return self.go_to_position(target)


class FourthGhost(Ghost):
    """Ghost that moves in random valid directions."""

    def choose_move(self, player_position: Position) -> Direction:
        """Choose a random direction."""
        if self.state == GhostStatu.WEAK:
            return self.run_away(player_position)
        if self.state == GhostStatu.EATEN:
            return self.go_to_position(self.start_position)

        directions = self.get_valid_directions()
        if directions:
            return random.choice(directions)
        return self.direction
