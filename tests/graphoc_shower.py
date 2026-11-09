"""Temporary Pygame viewer for the Pac-Man engine.

Run: python3 tests/graphoc_shower.py
Keys: arrows/WASD move, R regenerate, ESC quit.
"""

import argparse
import random
import sys
from pathlib import Path

# Allow launching this tester by its absolute path from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pygame

from src.models.maze import Maze
from src.services.spawnmanager import SpawnManager

CELL = 22
TOP = 72
BOTTOM = 36
MAX_WIDTH = 1200
MAX_HEIGHT = 900
WALL_COLOR = (51, 151, 255)
BACKGROUND = (12, 16, 30)
FLOOR_COLOR = (23, 29, 46)

# The maze generator uses wall bitmasks: N=1, E=2, S=4, W=8.
WALLS = ((1, (0, 0, 1, 0)), (2, (1, 0, 1, 1)), (4, (0, 1, 1, 1)), (8, (0, 0, 0, 1)))
MOVES = {
    pygame.K_UP: ("UP", 0, -1),
    pygame.K_w: ("UP", 0, -1),
    pygame.K_RIGHT: ("RIGHT", 1, 0),
    pygame.K_d: ("RIGHT", 1, 0),
    pygame.K_DOWN: ("DOWN", 0, 1),
    pygame.K_s: ("DOWN", 0, 1),
    pygame.K_LEFT: ("LEFT", -1, 0),
    pygame.K_a: ("LEFT", -1, 0),
}


def get_ghost_spawns(manager, maze):
    """Use the engine's spawn method, accommodating either owner."""
    for target in (manager, maze):
        for name in ("find_ghost_spawn", "find_ghost_spawns"):
            method = getattr(target, name, None)
            if callable(method):
                return method()
    raise AttributeError("Could not find find_ghost_spawn() on SpawnManager or Maze")


def create_world(width, height, seed):
    maze = Maze(width, height)
    maze.generate(seed=seed)
    manager = SpawnManager(maze)
    player = manager.find_player_spawn()
    ghosts = get_ghost_spawns(manager, maze)
    return maze, player, ghosts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, help="Save the initial frame and exit")
    args = parser.parse_args()
    width, height = 10, 10
    seed = 42
    pygame.init()
    cell = min(
        CELL, (MAX_WIDTH - 32) // width, (MAX_HEIGHT - TOP - BOTTOM - 32) // height
    )
    if cell < 6:
        raise ValueError("Maze too large for this viewer")
    screen = pygame.display.set_mode(
        (width * cell + 32, height * cell + TOP + BOTTOM + 16)
    )
    pygame.display.set_caption("Pac-Man | Engine Debug Viewer")
    font = pygame.font.SysFont(None, 26)
    small = pygame.font.SysFont(None, 21)
    clock = pygame.time.Clock()

    maze, player, ghosts = create_world(width, height, seed)
    pellets = {
        (x, y)
        for y in range(height)
        for x in range(width)
        if maze.grid[y][x] != 15 and (x, y) != player and (x, y) not in ghosts.values()
    }
    score = 0
    lives = 3
    steps = 0
    origin_x, origin_y = 16, TOP
    ghost_colors = [(245, 88, 88), (255, 171, 204), (100, 227, 255), (255, 188, 97)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    seed = random.randint(1, 2**31 - 1)
                    maze, player, ghosts = create_world(width, height, seed)
                    pellets = {
                        (x, y)
                        for y in range(height)
                        for x in range(width)
                        if maze.grid[y][x] != 15
                        and (x, y) != player
                        and (x, y) not in ghosts.values()
                    }
                    score = steps = 0
                elif event.key in MOVES:
                    direction, dx, dy = MOVES[event.key]
                    if maze.can_move(player[0], player[1], direction):
                        player = (player[0] + dx, player[1] + dy)
                        steps += 1

                        if player in pellets:
                            pellets.remove(player)
                            score += 10

        screen.fill(BACKGROUND)
        screen.blit(font.render("Pac-Man | Initial engine state", True, (240, 240, 255)), (16, 12))
        screen.blit(small.render(f"Seed request: {seed}   Score: {score}   Steps: {steps}", True, (180, 190, 210)), (16, 42))
        for y, row in enumerate(maze.grid):
            for x, walls in enumerate(row):
                px, py = origin_x + x * cell, origin_y + y * cell
                pygame.draw.rect(screen, FLOOR_COLOR, (px, py, cell, cell))
                if walls == 15:
                    pygame.draw.rect(screen, WALL_COLOR, (px + 2, py + 2, cell - 3, cell - 3))
                else:
                    for mask, (x1, y1, x2, y2) in WALLS:
                        if walls & mask:
                            pygame.draw.line(screen, WALL_COLOR,
                                             (px + x1 * cell, py + y1 * cell),
                                             (px + x2 * cell, py + y2 * cell), 2)
        for x, y in pellets:
            pygame.draw.circle(screen, (235, 215, 170),
                               (origin_x + x * cell + cell // 2, origin_y + y * cell + cell // 2), 2)
        for index, (name, (x, y)) in enumerate(ghosts.items()):
            pygame.draw.circle(screen, ghost_colors[index % len(ghost_colors)],
                               (origin_x + x * cell + cell // 2, origin_y + y * cell + cell // 2), cell // 3)
        x, y = player
        pygame.draw.circle(screen, (255, 225, 40),
                           (origin_x + x * cell + cell // 2, origin_y + y * cell + cell // 2), cell // 3)
        screen.blit(small.render("Arrows/WASD: move   R: regenerate   Esc: quit", True, (180, 190, 210)),
                    (16, origin_y + height * cell + 12))
        pygame.display.flip()
        if args.snapshot:
            pygame.image.save(screen, str(args.snapshot))
            print(f"Initial frame saved: {args.snapshot}; player={player}; ghosts={ghosts}")
            running = False
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
