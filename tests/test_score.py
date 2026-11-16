"""Tests for the ScoreManager class."""

from src.core.score import ScoreManager


def make_score_manager() -> ScoreManager:
    """Create a score manager with the project point values."""
    return ScoreManager(
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
    )


def test_score_starts_at_zero() -> None:
    """The score must start at zero."""
    score_manager = make_score_manager()

    assert score_manager.total_score == 0


def test_normal_pacgum_score() -> None:
    """Eating a normal pacgum adds its configured points."""
    score_manager = make_score_manager()

    score_manager.add_pacgum_score()

    assert score_manager.total_score == 10


def test_power_pacgum_score() -> None:
    """Eating a power pacgum adds its configured points."""
    score_manager = make_score_manager()

    score_manager.add_power_pacgum_score()

    assert score_manager.total_score == 50


def test_ghost_score() -> None:
    """Eating an edible ghost adds its configured points."""
    score_manager = make_score_manager()

    score_manager.add_ghost_score()

    assert score_manager.total_score == 200


def test_scores_are_added() -> None:
    """Different events add to the same total score."""
    score_manager = make_score_manager()

    score_manager.add_pacgum_score()
    score_manager.add_power_pacgum_score()
    score_manager.add_ghost_score()

    assert score_manager.total_score == 260


def test_score_reset() -> None:
    """Resetting the score returns it to zero."""
    score_manager = make_score_manager()
    score_manager.add_ghost_score()

    score_manager.reset_score()

    assert score_manager.total_score == 0
