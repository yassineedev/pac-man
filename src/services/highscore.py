"""Read and save the best scores."""

import json
from pathlib import Path

from pydantic import BaseModel, ValidationError, conint, constr

from src.shared.errors import BackendError


HighScoreName = constr(
    strict=True,
    strip_whitespace=True,
    min_length=1,
    max_length=10,
    pattern=r"^[A-Za-z0-9 ]+$",
)
HighScoreValue = conint(strict=True, ge=0)


class HighScore(BaseModel):
    """One player name and score."""

    name: HighScoreName
    score: HighScoreValue

    @classmethod
    def model_validate_score(cls, name: str, score: int) -> "HighScore":
        """Create a validated highscore."""
        try:
            return cls(name=name, score=score)
        except ValidationError as error:
            detail = error.errors()[0]
            field = detail["loc"][0]
            error_type = detail["type"]
            if field == "name":
                if error_type == "string_too_long":
                    message = (
                        "The player name must have 10 characters or less."
                    )
                elif error_type == "string_pattern_mismatch":
                    message = (
                        "The player name can use letters, numbers, "
                        "and spaces only."
                    )
                else:
                    message = "The player name is not valid."
            elif error_type == "greater_than_equal":
                message = "The score cannot be negative."
            else:
                message = "The score must be a whole number."
            raise BackendError(message) from error


class HighScoreService:
    """Keep the ten best scores in a JSON file."""

    MAX_SCORES = 10

    def __init__(self, score_path: str) -> None:
        if not isinstance(score_path, str) or not score_path:
            raise BackendError("The highscore path must be a string.")
        self.score_file = Path(score_path)
        self.scores: list[HighScore] = []

    def _read_file(self) -> list[object]:
        """Read raw score data or return an empty list."""
        if not self.score_file.exists():
            return []
        try:
            with self.score_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return data

    def load_scores(self) -> list[HighScore]:
        """Read valid saved scores."""
        loaded_scores: list[HighScore] = []
        for item in self._read_file():
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            score = item.get("score")
            try:
                highscore = HighScore.model_validate_score(name, score)
            except (BackendError, TypeError):
                continue
            loaded_scores.append(highscore)

        self.scores = self._sort_scores(loaded_scores)
        return list(self.scores)

    def _sort_scores(self, scores: list[HighScore]) -> list[HighScore]:
        """Sort scores and keep only the ten best."""
        scores.sort(key=self._get_score, reverse=True)
        return scores[: self.MAX_SCORES]

    def _get_score(self, highscore: HighScore) -> int:
        """Return one score for sorting."""
        return highscore.score

    def save_score(self, name: str, score: int) -> None:
        """Validate and save one player's score."""
        new_score = HighScore.model_validate_score(name, score)
        current_scores = self.load_scores()
        current_scores.append(new_score)
        self.scores = self._sort_scores(current_scores)

        try:
            self.score_file.parent.mkdir(parents=True, exist_ok=True)
            with self.score_file.open("w", encoding="utf-8") as file:
                json.dump(
                    [score.model_dump() for score in self.scores],
                    file,
                    indent=2,
                )
                file.write("\n")
        except OSError as error:
            raise BackendError("I could not save the highscores.") from error

    def get_top_scores(self) -> list[HighScore]:
        """Return the current top ten scores."""
        return list(self.scores)
