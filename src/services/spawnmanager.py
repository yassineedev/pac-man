"""Find the starting positions in the maze."""

from src.models.maze import Maze
from src.shared.game_data import Position
from src.shared.errors import BackendError


class SpawnManager:
    """Find positions for Pac-Man and the ghosts."""

    def __init__(self, maze: Maze) -> None:
        """Create a spawn manager for a maze."""
        self.maze = maze
        self.width = maze.width
        self.height = maze.height

    def get_protected_cells(self) -> set[tuple[int, int]] | None:
        """Return the protected cells in the middle of the maze."""
        protected_layout = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        if len(protected_layout) * 2 > self.height:
            return None
        if len(protected_layout[0]) * 2 > self.width:
            return None

        protected_cells: set[tuple[int, int]] = set()
        start_y = (self.height - len(protected_layout)) // 2
        start_x = (self.width - len(protected_layout[0])) // 2

        for y in range(len(protected_layout)):
            for x in range(len(protected_layout[y])):
                if protected_layout[y][x] == 1:
                    protected_cells.add((start_x + x, start_y + y))

        return protected_cells

    def find_player_spawn(self) -> Position:
        """Find a valid position near the middle of the maze."""
        if not self.maze.grid:
            raise ValueError("Maze not generated.")

        middle_x = self.width // 2
        middle_y = self.height // 2
        positions = [
            Position(middle_x, middle_y),
            Position(middle_x - 1, middle_y),
            Position(middle_x, middle_y - 1),
            Position(middle_x - 1, middle_y - 1),
        ]
        protected_cells = self.get_protected_cells() or set()

        for position in positions:
            coordinates = (position.x, position.y)
            if coordinates in protected_cells:
                continue
            if not self.maze.is_inside(position.x, position.y):
                continue
            if len(self.maze.get_neighbors(position.x, position.y)) == 0:
                continue
            return position

        # Search the maze if the preferred middle cells cannot be used.
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in protected_cells:
                    continue
                if len(self.maze.get_neighbors(x, y)) == 0:
                    continue
                return Position(x, y)

        raise BackendError("I could not find a player spawn position.")

    def find_ghost_spawn(
            self,
            player_spawn: Position | None = None
    ) -> dict[str, Position]:
        """Find four different ghost positions near the corners."""
        if not self.maze.grid:
            raise ValueError("Maze not generated.")

        if player_spawn is None:
            player_spawn = self.find_player_spawn()

        corners = [
            Position(0, 0),
            Position(0, self.height - 1),
            Position(self.width - 1, 0),
            Position(self.width - 1, self.height - 1),
        ]
        used_positions = {player_spawn}
        ghosts: dict[str, Position] = {}

        for number, corner in enumerate(corners):
            position = corner

            if position in used_positions:
                position = self.find_free_position(used_positions)
            elif not self.maze.is_inside(position.x, position.y):
                position = self.find_free_position(used_positions)
            elif len(self.maze.get_neighbors(position.x, position.y)) == 0:
                position = self.find_free_position(used_positions)

            if position in used_positions:
                continue

            ghosts[f"ghost_{number}"] = position
            used_positions.add(position)

        if len(ghosts) != 4:
            raise BackendError("I could not find four ghost positions.")
        return ghosts

    def find_free_position(self, used_positions: set[Position]) -> Position:
        """Find another corridor cell not already used."""
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                if position in used_positions:
                    continue
                if len(self.maze.get_neighbors(x, y)) == 0:
                    continue
                return position

        raise BackendError("I could not find a free spawn position.")
