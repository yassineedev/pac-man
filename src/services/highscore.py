"""Persistent top-ten highscore storage."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScoreEntry:
    """A validated highscore record."""

    name: str
    score: int


class HighscoreService:
    """Read, sanitize, rank and save score records."""

    def __init__(self, path: Path) -> None:
        """Store the highscore file path."""
        self.path = path

    def load(self) -> list[ScoreEntry]:
        """Read up to ten valid scores; tolerate missing or corrupt files."""
        pass

    def add(self, name: str, score: int) -> None:
        """Validate a name and non-negative score, then save the top ten."""
        pass

    def save(self, entries: list[ScoreEntry]) -> None:
        """Persist scores safely."""
        pass

    def validate_name(self, name: str) -> bool:
        """Accept at most ten alphanumeric or space characters."""
        pass
