from src.shared.game_data import Direction, GameData
from src.services.config import GameConfig, ConfigService
from src.services.spawnmanager import SpawnManager
from src.core.score import ScoreManager
from src.models.maze import Maze
from src.models.player import Player
from src.models.ghost import (
    FirstGhost,
    SecondGhost,
    ThirdGhost,
    FourthGhost,
)
from src.models.pacgum import PacgumManager


class Game:
    """Keep all game objects and game rules together."""

    def __init__(self, config_path: str) -> None:
        """Create the main objects needed for a new game."""
        config_service = ConfigService()
        self.game_conf: GameConfig = config_service.load_config(config_path)
        first_level = self.game_conf.levels[0]

        self.maze = Maze(first_level.width, first_level.height)
        self.maze.generate(first_level.seed)

        self.spawn_manager = SpawnManager(self.maze)
        player_start = self.spawn_manager.find_player_spawn()
        self.player = Player(player_start, Direction.RIGHT)

        ghost_starts = self.spawn_manager.find_ghost_spawn(player_start)
        ghost_classes = [
            (FirstGhost, "red"),
            (SecondGhost, "pink"),
            (ThirdGhost, "blue"),
            (FourthGhost, "orange"),
        ]
        self.ghosts = []
        for number, (ghost_class, color) in enumerate(ghost_classes):
            start = ghost_starts[f"ghost_{number}"]
            self.ghosts.append(ghost_class(start, color, self.maze))

        protected_cells = self.spawn_manager.get_protected_cells() or set()
        protected_cells.update(ghost_starts.values())
        self.pac_gums = PacgumManager(
            maze=self.maze,
            protected_positions=protected_cells,
            player_start=player_start,
        )
        self.pac_gums.create_power_pacgums()
        self.pac_gums.create_pacgums()

        self.score_manager = ScoreManager(
            points_per_pacgum=self.game_conf.points_per_pacgum,
            points_per_super_pacgum=self.game_conf.points_per_super_pacgum,
            points_per_ghost=self.game_conf.points_per_ghost,
        )

        self.state = "menu"
        self.lives = self.game_conf.lives
        self.level = 1
        self.time_left = first_level.level_max_time
        self.cheat_mode = False

    def start_game(self) -> None:
        """Start a new game.

        Logic to write:
        - Change the state from ``menu`` to ``playing``.
        - Reset the timer for the current level.
        - Make sure the player and ghosts are at their start positions.
        """
        pass

    def update(self, time_passed: float) -> None:
        """Update all active game rules after elapsed time.

        Implementation order:
        1. Return immediately unless the state is ``playing``.
        2. Decrease ``time_left`` by ``time_passed``.
        3. Move every ghost by calling ``choose_move`` and ``move``.
        4. Check whether Pac-Man ate a normal or power pacgum.
        5. Check player-ghost collisions.
        6. Check level completion, timeout, game over, or victory.
        """
        # Logic to write:
        # - Stop immediately if the state is not ``playing``.
        # - Decrease the level timer using ``time_passed``.
        # - Ask every ghost to choose and perform a move.
        # - Check pacgum and power-pacgum collection.
        # - Check collisions between the player and ghosts.
        # - Check timeout, level completion, game over, and victory.
        pass

    def move_player(self, direction: Direction) -> None:
        """Move Pac-Man when the game is being played."""
        # Logic to write:
        # - Ignore input when the state is not ``playing``.
        # - Store the requested direction in the Player.
        # - Move the player through the Maze.
        # - Do not move through walls or outside the maze.
        pass

    def pause_game(self) -> None:
        """Pause an active game."""
        # Logic to write:
        # - Change the state only when it is currently ``playing``.
        # - Do not update the timer or characters while paused.
        pass

    def continue_game(self) -> None:
        """Continue a paused game."""
        # Logic to write:
        # - This method can call ``resume_game``.
        # - Or keep only one method and remove this alias.
        pass

    def resume_game(self) -> None:
        """Return from the paused state to the playing state."""
        # Logic to write:
        # - Change the state only when it is currently ``paused``.
        pass

    def restart_game(self) -> None:
        """Reset the game to a new menu state.

        The complete version should recreate the current level, reset the
        score and lives, and put every character at its starting position.
        """
        # Logic to write:
        # - Reset the state to ``menu`` or ``playing`` according to the UI.
        # - Reset lives, level, score, and timer.
        # - Reset the player and every ghost.
        # - Recreate the pacgums for the new level.
        pass

    def get_game_data(self) -> GameData:
        """Return an immutable snapshot for the UI.

        Build ``PlayerData`` and ``GhostData`` values here. Copy the maze,
        pacgum positions, score, lives, level, timer, and state into a
        ``GameData`` object. The UI must receive data, not game objects.
        """
        # Logic to write:
        # - Create one immutable PlayerData object.
        # - Create one immutable GhostData object for every ghost.
        # - Convert the maze grid and positions to snapshot data.
        # - Return GameData with score, lives, level, timer, state,
        #   and cheat_mode.
        pass

    def use_cheat(self, cheat_name: str) -> None:
        """Apply a named peer-review cheat.

        Cheats should be handled in this class only. Later, support the
        agreed names such as ``invincible``, ``freeze_ghosts``,
        ``extra_life``, ``skip_level``, and ``fast_player``.
        """
        # Logic to write:
        # - Compare ``cheat_name`` with the agreed cheat commands.
        # - ``extra_life`` increases lives.
        # - ``invincible`` prevents dangerous collision effects.
        # - ``freeze_ghosts`` stops ghost movement.
        # - ``skip_level`` completes the current level.
        # - ``fast_player`` changes the movement speed.
        pass
