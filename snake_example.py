import pygame
import time
import random
from snake import Snake
from powerup_debuff import PowerUpOrDebuff  # Import the PowerUpOrDebuff class

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
    """Display a message on the screen at a specific position."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])

# Get random position on screen for food and power-ups
def get_random_position():
    return [random.randrange(1, (width // block_size)) * block_size,
            random.randrange(1, (height // block_size)) * block_size]

def score_display(score):
    """Display the score."""
    value = score_font.render(f"Score: {score}", True, green)
    screen.blit(value, [10, 10])

def game_loop():
    # Initial snake setup
    running = True
    Snake.set_block_size(block_size)
    s1 = Snake([[100, 50], [50, 50]])

    direction = s1.get_direction()
    change_to = direction

    # Initial food position
    food_pos = get_random_position()
    food_spawn = True

    # Initial score
    score = 0

    # Spawn random power-up or debuff (includes freeze debuff)
    powerup = PowerUpOrDebuff.spawn()

    running = True
    while running:
        # Event handling (moving snake, quitting the game, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
        s1.update()  # Update snake position (handle freeze here)

        # Check for collision with power-up or debuff
        if s1.get_head_position() == powerup.position:
            powerup.apply_effect(s1)  # Apply the freeze or speed boost effect
            score += 10  # Award points for picking up the item
            powerup = PowerUpOrDebuff.spawn()  # Spawn a new power-up/debuff

        # Edge of screen handling (wrap around)
        if s1.get_head_position()[0] < 0:
            s1.set_head_positions([width - block_size, s1.get_head_position()[1]])
        elif s1.get_head_position()[0] >= width:
            s1.set_head_positions([0, s1.get_head_position()[1]])
        elif s1.get_head_position()[1] < 0:
            s1.set_head_positions([s1.get_head_position()[0], height - block_size])
        elif s1.get_head_position()[1] >= height:
            s1.set_head_positions([s1.get_head_position()[0], 0])

        # Eat food
        if s1.get_head_position() == food_pos:
            s1.eat(1)
            s1.add_body_segment()  # Add a new segment to the body
            score += 10
            food_spawn = False

        # Spawn new food
        if not food_spawn:
            food_pos = get_random_position()
        food_spawn = True

        # Update screen
        screen.fill(black)
        for block in s1.get_body_segments():
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], block_size, block_size))
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))

        # Draw the power-up or debuff
        if powerup.item_type == "speed_boost":
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Yellow for speed boost
        elif powerup.item_type == "freeze":
            pygame.draw.rect(screen, blue, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Blue for freeze debuff

        score_display(score)
        pygame.display.update()

        # Check if snake is still alive
        if not s1.is_alive():
            game_over_screen(score)  # Call game over screen when the snake is dead
            running = False

        # Control speed (adjust for speed boost if active)
        if s1._Snake__is_speed_boosted:  # Check if speed boost is active
            clock.tick(snake_speed * 5)  # Speed up the game loop if speed boost is active
        elif s1._Snake__is_frozen:  # Snake movement is slowed down or halted when frozen
            clock.tick(snake_speed / 2)  # Slow down game speed if frozen
        else:
            
            clock.tick(snake_speed)  # Regular game speed
        # In the game loop, we need to check if the snake is frozen and prevent movement
        if s1._Snake__is_frozen:
            clock.tick(snake_speed)  # Snake movement is slowed down or halted when frozen
        else:
            clock.tick(snake_speed)

        
def game_over_screen(score):
    """Show game over screen with score and restart options."""
    screen.fill(black)
    message("Game Over!", red, width // 3, height // 3)
    message(f"Your score: {score}", white, width // 3, height // 2)
    message("Press R to Restart or Q to Quit", white, width // 4, height // 1.5)
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Run the game
game_loop()
