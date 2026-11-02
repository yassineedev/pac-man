"""Pygame rendering for gameplay."""
import pygame

from src.core.game import Game
from src.models.ghost import Ghost
from src.models.maze import Maze
from src.models.player import Player


class GameView:
    """Draw the maze, entities, pellets and heads-up display."""

    def draw(self, surface: pygame.Surface, game: Game) -> None:
        """Draw one gameplay frame."""
        pass

    def draw_maze(self, surface: pygame.Surface, maze: Maze) -> None:
        """Draw walls and collectible pellets."""
        pass

    def draw_player(self, surface: pygame.Surface, player: Player) -> None:
        """Draw Pac-Man."""
        pass

    def draw_ghosts(self, surface: pygame.Surface, ghosts: list[Ghost]) -> None:
        """Draw all four ghosts."""
        pass

    def draw_hud(self, surface: pygame.Surface, game: Game) -> None:
        """Draw score, lives, level and time."""
        pass
