"""Collision regression tests for the Marble Tilt Maze (Lab 4, Task 1).

Run with:  python tests/test_collision.py

No test framework is required: the file exits non-zero on the first failure, so
it also works as a CI job. Headless (SDL dummy video driver).
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import pygame

pygame.init()
pygame.display.set_mode((600, 500))

from game.game_engine import GameEngine


def fresh(mx, my, vx=0.0, vy=0.0):
    engine = GameEngine(600, 500)
    engine.marble.x, engine.marble.y = mx, my
    engine.marble.vx, engine.marble.vy = vx, vy
    return engine


def distance_to_walls(engine):
    m = engine.marble
    best = 1e9
    for wall in engine.walls:
        r = wall.rect()
        cx = min(max(m.x, r.left), r.right)
        cy = min(max(m.y, r.top), r.bottom)
        best = min(best, ((m.x - cx) ** 2 + (m.y - cy) ** 2) ** 0.5 - m.radius)
    return best


def test_no_bounce_while_gap():
    """A marble that does not touch a wall must not be pushed or reflected."""
    # just above the first internal wall (top edge y=140, radius 12)
    for gap in (0.5, 1.0, 3.0, 4.9):
        engine = fresh(300, 140 - 12 - gap, 0.0, 2.0)
        engine._resolve_wall_collisions()
        assert distance_to_walls(engine) >= gap - 1e-6, "marble moved while not touching"
        assert engine.marble.vy == 2.0, "velocity changed while not touching (gap %.1f)" % gap


def test_corner_gap_does_not_bounce():
    """The old bounding box bounced here; the circle must not (Task 1 bug)."""
    # 45 degrees off the corner at (460, 140): 15.5 px from the corner > radius 12
    engine = fresh(471.0, 129.0, -1.5, 1.5)
    before = (engine.marble.vx, engine.marble.vy)
    engine._resolve_wall_collisions()
    assert distance_to_walls(engine) > 0, "phantom collision resolved"
    assert (engine.marble.vx, engine.marble.vy) == before, "phantom bounce at a corner"


def test_contact_bounces():
    """A real overlap must separate the marble and reverse the approach."""
    engine = fresh(300, 140 - 12 + 2, 0.0, 3.0)   # 2 px into the wall
    engine._resolve_wall_collisions()
    assert distance_to_walls(engine) >= -1e-6, "marble left overlapping the wall"
    assert engine.marble.vy < 0, "velocity was not reflected away from the wall"


def test_no_tunneling_at_max_speed():
    """A 9 px/frame marble must not pass through a 16 px wall."""
    engine = fresh(300, 60, 0.0, 0.0)
    engine.marble.vy = 9.0
    for _ in range(40):
        engine.update()
    assert engine.marble.y < 200, "marble tunnelled through the first wall"


if __name__ == "__main__":
    tests = [test_no_bounce_while_gap, test_corner_gap_does_not_bounce,
             test_contact_bounces, test_no_tunneling_at_max_speed]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print("\nAll %d collision tests passed." % len(tests))
