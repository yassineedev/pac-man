"""Tests for the Pac-Man Player class."""

from src.models.player import Player
from src.shared.game_data import Direction, Position
from src.models.maze import Maze


def test_player() -> None:
    """Test Player initialization, movement, lives, and score."""

    maze = Maze(15, 15)
    maze.generate(seed=42)

    start = Position(0, 0)
    player = Player(start, Direction.RIGHT, lives=3)

    # Test 1: Initialization
    assert player.position == start
    assert player.lives == 3
    assert player.score == 0
    print("✅ Player initialization: PASS")

    # Test 2: Choose move
    player.input_direction = Direction.DOWN
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

    # Test 4: Lose life
    player.lose_life()
    assert player.lives == 2

    player.lose_life()
    player.lose_life()
    player.lose_life()

    assert player.lives == 0
    print("✅ Lose life: PASS")

    # Test 5: Add score
    player.add_score(10)
    player.add_score(50)
    player.add_score(200)

    assert player.score == 260

    player.add_score(-10)
    assert player.score == 260

    print("✅ Add score: PASS")

    # Test 6: Return to start
    player.return_to_start()

    assert player.position == start
    print("✅ Return to start: PASS")

    print("\n🎉 All Player tests passed!")


if __name__ == "__main__":
    test_player()
