"""Game engine for the Marble Tilt Maze.

Lab 4 changes (see CHANGES.md):
  Task 1 - collision is now a true circle-vs-rectangle test with sub-stepping,
           so the marble only bounces when its round edge touches a wall.
  Task 2 - the round ends on screen (win with finish time, or time-out) and
           waits for input instead of printing to the console.
  Task 3 - a difficulty menu and replay: Easy / Medium / Hard control tilt
           strength, friction and the time limit.
  Task 4 - sound feedback for bounces, the goal and the time-out.
"""
import math

import pygame

from .marble import Marble
from .sounds import SoundBank
from .wall import Wall

WHITE = (255, 255, 255)
DARK = (40, 40, 50)
WALL_COLOR = (90, 90, 110)
GOAL_COLOR = (60, 200, 120)
HUD_COLOR = (210, 216, 228)
ACCENT = (120, 190, 255)
WIN_COLOR = (90, 220, 140)
LOSE_COLOR = (240, 110, 110)

RESTITUTION = 0.45          # how bouncy the walls are
BOUNCE_SOUND_MIN = 1.2      # only play a bounce sound above this impact speed


class GameEngine:
    # ---------------------------------------------------------------- states
    MENU = "menu"
    PLAYING = "playing"
    END = "end"

    DIFFICULTIES = {
        "Easy": {"tilt": 0.35, "friction": 0.030, "time_limit_ms": 60000,
                 "blurb": "gentle tilt, high friction, 60 s"},
        "Medium": {"tilt": 0.60, "friction": 0.020, "time_limit_ms": 45000,
                   "blurb": "balanced tilt, 45 s"},
        "Hard": {"tilt": 0.95, "friction": 0.012, "time_limit_ms": 30000,
                 "blurb": "strong tilt, low friction, 30 s"},
    }

    def __init__(self, width, height, start_state=None):
        self.width = width
        self.height = height

        self.walls = self._build_maze()
        self.goal_x, self.goal_y, self.goal_radius = width - 60, height - 60, 22

        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 34, bold=True)

        self.sounds = SoundBank()

        self.difficulty = "Medium"
        self.game_over = False
        self.result = None            # "solved" / "timeout"
        self.finish_time_ms = None
        self.should_quit = False

        self.marble = Marble(50, 50)
        self.tilt_strength = 0.6
        self.friction = 0.02
        self.max_speed = 9
        self.time_limit_ms = 45000
        self.start_ticks = pygame.time.get_ticks()

        self.state = start_state or self.MENU
        self._last_bounce_ms = -1000
        if self.state == self.PLAYING:
            self.start_round(self.difficulty)

    # ---------------------------------------------------------------- setup
    def _build_maze(self):
        walls = []
        t = 16  # wall thickness

        # outer boundary
        walls.append(Wall(0, 0, self.width, t))
        walls.append(Wall(0, self.height - t, self.width, t))
        walls.append(Wall(0, 0, t, self.height))
        walls.append(Wall(self.width - t, 0, t, self.height))

        # a few internal walls forming a simple winding path
        walls.append(Wall(0, 140, self.width - 140, t))
        walls.append(Wall(140, 260, self.width - 140, t))
        walls.append(Wall(0, 380, self.width - 140, t))

        return walls

    def apply_difficulty(self, name):
        cfg = self.DIFFICULTIES[name]
        self.difficulty = name
        self.tilt_strength = cfg["tilt"]
        self.friction = cfg["friction"]
        self.time_limit_ms = cfg["time_limit_ms"]

    def start_round(self, difficulty=None):
        if difficulty:
            self.apply_difficulty(difficulty)
        self.marble.x, self.marble.y = 50.0, 50.0
        self.marble.vx = self.marble.vy = 0.0
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.result = None
        self.finish_time_ms = None
        self.state = self.PLAYING

    # ---------------------------------------------------------------- input
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.should_quit = True
            return
        if event.type != pygame.KEYDOWN:
            return

        key = event.key
        if key == pygame.K_ESCAPE:
            self.should_quit = True
            return

        if self.state == self.MENU:
            choice = {pygame.K_1: "Easy", pygame.K_2: "Medium", pygame.K_3: "Hard"}.get(key)
            if choice:
                self.start_round(choice)

        elif self.state == self.END:
            if key == pygame.K_r:
                self.start_round(self.difficulty)      # replay the same difficulty
            elif key == pygame.K_m:
                self.state = self.MENU
            else:
                choice = {pygame.K_1: "Easy", pygame.K_2: "Medium", pygame.K_3: "Hard"}.get(key)
                if choice:
                    self.start_round(choice)

    def handle_input(self):
        """Kept for backwards compatibility with the original main loop."""
        if self.state != self.PLAYING:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.width // 2
        dy = mouse_y - self.height // 2
        dist = max(1.0, math.hypot(dx, dy))
        self.marble.vx += (dx / dist) * self.tilt_strength
        self.marble.vy += (dy / dist) * self.tilt_strength

    # ---------------------------------------------------------------- update
    def update(self):
        if self.state != self.PLAYING:
            return

        elapsed = pygame.time.get_ticks() - self.start_ticks
        if elapsed >= self.time_limit_ms:
            self._end_round("timeout")
            return

        self.handle_input()

        self.marble.vx *= (1 - self.friction)
        self.marble.vy *= (1 - self.friction)

        speed = math.hypot(self.marble.vx, self.marble.vy)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.marble.vx *= scale
            self.marble.vy *= scale
            speed = self.max_speed

        # Sub-step so a fast marble can never tunnel through a 16 px wall.
        steps = max(1, int(math.ceil(speed / (self.marble.radius * 0.5))))
        for _ in range(steps):
            self.marble.x += self.marble.vx / steps
            self.marble.y += self.marble.vy / steps
            self._resolve_wall_collisions()

        gx = self.goal_x - self.marble.x
        gy = self.goal_y - self.marble.y
        if math.hypot(gx, gy) <= self.goal_radius:
            self._end_round("solved")

    def _end_round(self, result):
        self.game_over = True
        self.result = result
        if result == "solved":
            self.finish_time_ms = pygame.time.get_ticks() - self.start_ticks
            self.sounds.goal()
        else:
            self.sounds.timeout()
        self.state = self.END

    # ---------------------------------------------------------------- physics
    def _hit(self, wall):
        """Circle vs rectangle: returns (nx, ny, penetration) or None."""
        r = wall.rect()
        m = self.marble
        closest_x = min(max(m.x, r.left), r.right)
        closest_y = min(max(m.y, r.top), r.bottom)
        dx, dy = m.x - closest_x, m.y - closest_y
        d2 = dx * dx + dy * dy
        radius = m.radius
        if d2 > radius * radius:
            return None                      # the round marble does not touch the wall

        if d2 > 1e-9:                        # touching an edge or a corner
            d = math.sqrt(d2)
            return dx / d, dy / d, radius - d

        # Centre is inside the rectangle: push out along the shallowest axis.
        left, right = m.x - r.left, r.right - m.x
        top, bottom = m.y - r.top, r.bottom - m.y
        smallest = min(left, right, top, bottom)
        if smallest == left:
            return -1.0, 0.0, left + radius
        if smallest == right:
            return 1.0, 0.0, right + radius
        if smallest == top:
            return 0.0, -1.0, top + radius
        return 0.0, 1.0, bottom + radius

    def _resolve_wall_collisions(self):
        for _ in range(3):                   # a couple of passes settle corner hits
            moved = False
            for wall in self.walls:
                hit = self._hit(wall)
                if hit is None:
                    continue
                nx, ny, penetration = hit
                self.marble.x += nx * penetration
                self.marble.y += ny * penetration

                vn = self.marble.vx * nx + self.marble.vy * ny
                if vn < 0:                   # move only if closing on the wall
                    self.marble.vx -= (1 + RESTITUTION) * vn * nx
                    self.marble.vy -= (1 + RESTITUTION) * vn * ny
                    self._play_bounce(-vn)
                moved = True
            if not moved:
                break

    def _play_bounce(self, impact_speed):
        if impact_speed < BOUNCE_SOUND_MIN:
            return
        now = pygame.time.get_ticks()
        if now - self._last_bounce_ms < 90:   # do not machine-gun the sound
            return
        self._last_bounce_ms = now
        self.sounds.bounce(min(1.0, impact_speed / self.max_speed))

    # ---------------------------------------------------------------- render
    def render(self, screen):
        screen.fill(DARK)

        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall.rect())

        pygame.draw.circle(screen, GOAL_COLOR, (self.goal_x, self.goal_y), self.goal_radius)
        pygame.draw.circle(screen, WHITE, (int(self.marble.x), int(self.marble.y)), self.marble.radius)

        if self.state != self.MENU:
            self._render_hud(screen)

        if self.state == self.MENU:
            self._render_menu(screen)
        elif self.state == self.END:
            self._render_end(screen)

    def _render_hud(self, screen):
        elapsed = pygame.time.get_ticks() - self.start_ticks
        remaining = self.time_limit_ms - elapsed
        if self.state == self.END and self.result == "solved" and self.finish_time_ms is not None:
            label = "Solved in %.1fs" % (self.finish_time_ms / 1000.0)
            color = WIN_COLOR
        else:
            label = "Time: %ds" % max(0, remaining // 1000)
            color = WHITE if remaining > 5000 else LOSE_COLOR
        screen.blit(self.font.render(label, True, color), (10, 10))
        screen.blit(self.small_font.render(self.difficulty, True, HUD_COLOR),
                    (self.width - 90, 14))

    def _panel(self, screen, alpha=225):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((12, 14, 20, alpha))
        screen.blit(overlay, (0, 0))

    def _render_menu(self, screen):
        self._panel(screen, 235)
        w = self.width
        title = self.title_font.render("MARBLE TILT MAZE", True, ACCENT)
        screen.blit(title, (w // 2 - title.get_width() // 2, 90))
        sub = self.small_font.render("Tilt the maze with the mouse. Reach the green goal.",
                                     True, HUD_COLOR)
        screen.blit(sub, (w // 2 - sub.get_width() // 2, 135))
        prompt = self.font.render("Choose a difficulty", True, WHITE)
        screen.blit(prompt, (w // 2 - prompt.get_width() // 2, 190))

        y = 240
        for i, name in enumerate(("Easy", "Medium", "Hard"), start=1):
            cfg = self.DIFFICULTIES[name]
            line = "%d   %-6s  -  %s" % (i, name, cfg["blurb"])
            color = ACCENT if name == self.difficulty else HUD_COLOR
            screen.blit(self.small_font.render(line, True, color), (150, y))
            y += 34

        hint = self.small_font.render("Esc to quit", True, (150, 156, 170))
        screen.blit(hint, (w // 2 - hint.get_width() // 2, self.height - 40))

    def _render_end(self, screen):
        self._panel(screen, 225)
        w = self.width
        if self.result == "solved":
            title = self.big_font.render("MAZE SOLVED", True, WIN_COLOR)
            detail = "Finish time: %.2f s" % (self.finish_time_ms / 1000.0)
        else:
            title = self.big_font.render("TIME'S UP", True, LOSE_COLOR)
            detail = "The marble did not reach the goal."
        screen.blit(title, (w // 2 - title.get_width() // 2, 150))
        d = self.font.render(detail, True, WHITE)
        screen.blit(d, (w // 2 - d.get_width() // 2, 205))
        diff = self.small_font.render("Difficulty: %s" % self.difficulty, True, HUD_COLOR)
        screen.blit(diff, (w // 2 - diff.get_width() // 2, 240))

        options = [
            "R   replay %s" % self.difficulty,
            "1 / 2 / 3   new game: Easy / Medium / Hard",
            "M   back to menu        Esc   quit",
        ]
        y = 300
        for line in options:
            s = self.small_font.render(line, True, HUD_COLOR)
            screen.blit(s, (w // 2 - s.get_width() // 2, y))
            y += 28

        prompt = self.small_font.render("Waiting for your choice...", True, (150, 156, 170))
        screen.blit(prompt, (w // 2 - prompt.get_width() // 2, self.height - 40))
