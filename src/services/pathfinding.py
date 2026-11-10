from collections import deque
from src.models.maze import Maze
from src.shared.game_data import Position

class BFS:
    def find_path(
            self,
            start: Position,
            target: Position,
            maze: Maze
    ) -> None | list:
        """Find path to the target using bfs"""
        if not start or not target or not maze:
            return None
        queue = deque([start])
        visited: set = {start}
        visite_order = []
        previous = {
            start: None
        }
        while queue:
            current: Position = queue.popleft()
            neighbs = maze.get_neighbors(current.x, current.y)
            visite_order.append(current)
            if current == target:
                break
            for x, y in neighbs:
                n = Position(x, y)
                if n not in visited:
                    visited.add(n)
                    previous[n] = current
                    queue.append(n)
        # here i should build the previos path
        
