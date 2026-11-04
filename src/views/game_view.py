"""Draw the game with Pygame."""

from src.shared.game_data import GameData


class GameView:
    """Draw the maze, player, ghosts, and score."""

    def __init__(self) -> None:
        pass

    def draw_game(self, game_data: GameData) -> None:
        """Draw the current game."""
        pass

    def draw_maze(self, game_data: GameData) -> None:
        """Draw walls and pacgums."""
        pass

    def draw_player(self, game_data: GameData) -> None:
        """Draw Pac-Man."""
        pass

    def draw_ghosts(self, game_data: GameData) -> None:
        """Draw all ghosts."""
        pass

    def draw_score(self, game_data: GameData) -> None:
        """Draw score, lives, level, and time."""
        pass
