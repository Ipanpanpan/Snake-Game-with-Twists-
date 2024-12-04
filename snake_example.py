import pygame
import time
import random
from snake import Snake
from powerup_debuff import PowerUpOrDebuff  # Import the PowerUpOrDebuff class
from game import Game
# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 1280, 720

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)  # Gray for slow down indication

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

def score_display(score):
    """Display the score."""
    # Display scores for all players
    y_offset = 10
    for player, player_score in score.items():
        value = score_font.render(f"{player}: {player_score}", True, green)
        screen.blit(value, [10, y_offset])
        y_offset += 40  # Increment y position for the next score

def draw_game_state(game: Game):
    """Draw the game state on the screen."""
    screen.fill(black)
    for snake in game.get_snakes().values():
        # Determine snake color based on its state
        if snake.is_invincible():
            # Flashing effect for invincibility
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                snake_color = (0, 0, 0)  # Black
            else:
                snake_color = white  # White for flashing effect
        elif snake.is_slowed_down():
            snake_color = gray  # Indicate slow down
        else:
            snake_color = snake.get_color()
        
        for block in snake.get_body_segments():
            pygame.draw.rect(screen, snake_color, pygame.Rect(block[0], block[1], block_size, block_size))
    for powerup in game.get_available_foods():
        if powerup.item_type == "speed_boost":
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Yellow for speed boost
        elif powerup.item_type == "slow_down":
            pygame.draw.rect(screen, blue, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Blue for slow down debuff
        elif powerup.item_type == "invincibility":
            pygame.draw.rect(screen, white, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # White for invincibility
        elif powerup.item_type == "score_decrease":
            pygame.draw.rect(screen, (255, 192, 203), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Pink for score decrease
        elif powerup.item_type == "food_party":
            pygame.draw.rect(screen, green, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Pink for score decrease
        elif powerup.item_type == "normal":
            pygame.draw.rect(screen, red, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Red for normal fruit
    score_display(game.get_scores())
    pygame.display.update()

def game_loop():
    # Initial snake setup
    game = Game(screen_size=(width, height), block_size=block_size)

    s1 = Snake([[100, 50], [50, 50]], name="Player 1",
               key_map={"UP": pygame.K_w, "DOWN": pygame.K_s, 
                        "LEFT": pygame.K_a, "RIGHT": pygame.K_d},
               color=(0, 0, 255), update_rate=15)  # Adjusted to default
    s2 = Snake([[1000, 1000], [1000, 1050]], name="Player 2",
               key_map={"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, 
                        "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT},
               color=(0, 255, 0), update_rate=15)  # Assign a color for Player 2

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

        # Removed tick_speed logic as it's no longer needed
        clock.tick(game.get_fps())
    
    # After game over, display winner and close the game
    alive_snakes = [snake for snake in game.get_snakes().values() if snake.is_alive()]
    if len(alive_snakes) == 1:
        winner = alive_snakes[0].get_name()
        print(f"{winner} wins the game!")
        # Display winner on the screen for a short duration before closing
        screen.fill(black)
        message(f"{winner} wins the game!", green, width // 3, height // 2)
        pygame.display.update()
        pygame.time.delay(3000)  # Display for 3 seconds
    else:
        print("No winners. All snakes are dead.")
        # Optionally, display a tie message
        screen.fill(black)
        message("No winners. All snakes are dead.", red, width // 3, height // 2)
        pygame.display.update()
        pygame.time.delay(3000)  # Display for 3 seconds
    
    pygame.quit()
    quit()

# Run the game
if __name__ == "__main__":
    game_loop()
