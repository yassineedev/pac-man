"""Tests for the Pac-Man Player class."""

from src.models.player import Player
from src.shared.game_data import Direction, Position
from src.models.maze import Maze


def test_player() -> None:
    """Test Player initialization, movement, and reset."""

    maze = Maze(15, 15)
    maze.generate(seed=42)

    start = Position(0, 0)
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
    old_position = player.position

    player.move(Direction.RIGHT, maze)

    if maze.can_move(
        old_position.x,
        old_position.y,
        Direction.RIGHT.value
    ):
        assert player.position == Position(
            old_position.x + 1,
            old_position.y
        )
    else:
        assert player.position == old_position

    print("✅ Player movement: PASS")

    # Test 4: Return to start
    player.reset_position()

    assert player.position == start
    print("✅ Return to start: PASS")

    print("\n🎉 All Player tests passed!")


if __name__ == "__main__":
    test_player()
