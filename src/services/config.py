"""Read the game settings from a JSON file."""

from dataclasses import dataclass


@dataclass
class GameConfig:
    """Settings used by the game."""

    width: int = 0
    height: int = 0
    seed: int = 0


class ConfigService:
    """Read and check the game settings."""

    def load_config(self, file_path: str) -> GameConfig:
        """Read settings from a file."""
        pass

    def check_config(self, config: GameConfig) -> bool:
        """Check that settings are valid."""
        pass
