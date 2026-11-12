"""Test BFS pathfinding."""

from collections import deque

from src.models.maze import Maze
from src.services.pathfinding import BFS
from src.shared.game_data import Position


def test_bfs(width: int, height: int, seed: int) -> None:
    """Test BFS on a generated maze."""

    maze = Maze(width, height)
    maze.generate(seed=seed)

    bfs = BFS()

    start = Position(0, 0)
    target = Position(width - 1, height - 1)

    path = bfs.find_path(start, target, maze)

    print(f"\nMaze: {width}x{height}, Seed: {seed}")

    # Test 1: A path exists
    assert path is not None
    assert path[0] == start
    assert path[-1] == target

    print("✅ Path found: PASS")

    # Test 2: Every movement is valid
    for current, next_pos in zip(path, path[1:]):
        neighbors = maze.get_neighbors(current.x, current.y)

        assert next_pos in neighbors, (
            f"Invalid movement: {current} -> {next_pos}\n"
            f"Valid neighbors: {neighbors}"
        )

    print("✅ Valid movements: PASS")

    # Test 3: Path is shortest
    queue = deque([(start, 0)])
    visited: set[Position] = {start}
    shortest_steps = None

    while queue:
        current, distance = queue.popleft()

        if current == target:
            shortest_steps = distance
            break

        # get_neighbors() already returns list[Position]
        neighbors = maze.get_neighbors(current.x, current.y)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    assert shortest_steps is not None
    assert len(path) - 1 == shortest_steps

    print("✅ Shortest path: PASS")
    print(f"Path length: {len(path) - 1} steps")


def test_same_position() -> None:
    """Test when start and target are the same."""

    maze = Maze(15, 15)
    maze.generate(seed=42)

    bfs = BFS()
    start = Position(0, 0)

    path = bfs.find_path(start, start, maze)

    assert path == [start]

    print("✅ Same position: PASS")


def test_no_path() -> None:
    """Test when the target cannot be reached."""

    maze = Maze(15, 15)
    maze.generate(seed=42)

    bfs = BFS()

    start = Position(0, 0)

    # Find a protected 42 cell with four walls.
    target = None

    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 15:
                target = Position(x, y)
                break

        if target is not None:
            break

    assert target is not None, "No protected cell found"

    path = bfs.find_path(start, target, maze)

    assert path is None, (
        f"Expected no path to protected cell {target}, got {path}"
    )

    print("✅ No path: PASS")


if __name__ == "__main__":
    # Different maze sizes
    test_bfs(15, 15, 42)
    test_bfs(20, 20, 42)
    test_bfs(45, 45, 42)
    test_bfs(45, 30, 123)

    # Special cases
    test_same_position()
    test_no_path()

    print("\n🎉 All BFS tests passed!")