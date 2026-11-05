from src.models.maze import Maze

# def test_has_wall() -> None:
#     maze = Maze(21, 21)

#     # Use a small controlled grid to test wall logic.
#     # 10 = EAST (2) + WEST (8)
#     maze.grid = [[10]]

#     # Update dimensions to match the test grid.
#     maze.width = 1
#     maze.height = 1

#     assert maze.has_wall(0, 0, "RIGHT") is True
#     assert maze.has_wall(0, 0, "LEFT") is True
#     assert maze.has_wall(0, 0, "UP") is False
#     assert maze.has_wall(0, 0, "DOWN") is False

#     print("Wall tests passed!")


# def test_invalid_position() -> None:
#     maze = Maze(21, 21)
#     maze.grid = [[15]]
#     maze.width = 1
#     maze.height = 1

#     try:
#         maze.has_wall(5, 5, "RIGHT")
#     except ValueError:
#         print("Invalid position test passed!")
#     else:
#         raise AssertionError("Expected ValueError")


# def test_invalid_direction() -> None:
#     maze = Maze(21, 21)
#     maze.grid = [[15]]
#     maze.width = 1
#     maze.height = 1

#     try:
#         maze.has_wall(0, 0, "JUMP")
#     except ValueError:
#         print("Invalid direction test passed!")
#     else:
#         raise AssertionError("Expected ValueError")


# if __name__ == "__main__":
#     test_has_wall()
#     test_invalid_position()
#     test_invalid_direction()


# from src.models.maze import Maze


# def test_can_move() -> None:
#     maze = Maze(3, 3)

#     # All cells are open except the wall between (0, 0) and (1, 0).
#     maze.grid = [
#         [2, 8, 0],
#         [0, 0, 0],
#         [0, 0, 0]
#     ]

#     # Test 1: Moving into a wall
#     assert maze.can_move(0, 0, "RIGHT") is False
#     assert maze.can_move(1, 0, "LEFT") is False

#     # Test 2: Moving through an open path
#     assert maze.can_move(0, 0, "DOWN") is True
#     assert maze.can_move(1, 1, "RIGHT") is True
#     assert maze.can_move(1, 1, "UP") is True

#     # Test 3: Moving outside the maze
#     assert maze.can_move(0, 0, "UP") is False
#     assert maze.can_move(0, 0, "LEFT") is False
#     assert maze.can_move(2, 2, "RIGHT") is False
#     assert maze.can_move(2, 2, "DOWN") is False

#     # Test 4: Invalid starting position
#     assert maze.can_move(-1, 0, "RIGHT") is False
#     assert maze.can_move(3, 0, "LEFT") is False

#     # Test 5: Invalid direction
#     assert maze.can_move(1, 1, "JUMP") is False

#     print("All can_move tests passed!")


# if __name__ == "__main__":
#     test_can_move()

def test_get_neighbors() -> None:
    """Test reachable neighboring cells."""
    maze = Maze(3, 3)

    maze.grid = [
        [2, 8, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    # RIGHT blocked, UP and LEFT outside.
    assert maze.get_neighbors(0, 0) == [(0, 1)]

    # LEFT blocked, UP outside.
    assert maze.get_neighbors(1, 0) == [(1, 1), (2, 0)]

    # All four directions are open.
    assert maze.get_neighbors(1, 1) == [
        (1, 0),
        (1, 2),
        (2, 1),
        (0, 1)
    ]

    # Invalid position has no neighbors.
    assert maze.get_neighbors(-1, 0) == []

    print("✅ get_neighbors tests passed!")


if __name__ == "__main__":
    test_get_neighbors()