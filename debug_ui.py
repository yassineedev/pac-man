"""Small Pygame window for testing the game engine."""

from dataclasses import dataclass

import pygame

from src.core.game import Game, GameState
from src.models.maze import Maze
from src.shared.game_data import (
    Direction,
    GameData,
    GhostData,
    Position,
)
from src.shared.errors import BackendError


CELL_SIZE = 24
SIDE_PANEL_WIDTH = 220
PANEL_HEIGHT = 520
BACKGROUND = (8, 8, 24)
CELL_COLOR = (12, 12, 42)
WALL_COLOR = (35, 90, 220)
PACGUM_COLOR = (245, 245, 245)
POWER_COLOR = (255, 170, 40)
PLAYER_COLOR = (255, 220, 0)
TEXT_COLOR = (235, 235, 235)


@dataclass
class SmoothPosition:
    """Interpolate a character between two maze cells."""

    x: float
    y: float
    target_x: int
    target_y: int
    progress: float = 1.0

    @classmethod
    def from_position(cls, position: Position) -> "SmoothPosition":
        """Create a render position from a maze position."""
        return cls(
            float(position.x),
            float(position.y),
            position.x,
            position.y,
        )

    def update(self, position: Position, time_passed: float,
               movement_time: float) -> tuple[float, float]:
        """Move the visual position towards the logical position."""
        if (position.x, position.y) != (self.target_x, self.target_y):
            self.x = self.x + (self.target_x - self.x) * self.progress
            self.y = self.y + (self.target_y - self.y) * self.progress
            self.target_x = position.x
            self.target_y = position.y
            self.progress = 0.0

        if movement_time > 0:
            progress_step = time_passed / movement_time
            self.progress = min(1.0, self.progress + progress_step)

        start_x = self.x
        start_y = self.y
        return (
            start_x + (self.target_x - start_x) * self.progress,
            start_y + (self.target_y - start_y) * self.progress,
        )


def get_render_position(
    render_positions: dict[str, SmoothPosition],
    character_name: str,
    position: Position,
    time_passed: float,
    movement_time: float,
) -> tuple[float, float]:
    """Return a smooth pixel-grid position for one character."""
    key = character_name
    if key not in render_positions:
        render_positions[key] = SmoothPosition.from_position(position)
    return render_positions[key].update(position, time_passed, movement_time)


def get_render_center(position: tuple[float, float]) -> tuple[int, int]:
    """Return the pixel center of a smooth maze position."""
    return (
        int(position[0] * CELL_SIZE + CELL_SIZE // 2),
        int(position[1] * CELL_SIZE + CELL_SIZE // 2),
    )


def get_cell_center(position: Position) -> tuple[int, int]:
    """Return the pixel center of a maze position."""
    return (
        position.x * CELL_SIZE + CELL_SIZE // 2,
        position.y * CELL_SIZE + CELL_SIZE // 2,
    )


def draw_pixel_pacman(
    screen: pygame.Surface,
    data: GameData,
    render_positions: dict[str, SmoothPosition],
    time_passed: float,
) -> None:
    """Draw Pac-Man with sharp pixel-style shapes."""
    player = data.player
    position = get_render_position(
        render_positions,
        "player",
        player.position,
        time_passed,
        data.player_move_time,
    )
    center = get_render_center(position)
    half = CELL_SIZE // 2 - 3
    points = [
        (center[0] - half, center[1] - half),
        (center[0] + half, center[1] - half),
        (center[0] + half, center[1] + half),
        (center[0] - half, center[1] + half),
    ]
    pygame.draw.polygon(screen, PLAYER_COLOR, points)

    mouth_color = CELL_COLOR
    if player.direction == Direction.RIGHT:
        mouth = [center, (center[0] + half, center[1] - 5),
                 (center[0] + half, center[1] + 5)]
    elif player.direction == Direction.LEFT:
        mouth = [center, (center[0] - half, center[1] - 5),
                 (center[0] - half, center[1] + 5)]
    elif player.direction == Direction.UP:
        mouth = [center, (center[0] - 5, center[1] - half),
                 (center[0] + 5, center[1] - half)]
    else:
        mouth = [center, (center[0] - 5, center[1] + half),
                 (center[0] + 5, center[1] + half)]
    pygame.draw.polygon(screen, mouth_color, mouth)


def draw_pixel_ghost(
    screen: pygame.Surface,
    ghost: GhostData,
    color: tuple[int, int, int],
    position: tuple[float, float],
) -> None:
    """Draw one ghost using pixel-style rectangles."""
    left = int(position[0] * CELL_SIZE + 4)
    top = int(position[1] * CELL_SIZE + 4)
    body = pygame.Rect(left, top + 4, CELL_SIZE - 8, CELL_SIZE - 8)
    pygame.draw.rect(screen, color, body)
    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(left + 3, top, CELL_SIZE - 14, 6),
    )

    for foot_left in (left, left + 6, left + 12):
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(foot_left, top + CELL_SIZE - 7, 5, 4),
        )

    pygame.draw.rect(screen, (245, 245, 245), (left + 4, top + 6, 5, 6))
    pygame.draw.rect(screen, (245, 245, 245), (left + 11, top + 6, 5, 6))
    pygame.draw.rect(screen, (20, 40, 160), (left + 6, top + 8, 3, 3))
    pygame.draw.rect(screen, (20, 40, 160), (left + 13, top + 8, 3, 3))


def draw_maze(screen: pygame.Surface, data: GameData) -> None:
    """Draw walls, normal pacgums, and power pacgums."""
    for y, row in enumerate(data.maze):
        for x, cell in enumerate(row):
            left = x * CELL_SIZE
            top = y * CELL_SIZE
            rectangle = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, CELL_COLOR, rectangle)

            if cell & Maze.NORTH:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topleft,
                    rectangle.topright,
                    2,
                )
            if cell & Maze.EAST:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topright,
                    rectangle.bottomright,
                    2,
                )
            if cell & Maze.SOUTH:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.bottomleft,
                    rectangle.bottomright,
                    2,
                )
            if cell & Maze.WEST:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topleft,
                    rectangle.bottomleft,
                    2,
                )

    for position in data.pacgums:
        center_x, center_y = get_cell_center(position)
        pygame.draw.rect(
            screen,
            PACGUM_COLOR,
            pygame.Rect(center_x - 2, center_y - 2, 4, 4),
        )

    for position in data.power_pacgums:
        center_x, center_y = get_cell_center(position)
        pygame.draw.rect(
            screen,
            POWER_COLOR,
            pygame.Rect(center_x - 5, center_y - 5, 10, 10),
        )


def draw_characters(
    screen: pygame.Surface,
    data: GameData,
    render_positions: dict[str, SmoothPosition],
    time_passed: float,
) -> None:
    """Draw Pac-Man and the four ghosts."""
    draw_pixel_pacman(screen, data, render_positions, time_passed)

    colors = {
        "ghost_1": (230, 50, 50),
        "ghost_2": (255, 130, 180),
        "ghost_3": (70, 150, 255),
        "ghost_4": (245, 150, 40),
    }
    for ghost in data.ghosts:
        position = get_render_position(
            render_positions,
            ghost.name,
            ghost.position,
            time_passed,
            data.ghost_move_time,
        )
        color = colors.get(ghost.name, (200, 200, 200))
        if ghost.state == "WEAK":
            color = (70, 90, 220)
            if (
                data.power_mode
                and data.power_mode_time_left <= 2
                and int(data.power_mode_time_left * 8) % 2 == 0
            ):
                color = (245, 245, 245)
        if ghost.state == "EATEN":
            color = (100, 100, 100)
        draw_pixel_ghost(screen, ghost, color, position)


def draw_panel(
    screen: pygame.Surface,
    data: GameData,
    font: pygame.font.Font,
    name_entry_active: bool = False,
    player_name: str = "",
    name_error: str = "",
) -> None:
    """Draw simple debugging information."""
    maze_width = len(data.maze[0]) if data.maze else 0
    panel_x = maze_width * CELL_SIZE + 20
    values = [
        f"State: {data.state}",
        f"Lives: {data.lives}",
        f"Level: {data.level}",
        f"Time: {data.time_left:.1f}",
        f"Score: {data.score}",
        f"Pacgums: {len(data.pacgums)}",
        f"Power: {len(data.power_pacgums)}",
        f"Power mode: {data.power_mode}",
        f"Invincible: {data.invincible}",
        f"Ghosts frozen: {data.ghosts_frozen}",
        f"Fast player: {data.fast_player}",
        "",
        "Highscores:",
    ]
    for number, (name, score) in enumerate(data.highscores, start=1):
        values.append(f"{number}. {name} - {score}")
    values.extend([
        "",
        "Arrow keys: move",
        "Space: pause/resume",
        "R: restart",
        "I: invincible  F: freeze ghosts",
        "L: extra life  N: next level",
        "S: fast player",
        "Enter: start game",
        "Escape: quit",
    ])
    if name_entry_active:
        values.extend([
            "",
            "Enter your name:",
            f"> {player_name}",
            "Enter: save score",
            name_error,
        ])
    for number, value in enumerate(values):
        text = font.render(value, True, TEXT_COLOR)
        screen.blit(text, (panel_x, 20 + number * 25))


def main() -> None:
    """Run the engine debug window."""
    global CELL_SIZE

    pygame.init()
    game = Game("config.json")
    data = game.get_game_data()

    maze_width = len(data.maze[0]) if data.maze else 0
    maze_height = len(data.maze)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    available_width = max(320, screen_width - 40)
    available_height = max(320, screen_height - 80)
    required_rows = max(maze_height, PANEL_HEIGHT // CELL_SIZE)
    max_cell_width = (
        available_width - SIDE_PANEL_WIDTH
    ) // max(maze_width, 1)
    max_cell_height = available_height // max(required_rows, 1)
    CELL_SIZE = max(8, min(max_cell_width, max_cell_height))
    pygame.display.set_caption("Pac-Man Engine Debug")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    render_positions: dict[str, SmoothPosition] = {}
    name_entry_active = False
    player_name = ""
    name_error = ""
    running = True

    while running:
        time_passed = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif name_entry_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            game.save_final_score(player_name)
                            name_entry_active = False
                            name_error = ""
                        except BackendError as error:
                            name_error = str(error)
                    elif event.unicode and (
                        event.unicode.isalnum() or event.unicode == " "
                    ) and len(player_name) < 10:
                        player_name += event.unicode
                elif event.key == pygame.K_RETURN:
                    if game.state == GameState.MENU:
                        game.start_game()
                    elif game.state in (
                        GameState.GAMEOVER,
                        GameState.VICTORY,
                    ):
                        game.start_game()
                elif event.key == pygame.K_SPACE:
                    if game.state is GameState.PLAYING:
                        game.pause_game()
                    elif game.state is GameState.PAUSED:
                        game.resume_game()
                elif event.key == pygame.K_r:
                    game.restart_game()
                    game.start_game()
                elif event.key == pygame.K_i:
                    game.use_cheat("invincible")
                elif event.key == pygame.K_f:
                    game.use_cheat("freeze_ghosts")
                elif event.key == pygame.K_l:
                    game.use_cheat("extra_life")
                elif event.key == pygame.K_n:
                    game.use_cheat("skip_level")
                elif event.key == pygame.K_s:
                    game.use_cheat("fast_player")
                elif event.key == pygame.K_UP:
                    game.move_player(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.move_player(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.move_player(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(Direction.RIGHT)

        game.update(time_passed)
        data = game.get_game_data()
        if (
            data.state in (GameState.GAMEOVER.value, GameState.VICTORY.value)
            and not game.score_submitted
        ):
            name_entry_active = True
        screen.fill(BACKGROUND)
        draw_maze(screen, data)
        draw_characters(screen, data, render_positions, time_passed)
        draw_panel(
            screen,
            data,
            font,
            name_entry_active,
            player_name,
            name_error,
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
