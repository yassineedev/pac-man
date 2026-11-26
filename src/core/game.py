from src.shared.game_data import (
    Direction,
    GameData,
    GhostData,
    GhostStatu,
    PlayerData,
)
from src.services.config import GameConfig, ConfigService
from src.core.score import ScoreManager
from enum import Enum
from src.core.level import LevelManager
from src.shared.errors import BackendError
from src.services.highscore import HighScoreService


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
        if not isinstance(config_path, str) or not config_path:
            raise BackendError("The config path must be a non-empty string.")
        config_service = ConfigService()
        self.game_conf: GameConfig = config_service.load_config(config_path)
        self.highscore_service = HighScoreService(
            self.game_conf.highscore_filename
        )
        self.highscore_service.load_scores()
        self.level_manager = LevelManager(self.game_conf)
        self.level_manager.start_level()

        self.score_manager = ScoreManager(
            points_per_pacgum=self.game_conf.points_per_pacgum,
            points_per_super_pacgum=self.game_conf.points_per_super_pacgum,
            points_per_ghost=self.game_conf.points_per_ghost,
        )

        self.state: GameState = GameState.MENU
        self.lives = self.game_conf.lives
        self.power_mode = False
        self.power_mode_time_left = 0.0
        self.power_mode_duration = 10.0
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False
        self.fast_player = False
        self.normal_player_interval = self.level_manager.player_move_interval
        self.fast_player_interval = 0.1
        self.protection_duration = 2
        self.protection_left = 0.0
        self.score_submitted = False

    def start_game(self) -> None:
        """Start a new game from the menu, game over, or victory screen."""
        if self.state not in (
            GameState.MENU,
            GameState.GAMEOVER,
            GameState.VICTORY,
        ):
            return

        self.state = GameState.PLAYING
        self.lives = self.game_conf.lives
        self.power_mode = False
        self.power_mode_time_left = 0.0
        self.protection_left = 0.0
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False
        self.fast_player = False
        self.score_submitted = False
        self.highscore_service.load_scores()

        self.score_manager.reset_score()
        self.level_manager.current_level = 0
        self.level_manager.start_level()

    def update(self, time_passed: float) -> None:
        """Update timers, characters, pacgums, and collisions."""
        if isinstance(time_passed, bool) or not isinstance(
            time_passed, (int, float)
        ):
            raise BackendError("The passed time must be a number.")
        if self.state != GameState.PLAYING:
            return

        if time_passed < 0:
            return

        player_position_before = self.level_manager.player.position
        ghost_positions_before = {
            id(ghost): ghost.position
            for ghost in self.level_manager.ghosts
        }

        self.level_manager.update(time_passed, not self.ghosts_frozen)

        player = self.level_manager.player
        ghosts = self.level_manager.ghosts

        # update protection time if it's enabled
        if self.protection_left > 0:
            self.protection_left -= time_passed
            if self.protection_left <= 0:
                self.protection_left = 0.0
        # power mode logic
        if self.power_mode:
            self.power_mode_time_left -= time_passed
            if self.power_mode_time_left <= 0:
                self.power_mode_time_left = 0
                self.power_mode = False
                for ghost in ghosts:
                    if ghost.state == GhostStatu.WEAK:
                        ghost.make_normal()
        normal_eaten, power_eaten = self.level_manager.collect_pacgums(
            player.position
        )
        if normal_eaten:
            self.score_manager.add_pacgum_score()
        if power_eaten:
            self.score_manager.add_power_pacgum_score()
            self.power_mode = True
            self.power_mode_time_left = self.power_mode_duration
            for ghost in ghosts:
                if ghost.state == GhostStatu.NORMAL:
                    ghost.make_weak()
        # check if there is a collision between the player and the ghosts
        for ghost in ghosts:
            same_cell = player.position == ghost.position
            crossed_paths = (
                player_position_before == ghost.position
                and player.position == ghost_positions_before[id(ghost)]
            )
            if not same_cell and not crossed_paths:
                continue
            if ghost.state == GhostStatu.WEAK:
                ghost.get_eaten()
                self.score_manager.add_ghost_score()
                continue
            if ghost.state == GhostStatu.EATEN:
                continue
            if self.invincible:
                continue
            if self.protection_left > 0:
                continue
            self.lives -= 1
            self.protection_left = self.protection_duration
            self.level_manager.reset_characters()
            if self.lives <= 0:
                self.state = GameState.GAMEOVER
                return
            break

        if self.level_manager.level_time <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAMEOVER
                return

            self.level_manager.reset_characters()
            self.level_manager.reset_level_timer()
            self.power_mode = False
            self.power_mode_time_left = 0.0
            return

        if self.level_manager.is_level_done():
            if self.level_manager.next_level():
                self.power_mode = False
                self.power_mode_time_left = 0.0
                self._apply_player_speed()
            else:
                self.state = GameState.VICTORY

    def move_player(self, direction: Direction) -> None:
        """Move Pac-Man when the game is being played."""
        if self.state != GameState.PLAYING:
            return
        if not isinstance(direction, Direction):
            raise BackendError("The player direction is not valid.")
        self.level_manager.player.set_direction(direction)

    def pause_game(self) -> None:
        """Pause an active game."""
        self.state = GameState.PAUSED

    def resume_game(self) -> None:
        """Return from the paused state to the playing state."""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def use_cheat(self, cheat_name: str) -> None:
        """Apply a cheat used for peer review and debugging."""
        if self.state != GameState.PLAYING:
            return
        valid_cheats = {
            "invincible",
            "freeze_ghosts",
            "extra_life",
            "skip_level",
            "fast_player",
        }
        if cheat_name not in valid_cheats:
            raise BackendError("That cheat is not available.")

        self.cheat_mode = True

        if cheat_name == "invincible":
            self.invincible = not self.invincible
        elif cheat_name == "freeze_ghosts":
            self.ghosts_frozen = not self.ghosts_frozen
        elif cheat_name == "extra_life":
            self.lives += 1
        elif cheat_name == "skip_level":
            if self.level_manager.next_level():
                self.power_mode = False
                self.power_mode_time_left = 0.0
                self._apply_player_speed()
            else:
                self.state = GameState.VICTORY
        elif cheat_name == "fast_player":
            self.fast_player = not self.fast_player
            self._apply_player_speed()
        else:
            return

    def _apply_player_speed(self) -> None:
        """Apply the normal or cheat player movement interval."""
        if self.fast_player:
            self.level_manager.player_move_interval = (
                self.fast_player_interval
            )
        else:
            self.level_manager.player_move_interval = (
                self.normal_player_interval
            )

    def save_final_score(self, player_name: str) -> None:
        """Save the score after a win or a game over."""
        if self.state not in (GameState.GAMEOVER, GameState.VICTORY):
            raise BackendError("The game has not ended yet.")
        if self.score_submitted:
            raise BackendError("This score was already saved.")
        self.highscore_service.save_score(
            player_name,
            self.score_manager.total_score,
        )
        self.highscore_service.load_scores()
        self.score_submitted = True

    def get_highscores(self) -> list[tuple[str, int]]:
        """Return highscore names and values for the menu."""
        return [
            (highscore.name, highscore.score)
            for highscore in self.highscore_service.get_top_scores()
        ]

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
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False
        self.fast_player = False
        self.score_submitted = False
        self.level_manager.current_level = 0
        self.level_manager.start_level()

    def get_game_data(self) -> GameData:
        """Return an immutable snapshot for the UI.

        Build ``PlayerData`` and ``GhostData`` values here. Copy the maze,
        pacgum positions, score, lives, level, timer, and state into a
        ``GameData`` object. The UI must receive data, not game objects.
        """
        ghost_data = []
        for number, ghost in enumerate(self.level_manager.ghosts):
            ghost_data.append(
                GhostData(
                    name=f"ghost_{number + 1}",
                    position=ghost.position,
                    direction=ghost.direction,
                    state=ghost.state.value,
                )
            )

        return GameData(
            maze=tuple(tuple(row) for row in self.level_manager.maze.grid),
            player=PlayerData(
                position=self.level_manager.player.position,
                direction=self.level_manager.player.direction,
            ),
            ghosts=tuple(ghost_data),
            pacgums=tuple(self.level_manager.pacgum.pacgums),
            power_pacgums=tuple(self.level_manager.pacgum.power_pacgum),
            score=self.score_manager.total_score,
            lives=self.lives,
            level=self.level_manager.current_level + 1,
            time_left=self.level_manager.level_time,
            state=self.state.value,
            cheat_mode=self.cheat_mode,
            player_move_time=self.level_manager.player_move_interval,
            ghost_move_time=self.level_manager.ghost_move_interval,
            power_mode=self.power_mode,
            power_mode_time_left=self.power_mode_time_left,
            invincible=self.invincible,
            ghosts_frozen=self.ghosts_frozen,
            fast_player=self.fast_player,
            highscores=tuple(self.get_highscores()),
        )

    # def use_cheat(self, cheat_name: str) -> None:
    #     """Apply a named peer-review cheat.

    #     Cheats should be handled in this class only. Later, support the
    #     agreed names such as ``invincible``, ``freeze_ghosts``,
    #     ``extra_life``, ``skip_level``, and ``fast_player``.
    #     """
    #     # Logic to write:
    #     # - Compare ``cheat_name`` with the agreed cheat commands.
    #     # - ``extra_life`` increases lives.
    #     # - ``invincible`` prevents dangerous collision effects.
    #     # - ``freeze_ghosts`` stops ghost movement.
    #     # - ``skip_level`` completes the current level.
    #     # - ``fast_player`` changes the movement speed.
    #     if self.state != GameState.
    #     pass
