"""Tests for the Pac-Man Player class."""

from src.models.player import Player
from src.shared.game_data import Direction, Position
from src.models.maze import Maze


def test_player() -> None:
    """Test Player initialization, movement, and reset."""

    maze = Maze(3, 3)
    maze.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    start = Position(1, 1)
    player = Player(start, Direction.RIGHT)

    # Test 1: Initialization
    assert player.position == start
    print("✅ Player initialization: PASS")

    # Test 2: Choose move
    player.set_direction(Direction.DOWN)
    direction = player.choose_move(player.position)

    assert direction == Direction.DOWN
    print("✅ Choose move: PASS")

    # Test 3: Movement
    player.move(Direction.RIGHT, maze)
    assert player.position == Position(2, 1)
    assert player.direction == Direction.RIGHT

    # The maze boundary prevents movement outside the grid.
    player.move(Direction.RIGHT, maze)
    assert player.position == Position(2, 1)

    print("✅ Player movement: PASS")

    # Test 4: Return to start
    player.reset_position()

    assert player.position == start
    print("✅ Return to start: PASS")

    print("\n🎉 All Player tests passed!")


if __name__ == "__main__":
    test_player()
