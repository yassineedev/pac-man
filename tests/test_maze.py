from src.models.maze import Maze

def test_has_wall() -> None:
    maze = Maze(21, 21)

    # Use a small controlled grid to test wall logic.
    # 10 = EAST (2) + WEST (8)
    maze.grid = [[10]]

    # Update dimensions to match the test grid.
    maze.width = 1
    maze.height = 1

    assert maze.has_wall(0, 0, "RIGHT") is True
    assert maze.has_wall(0, 0, "LEFT") is True
    assert maze.has_wall(0, 0, "UP") is False
    assert maze.has_wall(0, 0, "DOWN") is False

    print("Wall tests passed!")


def test_invalid_position() -> None:
    maze = Maze(21, 21)
    maze.grid = [[15]]
    maze.width = 1
    maze.height = 1

    try:
        maze.has_wall(5, 5, "RIGHT")
    except ValueError:
        print("Invalid position test passed!")
    else:
        raise AssertionError("Expected ValueError")


def test_invalid_direction() -> None:
    maze = Maze(21, 21)
    maze.grid = [[15]]
    maze.width = 1
    maze.height = 1

    try:
        maze.has_wall(0, 0, "JUMP")
    except ValueError:
        print("Invalid direction test passed!")
    else:
        raise AssertionError("Expected ValueError")


if __name__ == "__main__":
    test_has_wall()
    test_invalid_position()
    test_invalid_direction()