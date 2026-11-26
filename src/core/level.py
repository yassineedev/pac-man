from src.services.config import GameConfig
from src.services.spawnmanager import SpawnManager
from src.shared.game_data import Direction, GhostStatu, Position
from src.models.maze import Maze
from src.models.player import Player
from src.models.ghost import (
    Ghost,
    FirstGhost,
    SecondGhost,
    ThirdGhost,
    FourthGhost,
)
from src.models.pacgum import PacgumManager
from src.shared.errors import BackendError


class LevelManager:
    """Create, update, and reset the objects of one level"""

    def __init__(self, game_config: GameConfig) -> None:
        """Prepare the manager without creating a level yet"""
        self.game_config: GameConfig = game_config
        self.current_level: int = 0
        self.ghost_classes = [
            (FirstGhost, "red"),
            (SecondGhost, "pink"),
            (ThirdGhost, "blue"),
            (FourthGhost, "orange"),
        ]
        self.ghosts: list[Ghost] = []
        self.maze = None
        self.player = None
        self.pacgum = None
        self.level_time: float = 0.0
        self.player_move_interval = 0.2
        self.player_move_timer = 0.0
        self.ghost_move_interval = 0.5
        self.ghost_move_timer = 0.0

    def start_level(self) -> None:
        """Create all objects needed for one level"""
        # here i readed the current level
        try:
            level = self.game_config.levels[self.current_level]
        except IndexError:
            raise BackendError("The requested level does not exist.") from None
        # here i generate the maze
        try:
            self.maze: Maze = Maze(level.width, level.height)
            self.maze.generate(level.seed)
        except (ValueError, TypeError, IndexError) as error:
            raise BackendError("I could not create the level maze.") from error
        # here i should create spawnmanager
        try:
            spawn = SpawnManager(self.maze)
            player_start: Position = spawn.find_player_spawn()
            ghosts_start: dict[str, Position] = spawn.find_ghost_spawn(
                player_start
            )
        except (ValueError, TypeError, IndexError) as error:
            raise BackendError(
                "I could not find level spawn positions."
            ) from error
        # create player & ghosts
        self.player = Player(player_start, Direction.RIGHT)
        self.ghosts = []
        for n, (ghs_cls, color) in enumerate(self.ghost_classes):
            try:
                start = ghosts_start[f"ghost_{n}"]
            except KeyError as error:
                raise BackendError(
                    "The level needs four ghost spawns."
                ) from error
            self.ghosts.append(ghs_cls(start, color, self.maze))
        # create pac gums
        protected_cells = spawn.get_protected_cells() or set()
        try:
            self.pacgum = PacgumManager(
                self.maze, protected_cells, self.player.position
            )
            self.pacgum.create_pacgums()
            self.pacgum.create_power_pacgums()
        except (ValueError, TypeError, IndexError) as error:
            raise BackendError(
                "I could not create the level pacgums."
            ) from error
        # here i should set the level time
        self.level_time = level.level_max_time
        self.player_move_timer = 0.0
        self.ghost_move_timer = 0.0

    def update(self, time_passed: float, move_ghosts: bool = True) -> None:
        """Update the current level after elapsed time"""
        if isinstance(time_passed, bool) or not isinstance(
            time_passed, (int, float)
        ):
            raise BackendError("The passed time must be a number.")
        if not isinstance(move_ghosts, bool):
            raise BackendError("The ghost movement flag is not valid.")
        if time_passed < 0:
            return

        if self.maze is None or self.player is None:
            raise BackendError("The level has not been started.")

        self.level_time -= time_passed
        if self.level_time < 0:
            self.level_time = 0

        self.player_move_timer += time_passed
        if self.player_move_timer >= self.player_move_interval:
            self.player_move_timer -= self.player_move_interval
            requested_direction = self.player.choose_move(
                self.player.position
            )
            current_direction = self.player.direction
            player_position = self.player.position

            requested_is_open = self.maze.can_move(
                player_position.x,
                player_position.y,
                requested_direction.value,
            )
            current_is_open = self.maze.can_move(
                player_position.x,
                player_position.y,
                current_direction.value,
            )

            if requested_is_open:
                self.player.move(requested_direction, self.maze)
            elif current_is_open:
                self.player.move(current_direction, self.maze)

        for ghost in self.ghosts:
            if ghost.state == GhostStatu.EATEN:
                ghost.update_respawn(time_passed)

        if not move_ghosts:
            return

        self.ghost_move_timer += time_passed
        if self.ghost_move_timer < self.ghost_move_interval:
            return

        self.ghost_move_timer -= self.ghost_move_interval
        for ghost in self.ghosts:
            if ghost.state == GhostStatu.EATEN:
                continue
            direction = ghost.choose_move(self.player.position)
            ghost.move(direction, self.maze)

    def collect_pacgums(
        self,
        position: Position
    ) -> tuple[bool, bool]:
        """Collect pacgums at a position"""
        if self.pacgum is None:
            raise BackendError("The level has not been started.")
        pacgum = False
        power_pacgum = False
        if self.pacgum.eat_pacgum(position):
            pacgum = True
        elif self.pacgum.eat_power_pacgums(position):
            power_pacgum = True
        return (pacgum, power_pacgum)

    def reset_characters(self) -> None:
        """Reset the player and ghosts after losing a life"""
        if self.player is None:
            raise BackendError("The level has not been started.")
        self.player.return_to_start()
        self.player_move_timer = 0
        self.ghost_move_timer = 0
        for ghost in self.ghosts:
            ghost.make_normal()
            ghost.return_to_start()
            ghost.respawn_time_left = 0

    def reset_level_timer(self) -> None:
        """Reset the timer of the current level."""
        try:
            level = self.game_config.levels[self.current_level]
        except IndexError:
            raise BackendError("The current level does not exist.") from None
        self.level_time = level.level_max_time

    def is_level_done(self) -> bool:
        """Return whether all pacgums in the level were collected"""
        if self.pacgum is None:
            raise BackendError("The level has not been started.")
        return self.pacgum.all_pacgums_eaten()

    def next_level(self) -> bool:
        """Start the next level when one exists"""
        if self.current_level >= len(self.game_config.levels) - 1:
            return False
        self.current_level += 1
        self.start_level()
        return True
