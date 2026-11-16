"""Tests for the PacgumManager class."""

from src.models.maze import Maze
from src.models.pacgum import PacgumManager
from src.services.spawnmanager import SpawnManager
from src.shared.game_data import Position


def make_pacgum_manager() -> PacgumManager:
    """Create a pacgum manager for testing."""
    maze = Maze(15, 15)
    maze.generate(seed=42)

    spawn_manager = SpawnManager(maze)
    player_start = spawn_manager.find_player_spawn()
    protected_cells = spawn_manager.get_protected_cells() or set()

    return PacgumManager(maze, protected_cells, player_start)


def test_create_power_pacgums() -> None:
    """Test that power pacgums are created in the four corners."""
    manager = make_pacgum_manager()
    manager.create_power_pacgums()

    expected_corners = {
        Position(0, 0),
        Position(0, 14),
        Position(14, 0),
        Position(14, 14),
    }

    assert manager.power_pacgum == expected_corners


def test_create_normal_pacgums() -> None:
    """Test that normal pacgums are created in the maze."""
    manager = make_pacgum_manager()
    manager.create_power_pacgums()
    manager.create_pacgums()

    assert len(manager.pacgums) > 0
    assert manager.pacgums.isdisjoint(manager.power_pacgum)
    assert manager.player not in manager.pacgums

    for position in manager.pacgums:
        assert isinstance(position, Position)
        assert len(manager.maze.get_neighbors(position.x, position.y)) > 0


def test_eat_normal_pacgum() -> None:
    """Test eating a normal pacgum only works once."""
    manager = make_pacgum_manager()
    manager.create_power_pacgums()
    manager.create_pacgums()
    position = next(iter(manager.pacgums))

    assert manager.eat_pacgum(position) is True
    assert position not in manager.pacgums
    assert manager.eat_pacgum(position) is False


def test_eat_power_pacgum() -> None:
    """Test eating a power pacgum only works once."""
    manager = make_pacgum_manager()
    manager.create_power_pacgums()
    position = next(iter(manager.power_pacgum))

    assert manager.eat_power_pacgums(position) is True
    assert position not in manager.power_pacgum
    assert manager.eat_power_pacgums(position) is False


def test_all_pacgums_eaten() -> None:
    """Test completion after all pacgums are removed."""
    manager = make_pacgum_manager()
    manager.create_power_pacgums()
    manager.create_pacgums()

    assert manager.all_pacgums_eaten() is False

    manager.pacgums.clear()
    manager.power_pacgum.clear()

    assert manager.all_pacgums_eaten() is True
