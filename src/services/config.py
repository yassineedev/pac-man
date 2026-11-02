"""Load and validate JSON configuration with hash comments."""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LevelConfig:
    """Dimensions of a generated level."""

    width: int = 15
    height: int = 15


@dataclass
class GameConfig:
    """Validated game settings with safe defaults."""

    lives: int = 3
    seed: int = 42
    level_max_time: int = 90
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    highscore_filename: str = "data/highscores.json"
    levels: list[LevelConfig] = field(
        default_factory=lambda: [LevelConfig() for _ in range(10)]
    )


class ConfigService:
    """Read configuration, sanitize values and report recoverable errors."""

    def load(self, path: Path) -> GameConfig:
        """Read a configuration file without exposing a traceback."""
        pass

    def strip_comments(self, text: str) -> str:
        """Ignore lines whose first non-space character is '#'."""
        pass

    def validate(self, raw: dict[str, object]) -> GameConfig:
        """Clamp invalid settings and ignore unknown keys."""
        pass
