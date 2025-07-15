import pygame
import math
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Angry Birds")

# Colors
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Slingshot base
SLING_X, SLING_Y = 150, HEIGHT - 100

class Bird:
    def __init__(self, x, y):
        self.radius = 15
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.color = RED
        self.dragging = False
        self.velocity = [0, 0]
        self.launched = False
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        if self.launched and self.active:
            self.velocity[1] += 0.5  # gravity
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            # Floor
            if self.y > HEIGHT - self.radius:
                self.y = HEIGHT - self.radius
                self.velocity = [0, 0]
                self.active = False

    def reset(self):
        self.x, self.y = self.init_x, self.init_y
        self.velocity = [0, 0]
        self.launched = False
        self.active = True


class Pig:
    def __init__(self, x, y):
        self.radius = 18
        self.x = x
        self.y = y
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, bird):
        if self.alive and bird.active:
            dist = math.hypot(self.x - bird.x, self.y - bird.y)
            if dist < self.radius + bird.radius:
                self.alive = False
                bird.active = False
                return True
        return False


def draw_slingshot(bird):
    if not bird.launched:
        pygame.draw.line(screen, BROWN, (SLING_X, SLING_Y), (bird.x, bird.y), 5)


def draw_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))


def draw_reset():
    pygame.draw.rect(screen, (200, 200, 200), (850, 20, 120, 40))
    text = font.render("Reset", True, BLACK)
    screen.blit(text, (880, 30))


# Game setup
birds = [Bird(SLING_X, SLING_Y) for _ in range(3)]
current_bird = birds.pop(0)
pigs = [Pig(random.randint(700, 900), HEIGHT - 30) for _ in range(5)]

score = 0
running = True

# Main loop
while running:
    screen.fill(WHITE)

    draw_slingshot(current_bird)
    draw_score(score)
    draw_reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 850 <= mx <= 970 and 20 <= my <= 60:
                # Reset everything
                birds = [Bird(SLING_X, SLING_Y) for _ in range(3)]
                current_bird = birds.pop(0)
                pigs = [Pig(random.randint(700, 900), HEIGHT - 30) for _ in range(5)]
                score = 0
                continue

            if not current_bird.launched:
                if math.hypot(mx - current_bird.x, my - current_bird.y) <= current_bird.radius:
                    current_bird.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_bird.dragging:
                current_bird.dragging = False
                current_bird.launched = True
                dx = SLING_X - pygame.mouse.get_pos()[0]
                dy = SLING_Y - pygame.mouse.get_pos()[1]
                current_bird.velocity = [dx / 5, dy / 5]

    if current_bird.dragging:
        current_bird.x, current_bird.y = pygame.mouse.get_pos()

    current_bird.update()
    current_bird.draw()

    for pig in pigs:
        if pig.check_collision(current_bird):
            score += 1
        pig.draw()

    if not current_bird.active and birds:
        current_bird = birds.pop(0)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
