import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pause One Object Example")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.paused = False  # Pause flag

    def update(self):
        if not self.paused:  # Only move if not paused
            self.rect.x += self.speed
            # Wrap around screen
            if self.rect.right > WIDTH:
                self.rect.left = 0

# Create two objects
obj1 = MovingObject(RED, (100, 200), 3)
obj2 = MovingObject(BLUE, (300, 200), 2)

# Sprite group
all_sprites = pygame.sprite.Group(obj1, obj2)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Toggle pause for obj1 when pressing SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                obj1.paused = not obj1.paused

    # Update sprites
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display pause text for obj1
    if obj1.paused:
        font = pygame.font.Font(None, 36)
        text = font.render("Obj1 Paused", True, (0, 0, 0))
        screen.blit(text, (obj1.rect.x, obj1.rect.y - 30))

    pygame.display.flip()
    clock.tick(60)