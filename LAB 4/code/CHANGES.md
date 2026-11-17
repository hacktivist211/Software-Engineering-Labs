# Lab 4 — Vibe Coding: Marble Tilt Maze

**PES University — Dept. of CSE · Software Engineering Lab**
**Name:** Chennupati Niraj Kumar · **SRN:** PES2UG24AM046 · **Section:** 5-A
**Assigned repo:** `SETAPESU26/42_marble-tilt-maze` · **Date:** 17 November 2026

## What was done

The starter game was run and played first (see `before.mp4`), then four tasks from
the repository README were completed with an LLM as a pair-programming partner.

| Task | Change | Where |
| :--- | :--- | :--- |
| 1 | Collision is now a true circle-vs-rectangle test instead of a bounding-box (`colliderect`) test, with sub-stepping so the marble cannot tunnel through a wall | `game/game_engine.py` (`_hit`, `_resolve_wall_collisions`), `tests/test_collision.py` |
| 2 | The round ends on screen: **MAZE SOLVED** with the finish time or **TIME'S UP**, over a dimmed maze, and waits for input instead of printing to the console | `game/game_engine.py` (`_render_end`, `_panel`, HUD) |
| 3 | Difficulty menu (Easy / Medium / Hard → tilt strength, friction, time limit) and replay from the end screen (`R` replay, `1`/`2`/`3` new difficulty, `M` menu, `Esc` quit) | `game/game_engine.py` (`DIFFICULTIES`, `start_round`, `_render_menu`) |
| 4 | Sound feedback for wall bounces, reaching the goal and running out of time, synthesised at start-up so no audio files are needed | `game/sounds.py`, `_play_bounce` |

### The bug in Task 1

The original test compared the marble's square bounding box with each wall:

```python
if marble_rect.colliderect(wall_rect):      # square vs rectangle
```

Near a wall corner the bounding square overlaps the wall while the round marble is
still ~5 px away, so the marble bounced off empty space. The demonstration video
shows a bounce while the marble is **+3.4 px** from the wall. The replacement finds
the closest point on the rectangle to the marble centre and resolves along that
normal, which is exact for a circle:

```python
closest_x = min(max(m.x, r.left), r.right)
closest_y = min(max(m.y, r.top), r.bottom)
distance  = hypot(m.x - closest_x, m.y - closest_y)
if distance > m.radius:      # the round marble really does not touch
    return None
```

## Controls

| Key / input | Action |
| :--- | :--- |
| Mouse | Tilt the maze — the marble accelerates away from the screen centre |
| `1` / `2` / `3` | Start Easy / Medium / Hard (menu, and after a round) |
| `R` | Replay the same difficulty (end screen) |
| `M` | Back to the difficulty menu (end screen) |
| `Esc` | Quit |

## Running it

```bash
pip install -r requirements.txt
python main.py
python tests/test_collision.py     # collision regression tests
```

## Videos

| File | Shows |
| :--- | :--- |
| `before.mp4` | Original build: the marble bounces **3.4 px before** touching the wall corner (the red square is the old square hit-box, the blue circle is the real marble radius, the HUD reports the clearance at impact) |
| `after.mp4` | Fixed build: correct wall contact (green "wall contact - correct bounce"), difficulty menu, full round, **MAZE SOLVED** with finish time, sound-effect indicator, and replay at a new difficulty |

The captures are rendered by the game itself with a scripted autopilot (the same
physics and drawing code), at 60 fps, and are exactly 10 seconds long.

## Note on sound

The effects are synthesised with the `array`/`math` modules at start-up, so the
game needs no audio assets and stays silent (without crashing) on machines with no
sound device — which is also why the capture runs show an `SFX:` indicator instead
of audible sound.
