# 👾 Pac-Man Game Engine — Task Tracker

**Progress:** 10/105 tasks completed (9.5%).  
**Next task:** 11 — Find a valid Pac-Man spawn position.

## Phase 1 — Maze System (10/13)

- [x] **01.** Import the provided 42 `MazeGenerator`.
- [x] **02.** Create the `MazeGeneratorPanel` wrapper.
- [x] **03.** Implement `make_maze(seed)`.
- [x] **04.** Create the `Maze` class.
- [x] **05.** Implement `generate(seed)`.
- [x] **06.** Store and access the maze grid.
- [x] **07.** Implement `is_inside()`.
- [x] **08.** Implement `has_wall()`.
- [x] **09.** Implement `can_move()`.
- [x] **10.** Implement and test `get_neighbors()`.
- [ ] **11.** Find a valid spawn position for Pac-Man.
- [ ] **12.** Find four valid spawn positions for ghosts.
- [ ] **13.** Test maze generation with fixed and random seeds.

## Phase 2 — Player System (0/9)

- [ ] **14.** Create the `Player` class in `src/models/player.py`.
- [ ] **15.** Add player position (`x`, `y`).
- [ ] **16.** Store the player's starting position.
- [ ] **17.** Add player direction.
- [ ] **18.** Implement `set_direction()`.
- [ ] **19.** Implement movement by one cell.
- [ ] **20.** Prevent movement through walls and outside the maze.
- [ ] **21.** Implement `reset_position()`.
- [ ] **22.** Test player movement and reset.

## Phase 3 — Pellets & Scoring (0/9)

- [ ] **23.** Create a system to store pellet positions.
- [ ] **24.** Place regular pellets in reachable maze cells.
- [ ] **25.** Place power pellets.
- [ ] **26.** Avoid placing pellets on protected cells and spawn positions.
- [ ] **27.** Detect when Pac-Man eats a pellet.
- [ ] **28.** Remove eaten pellets.
- [ ] **29.** Award points for regular pellets.
- [ ] **30.** Detect when all pellets are collected.
- [ ] **31.** Test pellet collection and scoring.

## Phase 4 — Ghost System (0/11)

- [ ] **32.** Create the `Ghost` class in `src/models/ghost.py`.
- [ ] **33.** Add ghost position and starting position.
- [ ] **34.** Add ghost direction and state.
- [ ] **35.** Get valid movement directions using `Maze`.
- [ ] **36.** Implement ghost movement.
- [ ] **37.** Implement ghost respawn.
- [ ] **38.** Implement `RandomGhost`.
- [ ] **39.** Implement BFS pathfinding.
- [ ] **40.** Implement `FollowGhost` using BFS.
- [ ] **41.** Create four ghosts with different behaviors.
- [ ] **42.** Test ghost movement and pathfinding.

## Phase 5 — Collisions & Lives (0/9)

- [ ] **43.** Add player lives.
- [ ] **44.** Detect player–ghost collisions.
- [ ] **45.** Detect collisions when player and ghost cross positions.
- [ ] **46.** Remove one life after a dangerous collision.
- [ ] **47.** Reset positions after losing a life.
- [ ] **48.** Add temporary protection after respawning.
- [ ] **49.** Prevent repeated life loss during protection.
- [ ] **50.** Detect game over when lives reach zero.
- [ ] **51.** Test collisions, lives, and game over.

## Phase 6 — Power Mode (0/10)

- [ ] **52.** Detect when Pac-Man eats a power pellet.
- [ ] **53.** Activate power mode.
- [ ] **54.** Add a power-mode timer.
- [ ] **55.** Change ghost behavior during power mode.
- [ ] **56.** Implement ghost fleeing behavior.
- [ ] **57.** Allow Pac-Man to eat frightened ghosts.
- [ ] **58.** Award points for eating ghosts.
- [ ] **59.** Respawn eaten ghosts.
- [ ] **60.** Restore normal ghost behavior when power mode expires.
- [ ] **61.** Test power mode.

## Phase 7 — Level Management (0/13)

- [ ] **62.** Create `LevelManager` in `src/core/level_manager.py`.
- [ ] **63.** Store the current level number.
- [ ] **64.** Use a fixed positive seed for Level 1.
- [ ] **65.** Use random seeds for later levels.
- [ ] **66.** Generate a new maze for each level.
- [ ] **67.** Set player and ghost spawn positions.
- [ ] **68.** Generate pellets for each level.
- [ ] **69.** Add a level timer.
- [ ] **70.** Update the level timer.
- [ ] **71.** Detect level completion.
- [ ] **72.** Increase difficulty between levels.
- [ ] **73.** Implement victory after completing 10 levels.
- [ ] **74.** Test level transitions.

## Phase 8 — Game Controller (0/11)

- [ ] **75.** Create `Game` in `src/core/game.py`.
- [ ] **76.** Define game states (menu, playing, paused, game over, victory).
- [ ] **77.** Implement `start()`.
- [ ] **78.** Implement `update(delta_time)`.
- [ ] **79.** Implement `move_player(direction)`.
- [ ] **80.** Implement `pause()`.
- [ ] **81.** Implement `resume()`.
- [ ] **82.** Implement `restart()`.
- [ ] **83.** Prevent updates in inappropriate game states.
- [ ] **84.** Implement the required cheat functionality.
- [ ] **85.** Test the game controller.

## Phase 9 — UI Integration (0/9)

- [ ] **86.** Create `GameData` in `src/shared/game_data.py`.
- [ ] **87.** Define an immutable game-state snapshot.
- [ ] **88.** Expose maze grid and wall data.
- [ ] **89.** Expose Pac-Man's position and direction.
- [ ] **90.** Expose ghost positions and states.
- [ ] **91.** Expose pellet and power-pellet positions.
- [ ] **92.** Expose score, lives, level, and timers.
- [ ] **93.** Expose current game state.
- [ ] **94.** Test the engine-to-UI data contract.

> **Team note:** Agree on the `GameData` interface with your Pygame teammate early, even if you implement it later.

## Phase 10 — Final Testing & Validation (0/11)

- [ ] **95.** Test a complete game without Pygame.
- [ ] **96.** Test maze generation across multiple seeds.
- [ ] **97.** Test player movement at maze boundaries.
- [ ] **98.** Test ghost movement and pathfinding.
- [ ] **99.** Test all collision scenarios.
- [ ] **100.** Test scoring and pellet collection.
- [ ] **101.** Test power-mode activation and expiration.
- [ ] **102.** Test level transitions and timers.
- [ ] **103.** Test game over and victory.
- [ ] **104.** Check type hints, mypy, flake8, and error handling.
- [ ] **105.** Run the complete game with your teammate's UI.

## Progress Summary

| Phase | Completed | Total |
|---|---:|---:|
| Maze System | 10 | 13 |
| Player System | 0 | 9 |
| Pellets & Scoring | 0 | 9 |
| Ghost System | 0 | 11 |
| Collisions & Lives | 0 | 9 |
| Power Mode | 0 | 10 |
| Level Management | 0 | 13 |
| Game Controller | 0 | 11 |
| UI Integration | 0 | 9 |
| Final Testing | 0 | 11 |
| **Total** | **10** | **105** |

Update each checkbox from `- [ ]` to `- [x]` as you finish a task.
