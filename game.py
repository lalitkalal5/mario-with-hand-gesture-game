import pygame
import random
import sys
from hand_detector import HandDetector

pygame.init()

detector = HandDetector()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Jump Runner")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# -------- PLAYER --------
player_img = pygame.image.load("assets/jumpy.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60,60))

player_rect = player_img.get_rect()
player_rect.x = 100
player_rect.y = 300

# Physics
gravity = 0.5
vy = 0
ground = 300

# -------- OBSTACLE --------
obstacle = pygame.Surface((30, 40))
obstacle.fill(RED)
obstacle_rect = obstacle.get_rect()

obstacle_rect.x = 800      # start from right side
obstacle_rect.bottom = ground + 60

obstacle_speed = 5

# Game state
game_over = False

running = True
restart_rect = pygame.Rect(300, 200, 200, 50)  # x, y, width, height

def reset_game():
    global game_over, player_rect, vy, obstacle_rect

    game_over = False
    vy= 0 

    player_rect.x = 100
    player_rect.y = ground

    obstacle_rect.x = 800

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_rect.collidepoint(event.pos):
                reset_game()
    
    hand_up, hand_y = detector.get_hand_up()

    keys = pygame.key.get_pressed()
    dx = 0
    if hand_up and player_rect.y == ground:
        vy = -12
    if keys[pygame.K_SPACE] and player_rect.y == ground:
        vy = -12
    if keys[pygame.K_LEFT]:        
        dx = -10
    if keys[pygame.K_RIGHT]:
        dx = 10
    if keys[pygame.K_DOWN]:
        vy = 5
    if keys[pygame.K_UP] and player_rect.y == ground:
        vy = -15

    if player_rect.left + dx <= 0:
        player_rect.left = 0 
        print(dx,"dx vala he agar kam ho raha he to")

    if player_rect.right + dx >= WIDTH:
        player_rect.right = WIDTH

    player_rect.x += dx 

    if not game_over:
        # Apply gravity
        vy += gravity
        player_rect.y += vy

        if player_rect.y >= ground:
            player_rect.y = ground
            vy = 0

        # Move obstacle
        obstacle_rect.x -= obstacle_speed

        # Reset obstacle when it leaves screen
        if obstacle_rect.right < 0:
            obstacle_rect.x = 800

            random_height = random.randint(20,80)
            obstacle = pygame.Surface((30, random_height))

            obstacle.fill(RED)
            obstacle_rect = obstacle.get_rect()

            obstacle_rect.x = 800      # start from right side
            obstacle_rect.bottom = ground + 60

        # Check collision
        if player_rect.colliderect(obstacle_rect):
            game_over = True

    # -------- DRAWING --------
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (0, ground+60), (WIDTH, ground+60), 3)

    screen.blit(player_img, player_rect)
    screen.blit(obstacle, obstacle_rect)

    # Show "Game Over"
    if game_over:
        font = pygame.font.Font(None, 50)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (300, 150))
            
        pygame.draw.rect(screen, BLACK, restart_rect)
        btn_text = font.render("RESTART", True, WHITE)
        screen.blit(btn_text, (restart_rect.x + 40, restart_rect.y + 10))

    pygame.display.update()
