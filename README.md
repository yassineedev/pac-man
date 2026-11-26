*This project is part of the 42 school curriculum.*

# Pac-Man

A Pac-Man game made with Python and Pygame.

## Status

This is only the project skeleton. Game logic is not ready.

## Team

- Developer 1: game engine, maze, player, ghosts, levels, config.
- Developer 2: game screens, drawing, keys, highscores.
- Both: tests, code review, and documentation.

## Run

1. Run `make install`.
2. Run `make run` after the game logic is added.

## Folders

- `src/core`: game rules.
- `src/models`: game objects.
- `src/services`: files and maze tool.
- `src/views`: Pygame screens.
- `src/shared`: data used by both developers.

## To finish

Add the full subject requirements, game rules, tests, and packaging steps.

## Configuration

The game reads `config.json`. Lines starting with `#` are comments and are
ignored. Full-line `//` comments are also accepted.

Global settings are stored once:

- `highscore_filename`: JSON file used to store high scores.
- `lives`: starting number of lives.
- `pacgum`: number of normal pacgums requested for a level.
- `points_per_pacgum`: points for a normal pacgum.
- `points_per_super_pacgum`: points for a power pacgum.
- `points_per_ghost`: points for eating a weak ghost.

The `levels` array stores settings for each level. Each level has its own:

- `width`: maze width.
- `height`: maze height.
- `seed`: maze generation seed.
- `level_max_time`: time limit in seconds for that level.

Example:

```json
{
  "highscore_filename": "data/highscores.json",
  "lives": 3,
  "pacgum": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "levels": [
    {"width": 25, "height": 25, "seed": 42, "level_max_time": 90},
    {"width": 25, "height": 25, "seed": 43, "level_max_time": 90}
  ]
}
```

## Highscores

Highscores are stored in the JSON file from `highscore_filename`.
The default file is `data/highscores.json`.

The game loads the file when it starts and keeps the ten highest scores.
When a game ends, the player can enter a name and save the final score.
Names can have up to 10 letters, numbers, or spaces. Scores must be
non-negative integers. Missing or broken highscore files are treated as an
empty list. Saving errors are reported to the game.
