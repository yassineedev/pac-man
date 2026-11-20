from src.shared.game_data import (
    Direction,
    GameData,
    GhostData,
    GhostStatu,
    PlayerData,
)
from src.services.config import GameConfig, ConfigService
from src.services.spawnmanager import SpawnManager
from src.core.score import ScoreManager
from src.models.maze import Maze
from src.models.player import Player
from src.models.ghost import (
    Ghost,
    FirstGhost,
    SecondGhost,
    ThirdGhost,
    FourthGhost,
)
from enum import Enum
from src.models.pacgum import PacgumManager


class GameState(Enum):
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAMEOVER = "GAMEOVER"
    VICTORY = "VICTORY"


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
        self.ghosts: list[Ghost] = []
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

        self.state: GameState = GameState.MENU
        self.lives = self.game_conf.lives
        self.level = 1
        self.time_left = first_level.level_max_time
        self.power_mode = False
        self.power_mode_time_left = 0.0
        self.power_mode_duration = 10.0
        self.cheat_mode = False
        self.ghost_move_interval = 0.5
        self.ghost_move_timer = 0

    def start_game(self) -> None:
        """Start a new game from the menu, game over, or victory screen."""
        if self.state not in (
            GameState.MENU,
            GameState.GAMEOVER,
            GameState.VICTORY,
        ):
            return

        first_level = self.game_conf.levels[0]
        self.state = GameState.PLAYING
        self.lives = self.game_conf.lives
        self.level = 1
        self.time_left = first_level.level_max_time
        self.power_mode = False
        self.power_mode_time_left = 0.0
        self.cheat_mode = False

        self.score_manager.reset_score()
        self.player.reset_position()
        for ghost in self.ghosts:
            ghost.reset()

        self.pac_gums.pacgums.clear()
        self.pac_gums.create_power_pacgums()
        self.pac_gums.create_pacgums()

    def update(self, time_passed: float) -> None:
        """Update timers, characters, pacgums, and collisions."""
        if self.state is not GameState.PLAYING:
            return
        if time_passed < 0:
            return
        self.ghost_move_timer += time_passed
        self.time_left -= time_passed
        if self.time_left <= 0:
            self.time_left = 0
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAMEOVER
                return

            self.player.reset_position()
            for ghost in self.ghosts:
                ghost.reset()
            self.power_mode = False
            self.power_mode_time_left = 0.0
            current_level = self.game_conf.levels[self.level - 1]
            self.time_left = current_level.level_max_time
            return

        if self.power_mode:
            self.power_mode_time_left -= time_passed
            if self.power_mode_time_left <= 0:
                self.power_mode_time_left = 0
                self.power_mode = False
                for ghost in self.ghosts:
                    ghost.make_normal()

        if self.pac_gums.eat_pacgum(self.player.position):
            self.score_manager.add_pacgum_score()

        if self.pac_gums.eat_power_pacgums(self.player.position):
            self.score_manager.add_power_pacgum_score()
            self.power_mode = True
            self.power_mode_time_left = self.power_mode_duration
            for ghost in self.ghosts:
                ghost.make_weak()
        if self.ghost_move_timer >= self.ghost_move_interval:
            self.ghost_move_timer -= self.ghost_move_interval
            for ghost in self.ghosts:
                direction = ghost.choose_move(self.player.position)
                ghost.move(direction, self.maze)

        for ghost in self.ghosts:
            if self.player.position != ghost.position:
                continue
            if ghost.state == GhostStatu.WEAK:
                ghost.get_eaten()
                self.score_manager.add_ghost_score()
                continue
            if self.cheat_mode:
                continue

            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAMEOVER
                return

            self.player.reset_position()
            for other_ghost in self.ghosts:
                other_ghost.reset()
            break

        if self.pac_gums.all_pacgums_eaten():
            self.state = GameState.VICTORY

    def move_player(self, direction: Direction) -> None:
        """Move Pac-Man when the game is being played."""
        if self.state != GameState.PLAYING:
            return
        self.player.set_direction(direction)
        self.player.move(direction, self.maze)

    def pause_game(self) -> None:
        """Pause an active game."""
        # Logic to write:
        # - Change the state only when it is currently ``playing``.
        # - Do not update the timer or characters while paused.
        self.state = GameState.PAUSED

    def resume_game(self) -> None:
        """Return from the paused state to the playing state."""
        # Logic to write:
        # - Change the state only when it is currently ``paused``.
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

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
        self.state = GameState.MENU
        self.lives = self.game_conf.lives
        self.score_manager.total_score = 0
        self.time_left = self.game_conf.levels[0].level_max_time
        self.pac_gums.create_power_pacgums()
        self.pac_gums.create_pacgums()

    def get_game_data(self) -> GameData:
        """Return an immutable snapshot for the UI.

        Build ``PlayerData`` and ``GhostData`` values here. Copy the maze,
        pacgum positions, score, lives, level, timer, and state into a
        ``GameData`` object. The UI must receive data, not game objects.
        """
        ghost_data = []
        for number, ghost in enumerate(self.ghosts):
            ghost_data.append(
                GhostData(
                    name=f"ghost_{number + 1}",
                    position=ghost.position,
                    direction=ghost.direction,
                    state=ghost.state.value,
                )
            )

        return GameData(
            maze=tuple(tuple(row) for row in self.maze.grid),
            player=PlayerData(
                position=self.player.position,
                direction=self.player.direction,
            ),
            ghosts=tuple(ghost_data),
            pacgums=tuple(self.pac_gums.pacgums),
            power_pacgums=tuple(self.pac_gums.power_pacgum),
            score=self.score_manager.total_score,
            lives=self.lives,
            level=self.level,
            time_left=self.time_left,
            state=self.state.value,
            cheat_mode=self.cheat_mode,
        )

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
