import pygame
import time
import random
from snake import Snake
from powerup_debuff import PowerUpOrDebuff  # Import the PowerUpOrDebuff class
from game import Game
from map import Map, Room, Pixel
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
    
    
    # Draw the map
    game_map = game.get_map()
    screen.fill(black)
    # Draw rooms
    wall_color = (77, 65, 41)
    door_color = (161, 103, 80)
    ceiling_color_not_occupied = (51, 43, 27)
    ceiling_color_occupied = (171, 141, 97)
    for room in game_map.rooms.values():
        pygame.draw.rect(screen, wall_color, pygame.Rect(room.pos[0], room.pos[1], room.get_width() * game.get_block_size(), room.get_height() * game.get_block_size()))
        if room.isoccupied:
            pygame.draw.rect(screen, ceiling_color_occupied, pygame.Rect(room.pos[0] + game.get_block_size(), room.pos[1] + game.get_block_size(), 
                                                                (room.get_width() -2) * game.get_block_size(), (room.get_height() - 2) * game.get_block_size()))
        else:
            pygame.draw.rect(screen, ceiling_color_not_occupied, pygame.Rect(room.pos[0] + game.get_block_size(), room.pos[1] + game.get_block_size(), 
                                                                (room.get_width() -2) * game.get_block_size(), (room.get_height() - 2) * game.get_block_size()))
        # Draw doors
        
        for door in room.doors.items():
            side, interval = door
            if side == "top":
                pygame.draw.rect(screen, door_color, pygame.Rect(room.pos[0] + interval[0] * game.get_block_size(), room.pos[1], (interval[1] - interval[0]) * game.get_block_size(), game.get_block_size()))
            elif side == "bottom":
                pygame.draw.rect(screen, door_color, pygame.Rect(room.pos[0] + interval[0] * game.get_block_size(), room.pos[1] + (room.get_height() - 1) * game.get_block_size(), (interval[1] - interval[0]) * game.get_block_size(), game.get_block_size()))
            elif side == "left":
                pygame.draw.rect(screen, door_color, pygame.Rect(room.pos[0], room.pos[1] + interval[0] * game.get_block_size(), game.get_block_size(), (interval[1] - interval[0]) * game.get_block_size()))
            elif side == "right":
                pygame.draw.rect(screen, door_color, pygame.Rect(room.pos[0] + (room.get_width() - 1) * game.get_block_size(), room.pos[1] + interval[0] * game.get_block_size(), game.get_block_size(), (interval[1] - interval[0]) * game.get_block_size()))

    # Draw the snakes
    for snake in game.get_snakes().values():
        # Determine snake color based on its state
        if snake.is_invincible():
            # Get current time and invincibility start time
            current_time = pygame.time.get_ticks()
            inv_start_time = snake.get_invincibility_start_time()
            
            # Safety check: inv_start_time should not be None
            if inv_start_time is None:
                print(f"Error: {snake.get_name()} is invincible but start time is not set.")
                snake_color = snake.get_color()
            else:
                elapsed_time = current_time - inv_start_time
                
                if elapsed_time < 2000:
                    # Phase 1: Flashing every 250 ms for the first 2 seconds
                    if (elapsed_time // 250) % 2 == 0:
                        snake_color = (0, 0, 0)  # Black
                    else:
                        snake_color = white  # White for flashing effect
                elif elapsed_time < 5000:
                    # Phase 2: Solid black for the next 3 seconds
                    snake_color = (0, 0, 0)  # Black
                else:
                    # Invincibility duration has ended; remove invincibility
                    print(f"{snake.get_name()} invincibility duration ended.")
                    snake.remove_invincibility()
                    snake_color = snake.get_color()  # Revert to original color
        elif snake.is_slowed_down():
            snake_color = gray  # Indicate slow down
        else:
            snake_color = snake.get_color()
        
        # Draw the snake's body
        for block in snake.get_body_segments():
            pygame.draw.rect(screen, snake_color, pygame.Rect(block[0], block[1], block_size, block_size))

        if snake.is_armor_active():
            armor_positions = snake.get_armor_positions()
            for pos in armor_positions:
                pygame.draw.rect(screen, gray, pygame.Rect(pos[0], pos[1], block_size, block_size))
    
    # Draw power-ups/debuffs
    for powerup in game.get_available_foods():
        pixels = game_map.get_pixels()

        if pixels[powerup.get_position()[1] // block_size, powerup.get_position()[0] // block_size] == 1:
            powerup.set_position((powerup.get_position()[0] // block_size + 1, powerup.get_position()[1] // block_size + 1))
            
        if (pixels[powerup.get_position()[1] // block_size, powerup.get_position()[0] // block_size] >=2 and 
            game_map.get_room(pixels[powerup.get_position()[1] // block_size, powerup.get_position()[0] // block_size]).is_occupied() == False):
            continue

        if powerup.item_type == "speed_boost":
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Yellow for speed boost
        elif powerup.item_type == "slow_down":
            pygame.draw.rect(screen, blue, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Blue for slow down debuff
        elif powerup.item_type == "invincibility":
            pygame.draw.rect(screen, white, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # White for invincibility
        elif powerup.item_type == "score_decrease":
            pygame.draw.rect(screen, (255,192,203), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Pink for score decrease
        elif powerup.item_type == "food_party":
            pygame.draw.rect(screen, green, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Pink for score decrease
        elif powerup.item_type == "normal":
            pygame.draw.rect(screen, red, pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # Red for normal fruit
        elif powerup.item_type == "armor":
            pygame.draw.rect(screen, (156,81,0), pygame.Rect(powerup.position[0], powerup.position[1], block_size, block_size))  # brown for armor fruit

    for room in game_map.rooms.values():
        room.isoccupied = False
    # Display scores
    score_display(game.get_scores())
    pygame.display.update()


def game_loop():
    # Initial snake setup
    game = Game(screen_size=(width, height), block_size=block_size)

    s1 = Snake([[100, 50], [50, 50]], name="Player 1",
               key_map={"UP": pygame.K_w, "DOWN": pygame.K_s, 
                        "LEFT": pygame.K_a, "RIGHT": pygame.K_d},
               color=(0, 0, 255), update_rate=15)  # Adjusted to default
    s2 = Snake([[1000, 680], [1050, 680]], name="Player 2",
               key_map={"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, 
                        "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT},
               color=(0, 255, 0), update_rate=15)  # Assign a color for Player 2
    game_map = game.get_map()

    food_per_room = 4
    # Add food to each room except the center room
    for room in game_map.rooms.values():
        if room.get_id() == 2:
            continue
        for i in range(food_per_room):
            game.add_food_to_room(room.get_id())

    for i in range(10):
        game.add_food_randomly()

        
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed. Quit game.")
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
