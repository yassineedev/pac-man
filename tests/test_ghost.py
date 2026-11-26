"""Tests for ghost state changes."""

from src.models.ghost import FirstGhost
from src.models.maze import Maze
from src.shared.game_data import GhostStatu, Position


def test_eaten_ghost_returns_to_normal_after_respawn_delay() -> None:
    """An eaten ghost should respawn and become normal again."""
    maze = Maze(3, 3)
    ghost = FirstGhost(Position(1, 1), "red", maze)

    ghost.get_eaten()
    ghost.update_respawn(1.0)

    assert ghost.state == GhostStatu.EATEN
    assert ghost.respawn_time_left == 1
    assert ghost.position == ghost.start_position

    ghost.update_respawn(1.0)

    assert ghost.state == GhostStatu.NORMAL
    assert ghost.respawn_time_left == 0
