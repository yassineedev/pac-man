"""Shared game constants and direction types."""
from enum import Enum

Position = tuple[int, int]


class Direction(Enum):
    """Grid movement vectors."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
