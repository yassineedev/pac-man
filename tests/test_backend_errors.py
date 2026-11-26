"""Test clear errors from the backend."""

import json

import pytest

from src.core.game import Game
from src.services.config import ConfigService
from src.shared.errors import BackendError


def test_missing_config_raises_clear_error() -> None:
    """A missing config file should stop the game with a clear error."""
    with pytest.raises(BackendError, match="read the config"):
        ConfigService().load_config("missing-config.json")


def test_invalid_config_value_raises_clear_error(tmp_path) -> None:
    """A bad config value should explain the problem."""
    config_path = tmp_path / "config.json"
    values = {
        "highscore_filename": "scores.json",
        "lives": 3,
        "pacgum": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "levels": [
            {"width": 6, "height": 7, "seed": 42, "level_max_time": 90}
        ],
    }
    config_path.write_text(json.dumps(values), encoding="utf-8")

    with pytest.raises(BackendError, match="width.*at least 7"):
        ConfigService().load_config(str(config_path))


def test_invalid_update_time_raises_clear_error() -> None:
    """The game should reject a value that is not elapsed time."""
    game = Game("config.json")
    game.start_game()

    with pytest.raises(BackendError, match="passed time"):
        game.update("fast")
