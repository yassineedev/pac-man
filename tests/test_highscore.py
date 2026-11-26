"""Tests for persistent highscores."""

import json

import pytest

from src.services.highscore import HighScoreService
from src.shared.errors import BackendError


def test_highscores_are_sorted_and_limited(tmp_path) -> None:
    """Only the ten best valid scores should remain."""
    path = tmp_path / "scores.json"
    service = HighScoreService(str(path))

    for number in range(12):
        service.save_score(f"P{number}", number)

    scores = service.load_scores()

    assert len(scores) == 10
    assert scores[0].score == 11
    assert scores[-1].score == 2


def test_invalid_saved_rows_are_ignored(tmp_path) -> None:
    """Broken rows should not stop valid scores from loading."""
    path = tmp_path / "scores.json"
    path.write_text(
        json.dumps([
            {"name": "Good", "score": 20},
            {"name": "Bad!", "score": 30},
            {"name": "Wrong", "score": -1},
        ]),
        encoding="utf-8",
    )

    scores = HighScoreService(str(path)).load_scores()

    assert [(score.name, score.score) for score in scores] == [("Good", 20)]


@pytest.mark.parametrize("name", ["", "TooLongName", "Bad!"])
def test_invalid_name_raises_error(tmp_path, name: str) -> None:
    """Names outside the rules should be rejected."""
    service = HighScoreService(str(tmp_path / "scores.json"))

    with pytest.raises(BackendError):
        service.save_score(name, 10)
