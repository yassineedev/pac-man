"""Read and save the best scores."""

from dataclasses import dataclass


@dataclass
class HighScore:
    """One player name and score."""

    name: str
    score: int


class HighScoreService:
    """Keep the ten best scores in a JSON file."""

    def load_scores(self) -> list[HighScore]:
        """Read saved scores."""
        pass

    def save_score(self, name: str, score: int) -> None:
        """Save a player's score."""
        pass

    def get_top_scores(self) -> list[HighScore]:
        """Get the ten best scores."""
        pass
