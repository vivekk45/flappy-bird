import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = 0.25
JUMP_STRENGTH = -6
PIPE_WIDTH = 50
PIPE_GAP = 175
BIRD_RADIUS = 20
PIPE_VELOCITY = 2.5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets (you can use your own images or colors for background and bird)
bird_img = pygame.Surface((BIRD_RADIUS*2, BIRD_RADIUS*2))
bird_img.fill(BIRD_COLOR)

# Define the Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y > HEIGHT - BIRD_RADIUS * 2:
            self.y = HEIGHT - BIRD_RADIUS * 2
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self, screen):
        screen.blit(bird_img, (self.x, self.y))

# Define the Pipe class
class  Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP

    def update(self):
        self.x -= PIPE_VELOCITY

    def draw(self, screen):
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.top))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.bottom, PIPE_WIDTH, HEIGHT - self.bottom))

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        # Collision with top pipe
        if bird.x + BIRD_RADIUS > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.top or bird.y + BIRD_RADIUS * 2 > self.bottom:
                return True
        return False

# Main game loop
def game():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()

        # Add new pipe
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Update pipes
        for pipe in pipes[:]:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                score += 1

            if pipe.collide(bird):
                running = False

            pipe.draw(screen)

        bird.draw(screen)

        # Draw the score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    str(input("enter your name:"))
    print(f"Game Over! Your score is {score}")

if __name__ == "__main__":
    game()
