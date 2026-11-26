# Pac-Man Project - Mentor Context

This file is a handoff summary for continuing the mentoring conversation. It
is not the official project README.

## Student preferences

- Act as a mentor first, not as a code generator.
- Explain the logic before suggesting code.
- Do not write code unless the student explicitly asks for it.
- When code is requested, change only the requested part.
- Review the student's code and explain mistakes.
- Use beginner-friendly Python and simple A2/B1 English.
- Avoid over-engineered or AI-looking code.
- Do not use nested functions.
- Use simple names and short docstrings.
- Keep polymorphism clear for the project defense.
- Do not change the student's logic without asking.
- Do not call style suggestions runtime errors without checking the other classes.
- Use try/except only when a real operation can fail.

## Project requirements

The project is a Python Pac-Man game using an external A-Maze-ing generator.
It must include:

- Object-oriented architecture and polymorphism.
- JSON configuration with comments and safe defaults.
- A level array with width, height, seed, and level time per level.
- Four ghosts with different behaviours.
- Normal pacgums and four power pacgums.
- Score, lives, collisions, levels, timers, pause, and victory.
- Cheat mode for peer review.
- Persistent highscores.
- UI integration through an immutable `GameData` snapshot.
- Type hints, docstrings, flake8, mypy, and tests.

## Target architecture

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

`Game` should coordinate global state, lives, score, power mode, collisions,
level transitions, pause, game over, victory, and cheats.

`LevelManager` should create and update the current maze, player, ghosts,
pacgums, and level timer. The UI should call `Game.update()`, not
`LevelManager.update()` directly.

`Player` manages position, direction, input direction, movement, and reset.
It does not manage score or lives.

`Ghost` is the base class. The ghost subclasses use polymorphism through
different `choose_move(player_position)` implementations.

`PacgumManager` stores and removes pacgums. It does not manage score or power
mode.

`ScoreManager` manages only score. Lives belong to `Game` because losing a
life affects resetting characters and checking game over.

`GameData` is the immutable state snapshot sent to the UI. The UI reads it and
does not modify backend objects.

## Current progress

### Tests and quality checks

- The complete test suite currently passes: **18 tests passed**.
- `flake8 src tests debug_ui.py` currently passes.
- `mypy src` currently reports **22 errors**. Most are in the new
  `LevelManager` optional attribute types, protected-position types, and the
  `PlayerData` helper.

### Maze and spawns

- Maze generation works through the external generator.
- `is_inside`, `has_wall`, `can_move`, and `get_neighbors` exist.
- `get_neighbors` returns `Position` objects.
- Player and ghost spawns use `Position` objects.
- Player spawn searches for a valid corridor near the middle.
- Ghost spawns use corners and find another corridor if needed.
- The `Game` constructor protects ghost spawn positions when creating its
  pacgums.
- Maze and spawn tests pass.

### Configuration

`src/services/config.py` now returns frozen dataclasses:

```text
GameConfig
  highscore_filename
  levels: tuple[LevelConfig, ...]
  lives
  pacgum
  points_per_pacgum
  points_per_super_pacgum
  points_per_ghost

LevelConfig
  width
  height
  seed
  level_max_time
```

The parser supports full-line `#` comments and full-line `//` comments. It
uses defaults for missing files, invalid JSON, invalid values, and missing
level data. `config.json` contains a list of level objects, and
`level_max_time` is stored inside each level object.

### Player

`Player` currently has:

- position
- start position
- direction
- input direction
- `choose_move()`
- `set_direction()`
- `reset_position()`
- `return_to_start()`

The intended input flow is:

```text
UI key -> Game.move_player(direction)
       -> Player.set_direction(direction)
Game.update(delta_time)
       -> Player.choose_move()
       -> Player.move(direction, maze)
```

Player movement uses a timer so it does not move once per rendered frame.

Known issue: `Player.player_data()` currently uses the wrong keyword
`Direction` instead of `direction`. This causes a mypy error and should be
fixed before relying on that helper.

### Ghosts

Ghost classes exist with normal, weak, and eaten states:

- `FirstGhost` follows Pac-Man with BFS.
- `SecondGhost` targets a position ahead.
- `ThirdGhost` targets a farther position.
- `FourthGhost` chooses random valid directions.

Ghost movement uses a timer in the engine. Power mode changes normal ghosts
to weak ghosts. A weak ghost becomes eaten and receives a respawn delay.

Current limitation: `Ghost.update_respawn()` is not complete. It currently
does not decrease the timer or perform the `EATEN -> NORMAL` transition
correctly. This must be designed and tested before final collision work.

### Pacgums and score

`PacgumManager` stores normal and power pacgums, creates them, removes eaten
ones, and checks completion. There are exactly four power pacgums, one at each
corner coordinate.

The current pacgum creation still uses every valid corridor cell. The parsed
`pacgum: 42` value is not yet used to limit normal pacgums to exactly 42.

`ScoreManager` supports normal pacgum, power pacgum, ghost score, and reset.
Score tests pass.

### Game controller

`src/core/game.py` currently has:

- `GameState` enum: menu, playing, paused, game over, victory.
- configuration loading.
- direct creation of the first maze, player, ghosts, and pacgums.
- player movement input.
- player and ghost movement timers.
- level timer.
- power-mode timer.
- pacgum scoring.
- basic ghost collisions and temporary protection.
- `GameData` construction for the UI.
- a `LevelManager` attribute, but the game still creates the first level
  directly. The manager is not fully integrated yet.

The current `Game.update()` has basic working logic, but level transitions,
complete ghost respawn, crossing collisions, and full collision design are
still unfinished.

### LevelManager

`src/core/level.py` now contains a partially implemented `LevelManager`.

Implemented or started:

- stores `GameConfig`.
- stores a current level index using `current_level`.
- creates the maze from the current `LevelConfig`.
- uses the level seed.
- creates the player and four ghost classes.
- creates normal and power pacgums.
- stores the level timer.
- updates the player and ghost movement timers.
- updates player and ghost movement.
- calls eaten-ghost respawn updates.
- collects pacgums and awards score through its current `ScoreManager`.
- resets player and ghosts.

Still incomplete:

- `is_level_done()`.
- `next_level()`.
- final decision about whether score belongs only in `Game`.
- full type annotations for attributes created after `__init__`.
- integration with `Game`.
- ghost spawn cells should be reviewed for pacgum protection.

The current LevelManager is useful for learning and testing, but the game
still duplicates level creation in `Game`. Do not refactor both classes at
once; first make the manager work, then migrate creation responsibility from
`Game`.

### UI debug tool

`debug_ui.py` is a small Pygame engine-debug window. It displays the maze,
pixel-style cells, Pac-Man, ghosts, normal pacgums, power pacgums, score,
lives, timer, and state. It uses engine objects directly because the UI
snapshot work is still being completed.

Controls:

```text
Arrow keys -> send player direction
Space      -> pause/resume
R          -> restart
Escape     -> quit
```

The UI is for finding engine bugs. It should not contain game rules.

## Known incomplete systems

- Level transitions and final `LevelManager` integration.
- Complete eaten-ghost respawn timing.
- Collision manager or clean collision helper design.
- Crossing collisions.
- Full power-mode behavior and tests.
- Exact normal-pacgum count from configuration.
- Complete restart behavior.
- Highscores.
- Cheat mode.
- Final UI contract tests.
- Mypy cleanup.

## Recommended next order

1. Finish and test `LevelManager.is_level_done()`.
2. Finish and test `LevelManager.next_level()`.
3. Decide the exact ownership of `ScoreManager`.
4. Move level creation from `Game` into `LevelManager` gradually.
5. Make `Game.update()` call the level manager without duplicating movement.
6. Finish eaten-ghost respawn state transitions.
7. Define and test all collision cases.
8. Finish level timer, life loss, game over, and victory transitions.
9. Complete `GameData` and test the engine-to-UI contract.
10. Add cheat mode only after normal gameplay works.
11. Fix mypy errors and run the complete validation suite.

## Cheat mode plan

Cheats belong in `Game`, not in Player, Ghost, ScoreManager, or
PacgumManager. Suggested peer-review controls are invincibility, ghost freeze,
extra life, level skip, and increased speed. Add them only after normal play
and level transitions work.

## Useful commands

```bash
./.venv/bin/python -m pytest -q
./.venv/bin/python -m flake8 src tests debug_ui.py
./.venv/bin/python -m mypy src
./.venv/bin/python debug_ui.py
```
