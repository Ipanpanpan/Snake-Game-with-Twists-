import pygame
import time
import random
from snake import Snake


# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 600, 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Clock and speed
clock = pygame.time.Clock()
snake_speed = 15

# Snake block size
block_size = 10

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def message(msg, color, x, y):
    """Display a message on the screen."""
    message_surface = font_style.render(msg, True, color)
    screen.blit(message_surface, [x, y])

def score_display(score):
    """Display the score."""
    value = score_font.render(f"Score: {score}", True, green)
    screen.blit(value, [10, 10])

def game_loop():
    # Initial snake setup

    Snake.set_block_size(block_size)

    s1 = Snake([[100, 50], [50, 50]])

    direction = s1.get_direction()
    change_to = direction

    # Initial food position
    food_pos = [random.randrange(1, (width // block_size)) * block_size,
                random.randrange(1, (height // block_size)) * block_size]
    food_spawn = True

    # Initial score
    score = 0

    running = True
    while running:

        # Change direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
        s1.set_direction(change_to)
        s1.update()

        #Edge of screen handling
        new_pos = s1.get_head_position()
        if (s1.get_head_position()[0] < 0):
            new_pos[0] = width
            s1.set_head_positions(new_pos)
            
        elif s1.get_head_position()[0] >= width:
            new_pos[0] = 0
            s1.set_head_positions(new_pos)
            
        elif s1.get_head_position()[1] < 0:
            new_pos[1] = height
            s1.set_head_positions(new_pos)

        elif s1.get_head_position()[1] >= height:
            new_pos[1] = 0
            s1.set_head_positions(new_pos)


        #Eat fruit
        if s1.get_head_position() == food_pos:
            s1.eat(1)
            score += 10
            food_spawn = False


        #Spawn Food
        if not food_spawn:
            food_pos = [random.randrange(1, (width // block_size)) * block_size,
                        random.randrange(1, (height // block_size)) * block_size]
        food_spawn = True

        
        # Game over conditions
        if not s1.is_alive():
            running = False


        # Update screen
        screen.fill(black)
        for block in s1.get_body_segments():
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], block_size, block_size))
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))
        score_display(score)
        pygame.display.update()

        # Control speed
        clock.tick(snake_speed)


    # Game over message
    screen.fill(black)
    message("Game Over!", red, width // 3, height // 3)
    message(f"Your score: {score}", white, width // 3, height // 2)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()

# Run the game
game_loop()
