"""Test player spawn positions."""

from src.models.maze import Maze
from src.services.spawnmanager import SpawnManager


def test_player_spawn(width: int, height: int) -> None:
    """Test player spawn for different maze sizes."""

    maze = Maze(width, height)
    maze.generate(seed=42)

    spawn_manager = SpawnManager(maze)
    spawn = spawn_manager.find_player_spawn()

    # Handle None when the maze is too small.
    protected = spawn_manager.get_protected_cells() or set()

    print(f"\nMaze: {width}x{height}")
    print(f"Player spawn: {spawn}")
    print(f"Protected: {spawn in protected}")

    assert isinstance(spawn, tuple)
    assert len(spawn) == 2

    x, y = spawn

    assert maze.is_inside(x, y)
    assert spawn not in protected
    assert len(maze.get_neighbors(x, y)) > 0

    print("PASS")


if __name__ == "__main__":
    test_player_spawn(45, 45)  # Odd x Odd
    test_player_spawn(44, 44)  # Even x Even
    test_player_spawn(45, 44)  # Odd x Even
    test_player_spawn(44, 45)  # Even x Odd

    test_player_spawn(9, 9)    # Small maze, no 42

    print("\nAll player spawn tests passed!")