import pygame
import time
import random
from snake import Snake
from powerup_debuff import PowerUpOrDebuff  # Import the PowerUpOrDebuff class
from game import Game
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

def draw_game_state(game : Game):
    """Draw the game state on the screen."""
    screen.fill(black)
    for snake in game.get_snakes().values():
        for block in snake.get_body_segments():
            pygame.draw.rect(screen, snake.get_color(), pygame.Rect(block[0], block[1], block_size, block_size))
    for powerup in game.get_available_foods():
        if powerup.item_type == "speed boost":
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Yellow for speed boost
        elif powerup.item_type == "freeze":
            pygame.draw.rect(screen, blue, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Blue for freeze debuff
        elif powerup.item_type == "normal":
            pygame.draw.rect(screen, red, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))
    score_display(game.get_scores())
    pygame.display.update()

def game_loop():
    # Initial snake setup
    game = Game(screen_size=(width, height), block_size=block_size)

    s1 = Snake([[100, 50], [50, 50]], name = "Player 1", key_map={"UP" : pygame.K_w, "DOWN" : pygame.K_s, "LEFT" : pygame.K_a, "RIGHT" : pygame.K_d}, color = (0, 0, 255), update_rate= 40)
    s2 = Snake([[1000, 1000], [1000, 1050]], name = "Player 2", key_map={"UP" : pygame.K_UP, "DOWN" : pygame.K_DOWN, "LEFT" : pygame.K_LEFT, "RIGHT" : pygame.K_RIGHT})

    game.add_snake(s1)
    game.add_snake(s2)
    
    while not game.is_game_over():
        # Event handling (moving snake, quitting the game, etc.)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("Quit")
                pygame.quit()
                quit()
        game.update(events)
        draw_game_state(game)

        s1 : Snake = game.get_snakes()["Player 1"]
        if s1.is_speed_boosted():
            tick_speed = snake_speed * 5
        elif s1.is_frozen():
            tick_speed = snake_speed / 2
        else:
            tick_speed = snake_speed
        clock.tick(game.get_fps())

        
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
if __name__ == "__main__":
    game_loop()
