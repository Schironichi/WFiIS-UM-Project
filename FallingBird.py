import pygame

# Initialize Pygame
pygame.init()
positions = [30, 172, 397, 319, 402, 76, 80, 504, 45, 88, 539, 246, 563, 60, 
                   409, 503, 358, 452, 261, 406, 63, 466, 334, 187, 432, 179, 332, 
                   59, 622, 536, 523, 154, 307, 540, 344, 528, 195, 123, 295, 162, 
                   586, 145, 207, 395, 364, 481, 443, 114, 670, 579, 395, 293, 375, 
                   579, 234, 144, 302, 178, 31, 292, 285, 596, 59, 168, 240, 24, 212, 
                   304, 303, 373, 99, 323, 114, 284, 374, 498, 624, 565, 456, 472, 357, 
                   638, 111, 65, 431, 574, 297, 231, 455, 269, 473, 267, 572, 98, 457, 
                   46, 495, 63, 187, 352, 302, 178, 31, 292, 285]

# Set the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.display.set_caption("Falling Bird - DR PR KK")

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
BLUE = (0, 0, 255)

# Set the font
FONT = pygame.font.Font(None, 36)

# Set the game clock
clock = pygame.time.Clock()

# Set the player dimensions and position
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_X = WINDOW_WIDTH // 2
PLAYER_Y = 0

# Set the obstacle dimensions and speed
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 2

# Set the number of obstacles
NUM_OBSTACLES = 2

# Load the player image and scale it to the desired size
player_image = pygame.image.load('Kratos.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Create the player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create the player sprite
player = Player(PLAYER_X, PLAYER_Y)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create the obstacles
obstacle_rects = []
obstacle_rects.append([
    pygame.Rect(0, WINDOW_HEIGHT // 2, positions[0], OBSTACLE_HEIGHT),
    pygame.Rect(positions[0] + 2 * OBSTACLE_WIDTH, WINDOW_HEIGHT // 2, WINDOW_WIDTH - 2 * OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
])
obstacle_rects.append([
    pygame.Rect(0, WINDOW_HEIGHT, positions[1], OBSTACLE_HEIGHT),
    pygame.Rect(positions[1] + 2 * OBSTACLE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH - 2 * OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
])

# Set the initial score and game over flag
score = 0
game_over = False

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Game loop
while not game_over:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player.rect.left > 7:
            player.rect.move_ip(-8, 0)
    if keys[pygame.K_d]:
        if player.rect.right < WINDOW_WIDTH - 7:
            player.rect.move_ip(8, 0)

    # Move the obstacles down
    for obstacle_rect in obstacle_rects:
        obstacle_rect[0].move_ip(0, -OBSTACLE_SPEED)
        obstacle_rect[1].move_ip(0, -OBSTACLE_SPEED)

        # Check for collisions
        if player.rect.colliderect(obstacle_rect[0]) or player.rect.colliderect(obstacle_rect[1]) or score == 100:
            game_over = True

        # If the obstacle goes off the screen, move it back to the top
        if obstacle_rect[0].bottom <= 0 and not game_over:
            score += 1
            obstacle_rect[0] = pygame.Rect(0, WINDOW_HEIGHT, positions[score + 2], OBSTACLE_HEIGHT)
            obstacle_rect[1] = pygame.Rect(positions[score + 2] + 2 * OBSTACLE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH - 2 * OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player
    all_sprites.draw(screen)

    # Draw the obstacles
    for obstacle_rect in obstacle_rects:
        pygame.draw.rect(screen, GRAY, obstacle_rect[0])
        pygame.draw.rect(screen, GRAY, obstacle_rect[1])

    # Draw the score
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, WINDOW_HEIGHT- 30))

    # Update the screen
    pygame.display.update()

    # Set the game clock tick rate
    clock.tick(60)

# End the game
pygame.quit()
