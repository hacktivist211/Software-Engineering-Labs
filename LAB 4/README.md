# Lab 4 — Vibe Coding: Marble Tilt Maze

**Problem Statement:** fix and extend the starter game in the assigned repository
`github.com/SETAPESU26/42_marble-tilt-maze`
**PES University · Dept. of CSE · Software Engineering Lab**
**Name:** Chennupati Niraj Kumar · **SRN:** PES2UG24AM046 · **Section:** 5-A · **Date:** 17 November 2026

The assigned repository was cloned, the game was run, and four README tasks were completed with an LLM as a
pair-programming partner. The solved code is pushed to **`github.com/hacktivist211/42_marble-tilt-maze`**
(no pull request was raised against `SETAPESU26`).

## Submission deliverables

| # | Deliverable | File |
| :-: | :--- | :--- |
| a | 10-second gameplay video **before** the changes (bug visible) | [`before.mp4`](before.mp4) |
| a | 10-second gameplay video **after** the changes (bug fixed + new features) | [`after.mp4`](after.mp4) |
| b | Updated code | [`code/`](code) — same tree as the pushed repository |
| c | Chat / LLM history | [`Chat_History.pdf`](Chat_History.pdf) · [`.docx`](Chat_History.docx) |

The two lab handouts (task sheet and repo-link sheet) are kept in [`reference/`](reference).

## Tasks completed

| Task | Change | Commit |
| :--- | :--- | :--- |
| 1 | Collision is a true circle-vs-rectangle test (closest point on the wall) with sub-stepping, instead of a bounding-box `colliderect()` test — the marble no longer bounces ~5 px before touching a corner | `Task 1: true circle-vs-rectangle collision with sub-stepping` |
| 2 | On-screen end of round: **MAZE SOLVED** with the finish time or **TIME'S UP**, over a dimmed maze, waiting for input instead of printing to the console | `Task 2: on-screen end of round with the finish time` |
| 3 | Difficulty menu (Easy / Medium / Hard → tilt strength, friction, time limit) and replay from the end screen (`R`, `1`/`2`/`3`, `M`, `Esc`) | `Task 3: difficulty menu and replay` |
| 4 | Sound feedback for bounces, the goal and the time-out, synthesised at start-up (no binary assets, silent fallback when there is no audio device) | `Task 4: sound feedback (and repository tidy-up)` |

`code/tests/test_collision.py` (4 tests) covers the phantom-corner case, a real contact and tunnelling at top speed.

## Evidence in the videos

The capture runs add two diagnostic overlays: the **red square** is the old square hit-box, the **blue circle** is the
marble's real radius, and the HUD reports the clearance to the nearest wall at the moment a collision fires.

* `before.mp4` — "BOUNCE while still **+3.4 px** away from the wall" (red), i.e. the bug.
* `after.mp4` — "wall contact - correct bounce" (green) at 0 px, then the difficulty menu, a full round,
  **MAZE SOLVED / Finish time 6.29 s**, the `SFX:` indicator for the sound effects, and replay at a new difficulty.

## Running the game

```bash
cd code
pip install -r requirements.txt
python main.py
python tests/test_collision.py
```

| Key / input | Action |
| :--- | :--- |
| Mouse | Tilt the maze (the marble accelerates away from the screen centre) |
| `1` / `2` / `3` | Easy / Medium / Hard |
| `R` | Replay the same difficulty |
| `M` | Back to the difficulty menu |
| `Esc` | Quit |
