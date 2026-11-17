import pygame

from game.game_engine import GameEngine

# Screen dimensions
WIDTH, HEIGHT = 600, 500
FPS = 60


def main():
    # Initialize pygame / start application
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Marble Tilt Maze - Pygame Version")

    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            engine.handle_event(event)

        # input + physics + collision all live in the engine
        engine.update()
        engine.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

        if engine.should_quit:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
