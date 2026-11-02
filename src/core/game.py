"""Main game coordinator and state transitions."""
from src.core.states import GameState
from src.models.ghost import Ghost
from src.models.maze import Maze
from src.models.player import Player
from src.services.config import GameConfig


class Game:
    """Coordinate levels, entities, scoring and screen transitions."""

    def __init__(self, config: GameConfig) -> None:
        """Initialize game state without starting the event loop."""
        self.config = config
        self.state = GameState.MENU
        self.level_index = 0
        self.score = 0
        self.remaining_time = float(config.level_max_time)
        self.maze: Maze | None = None
        self.player: Player | None = None
        self.ghosts: list[Ghost] = []
        self.cheat_enabled = False

    def run(self) -> None:
        """Run the Pygame event/update/render loop."""
        pass

    def start(self) -> None:
        """Start a new game at the first level."""
        pass

    def load_level(self, index: int) -> None:
        """Generate and initialize a level."""
        pass

    def handle_events(self) -> None:
        """Process keyboard input and window events."""
        pass

    def update(self, delta_time: float) -> None:
        """Advance gameplay while not paused."""
        pass

    def handle_collisions(self) -> None:
        """Resolve pellets and ghost interactions."""
        pass

    def next_level(self) -> None:
        """Advance to the next level or victory."""
        pass

    def toggle_pause(self) -> None:
        """Switch between playing and paused states."""
        pass

    def apply_cheat(self, command: str) -> None:
        """Activate evaluation helpers such as skip and invincibility."""
        pass

    def finish(self, won: bool) -> None:
        """Show the result and request a highscore name."""
        pass
