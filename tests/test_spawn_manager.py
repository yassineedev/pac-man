"""Test player spawn positions."""

from src.models.maze import Maze
from src.services.spawnmanager import SpawnManager


def test_spawn_positions() -> None:
    """Test player and ghost positions for different maze sizes."""
    maze_sizes = [(45, 45), (44, 44), (45, 44), (44, 45), (9, 9)]

    for width, height in maze_sizes:
        maze = Maze(width, height)
        maze.generate(seed=0)

        spawn_manager = SpawnManager(maze)
        player_spawn = spawn_manager.find_player_spawn()
        ghosts = spawn_manager.find_ghost_spawn(player_spawn)
        protected = spawn_manager.get_protected_cells() or set()

        assert player_spawn not in protected
        assert spawn_manager.is_valid_spawn(player_spawn)
        assert len(ghosts) == 4
        assert len(set(ghosts.values())) == 4
        assert player_spawn not in ghosts.values()

        for ghost_spawn in ghosts.values():
            assert spawn_manager.is_valid_spawn(ghost_spawn)


if __name__ == "__main__":
    test_spawn_positions()
    print("\nAll player spawn tests passed!")
