# Pac-Man Project - Mentor Context

This file is a handoff summary for continuing the mentoring conversation in a
new chat. It is not the official project README.

## Student preferences

- Act as a mentor first, not as a code generator.
- Explain the logic before suggesting code.
- Do not write complete functions unless explicitly requested.
- Review the student's code and explain mistakes.
- Use beginner-friendly Python and simple A2/B1 English.
- Avoid over-engineered or AI-looking code.
- Do not use nested functions.
- Use simple names and short docstrings.
- Keep polymorphism clear for the project defense.
- Do not change the student's logic without asking.
- Use try/except only when a real operation can fail.

## Project requirements

The project is a Python Pac-Man game using an external A-Maze-ing generator.
It must include:

- Object-oriented architecture and polymorphism.
- JSON configuration with comments and safe defaults.
- Four ghosts with different behaviours.
- Normal pacgums and four power pacgums.
- Score, lives, collisions, levels, timers, pause, and victory.
- Cheat mode for peer review.
- Persistent highscores.
- UI integration through an immutable `GameData` snapshot.
- Type hints, docstrings, flake8, mypy, and tests.

## Architecture decisions

```text
pac-man.py -> ConfigService -> GameConfig -> Game
                                      Game -> LevelManager
                                      Game -> ScoreManager
                                      Game -> CollisionManager
                                      Game -> PowerMode
                                      Game -> GameData
```

`ConfigService` reads and validates JSON. `Game` receives the parsed
`GameConfig`; it does not parse JSON itself.

`Game` coordinates gameplay, game state, lives, levels, pause, game over,
victory, and later cheats.

`LevelManager` creates a maze, player, ghosts, pacgums, and the level timer.

`Player` manages position, direction, input direction, movement, and reset.
It does not manage score or lives.

`Ghost` is the base class. The ghost subclasses use polymorphism by providing
different `choose_move(player_position)` implementations.

`PacgumManager` stores and removes pacgums. It does not manage score or power
mode.

`ScoreManager` manages only score. Lives belong to `Game` because losing a life
affects resetting characters and checking game over.

`GameData` is the state snapshot sent to the UI. The UI reads it and does not
modify backend objects.

## Current progress

### Maze and spawns

The maze phase is almost complete:

- Maze generation works through the external generator.
- `is_inside`, `has_wall`, `can_move`, and `get_neighbors` exist.
- `get_neighbors` returns `Position` objects.
- Player and ghost spawns use `Position` objects.
- Player spawn checks the middle and searches for a corridor if needed.
- Ghost spawns use corners and find another corridor if a corner is invalid.
- Player and ghost positions do not overlap.
- Maze and spawn tests pass.

Remaining maze work is testing several fixed and random seeds.

### Player

`Player` currently has position, starting position, direction, input direction,
`choose_move`, `set_direction`, `reset_position`, and compatibility method
`return_to_start`.

Score and lives were removed from `Player` to avoid duplicated responsibility.
The old player test still expects the old constructor and must be rewritten.

### Ghosts

Ghost classes exist with normal, weak, and eaten states. Four behaviours exist:

- `FirstGhost` follows Pac-Man.
- `SecondGhost` targets a position ahead.
- `ThirdGhost` targets a farther position.
- `FourthGhost` chooses random valid directions.

Respawn timing, collision integration, power-mode integration, and full tests
are still missing.

### Pacgums

`PacgumManager` now uses `Position` internally. It stores normal and power
pacgums, creates normal pacgums, creates power pacgums, removes eaten pacgums,
and checks completion.

Subject decision:

```text
There are exactly four power pacgums.
One is placed at each corner coordinate.
```

The four power pacgums are placed at the corners even if a corner is closed.
Normal pacgums are placed on valid corridor cells and avoid protected cells,
the player, and power pacgum positions. The current code uses every valid
corridor cell rather than limiting the number to 42.

Pacgum tests currently pass. Remaining work includes adding ghost spawn cells
to the protected positions when levels are integrated, deciding whether all
valid cells or exactly 42 normal pacgums are wanted, and connecting eating to
the score system.

### Score

`ScoreManager` follows only this rule:

```text
Normal pacgum -> +X
Power pacgum  -> +Y
Edible ghost  -> +Z
Score never decreases.
```

It has methods for normal pacgum score, power pacgum score, edible ghost score,
and resetting the score. It does not manage lives. Score tests currently pass.

## Incomplete systems

- `src/core/game.py` is still empty.
- The level manager is still incomplete.
- Configuration loading and validation are incomplete.
- Collision handling is not implemented.
- Power mode is not implemented.
- Highscores are not implemented.
- Cheat mode is not implemented.
- Full `GameData` integration is not implemented.

## Next order of work

1. Finish maze tests with multiple fixed and random seeds.
2. Rewrite the old player tests.
3. Finish `ConfigService` and `GameConfig` values.
4. Build the `Game` class without cheats.
5. Build the level manager.
6. Connect player movement, pacgums, and score.
7. Implement collisions and lives in the game flow.
8. Implement power mode.
9. Implement level timers, game over, and victory.
10. Complete `GameData` for the UI.
11. Add cheat mode.
12. Add complete backend tests.

## Cheat mode plan

Cheats belong in `Game`, not in Player, Ghost, ScoreManager, or PacgumManager.
Suggested peer-review controls are invincibility, ghost freeze, extra life,
level skip, and increased speed. Cheats should be added only after normal game
play works.

## Useful tests

```bash
./.venv/bin/python -m pytest -q tests/test_maze.py tests/test_spawn_manager.py
./.venv/bin/python -m pytest -q tests/test_pacgum.py
./.venv/bin/python -m pytest -q tests/test_score.py
./.venv/bin/python -m flake8 src tests
```

The complete repository test run is not expected to pass yet because several
classes and old tests are still incomplete.
