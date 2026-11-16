from collections import deque

from src.models.maze import Maze
from src.shared.game_data import Position


class BFS:
    def find_path(
            self,
            start: Position,
            target: Position,
            maze: Maze
    ) -> list[Position] | None:
        """Find path to the target using bfs"""
        if not start or not target or not maze:
            return None
        queue: deque[Position] = deque([start])
        visited: set[Position] = {start}
        previous: dict[Position, Position | None] = {start: None}
        found = False

        while queue:
            current_position = queue.popleft()
            neighbs = maze.get_neighbors(
                current_position.x,
                current_position.y,
            )
            if current_position == target:
                found = True
                break
            for n in neighbs:
                if n not in visited:
                    visited.add(n)
                    previous[n] = current_position
                    queue.append(n)
        # here i should build the previos path
        if not found:
            return None
        path_position: Position | None = target
        path: list[Position] = []
        while path_position is not None:
            path.append(path_position)
            path_position = previous[path_position]
        path.reverse()
        return path
