"""Small Pygame window for testing the game engine."""

import pygame

from src.core.game import Game, GameState
from src.shared.game_data import Direction, GhostStatu


CELL_SIZE = 24
SIDE_PANEL_WIDTH = 220
BACKGROUND = (8, 8, 24)
WALL_COLOR = (35, 90, 220)
PACGUM_COLOR = (245, 245, 245)
POWER_COLOR = (255, 170, 40)
PLAYER_COLOR = (255, 220, 0)
TEXT_COLOR = (235, 235, 235)


def draw_maze(screen: pygame.Surface, game: Game) -> None:
    """Draw walls, normal pacgums, and power pacgums."""
    for y, row in enumerate(game.maze.grid):
        for x, cell in enumerate(row):
            left = x * CELL_SIZE
            top = y * CELL_SIZE
            rectangle = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)

            if cell & game.maze.NORTH:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topleft,
                    rectangle.topright,
                    2,
                )
            if cell & game.maze.EAST:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topright,
                    rectangle.bottomright,
                    2,
                )
            if cell & game.maze.SOUTH:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.bottomleft,
                    rectangle.bottomright,
                    2,
                )
            if cell & game.maze.WEST:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    rectangle.topleft,
                    rectangle.bottomleft,
                    2,
                )

    for position in game.pac_gums.pacgums:
        center = (
            position.x * CELL_SIZE + CELL_SIZE // 2,
            position.y * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(screen, PACGUM_COLOR, center, 3)

    for position in game.pac_gums.power_pacgum:
        center = (
            position.x * CELL_SIZE + CELL_SIZE // 2,
            position.y * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(screen, POWER_COLOR, center, 7)


def draw_characters(screen: pygame.Surface, game: Game) -> None:
    """Draw Pac-Man and the four ghosts."""
    player_center = (
        game.player.position.x * CELL_SIZE + CELL_SIZE // 2,
        game.player.position.y * CELL_SIZE + CELL_SIZE // 2,
    )
    pygame.draw.circle(screen, PLAYER_COLOR, player_center, CELL_SIZE // 2 - 3)

    colors = {
        "red": (230, 50, 50),
        "pink": (255, 130, 180),
        "blue": (70, 150, 255),
        "orange": (245, 150, 40),
    }
    for ghost in game.ghosts:
        center = (
            ghost.position.x * CELL_SIZE + CELL_SIZE // 2,
            ghost.position.y * CELL_SIZE + CELL_SIZE // 2,
        )
        color = colors.get(ghost.color, (200, 200, 200))
        if ghost.state == GhostStatu.WEAK:
            color = (70, 90, 220)
        if ghost.state == GhostStatu.EATEN:
            color = (100, 100, 100)
        pygame.draw.circle(screen, color, center, CELL_SIZE // 2 - 3)


def draw_panel(
    screen: pygame.Surface,
    game: Game,
    font: pygame.font.Font,
) -> None:
    """Draw simple debugging information."""
    panel_x = game.maze.width * CELL_SIZE + 20
    values = [
        f"State: {game.state.value}",
        f"Lives: {game.lives}",
        f"Level: {game.level}",
        f"Time: {game.time_left:.1f}",
        f"Score: {game.score_manager.total_score}",
        f"Pacgums: {len(game.pac_gums.pacgums)}",
        f"Power: {len(game.pac_gums.power_pacgum)}",
        f"Power mode: {game.power_mode}",
        "",
        "Arrow keys: move",
        "Space: pause/resume",
        "R: restart",
        "Escape: quit",
    ]
    for number, value in enumerate(values):
        text = font.render(value, True, TEXT_COLOR)
        screen.blit(text, (panel_x, 20 + number * 25))


def main() -> None:
    """Run the engine debug window."""
    pygame.init()
    game = Game("config.json")
    game.start_game()

    width = game.maze.width * CELL_SIZE + SIDE_PANEL_WIDTH
    height = game.maze.height * CELL_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pac-Man Engine Debug")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    running = True

    while running:
        time_passed = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if game.state is GameState.PLAYING:
                        game.pause_game()
                    elif game.state is GameState.PAUSED:
                        game.resume_game()
                elif event.key == pygame.K_r:
                    game.restart_game()
                    game.start_game()
                elif event.key == pygame.K_UP:
                    game.move_player(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.move_player(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.move_player(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(Direction.RIGHT)

        game.update(time_passed)
        screen.fill(BACKGROUND)
        draw_maze(screen, game)
        draw_characters(screen, game)
        draw_panel(screen, game, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
