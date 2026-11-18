"""Load and validate the game configuration."""

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LevelConfig:
    """Settings for one level."""

    width: int
    height: int
    seed: int
    level_max_time: int


@dataclass(frozen=True)
class GameConfig:
    """All settings used by the game engine."""

    highscore_filename: str
    levels: tuple[LevelConfig, ...]
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int


class ConfigService:
    """Read comments, parse JSON, and validate game settings."""

    def _read_file(self, file_path: str) -> str:
        """Return the configuration file contents."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _strip_comments(self, data: str) -> str:
        """Remove full-line comments before reading JSON."""
        lines = []
        for line in data.splitlines():
            stripped_line = line.lstrip()
            if stripped_line.startswith("#"):
                lines.append("")
            elif stripped_line.startswith("//"):
                lines.append("")
            else:
                lines.append(line)
        return "\n".join(lines)

    def _read_integer(
        self,
        values: dict[str, Any],
        name: str,
        default: int,
        minimum: int = 0,
    ) -> int:
        """Read one integer or return its safe default."""
        value = values.get(name, default)
        if isinstance(value, bool) or not isinstance(value, int):
            return default
        if value < minimum:
            return default
        return value

    def _parse_level(
        self,
        values: dict[str, Any],
        default_seed: int,
    ) -> LevelConfig:
        """Parse one level object."""
        return LevelConfig(
            width=self._read_integer(values, "width", 25, 14),
            height=self._read_integer(values, "height", 25, 10),
            seed=self._read_integer(values, "seed", default_seed, 1),
            level_max_time=self._read_integer(
                values, "level_max_time", 90, 1
            ),
        )

    def load_config(self, file_path: str) -> GameConfig:
        """Parse a file and return validated game settings."""
        data = self._strip_comments(self._read_file(file_path))
        parsed = json.loads(data)
        if not isinstance(parsed, dict):
            raise ValueError("The configuration root must be an object.")

        levels_data = parsed.get("levels", [])
        if not isinstance(levels_data, list) or not levels_data:
            levels_data = [{}]

        levels = []
        for index, level_data in enumerate(levels_data):
            if not isinstance(level_data, dict):
                level_data = {}
            levels.append(self._parse_level(level_data, index + 1))

        highscore_filename = parsed.get(
            "highscore_filename", "data/highscores.json"
        )
        if not isinstance(highscore_filename, str) or not highscore_filename:
            highscore_filename = "data/highscores.json"

        return GameConfig(
            highscore_filename=highscore_filename,
            levels=tuple(levels),
            lives=self._read_integer(parsed, "lives", 3, 1),
            pacgum=self._read_integer(parsed, "pacgum", 42, 0),
            points_per_pacgum=self._read_integer(
                parsed, "points_per_pacgum", 10, 0
            ),
            points_per_super_pacgum=self._read_integer(
                parsed, "points_per_super_pacgum", 50, 0
            ),
            points_per_ghost=self._read_integer(
                parsed, "points_per_ghost", 200, 0
            ),
        )
