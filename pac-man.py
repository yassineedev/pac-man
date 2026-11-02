"""Command-line entry point for Pac-Man."""
import sys
from pathlib import Path

from src.core.game import Game
from src.services.config import ConfigService


def main() -> None:
    """Load the supplied configuration and launch the game."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return
    config = ConfigService().load(Path(sys.argv[1]))
    Game(config).run()


if __name__ == "__main__":
    main()
