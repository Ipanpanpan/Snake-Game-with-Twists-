from powerup_debuff import PowerUpOrDebuff
from typing import List, Dict
import numpy.random as np_random
from snake import Snake
import pygame
import numpy as np

class Game:

    def __init__(self, screen_size, block_size, min_foods=10, fps=60):
        self.__block_size = block_size  # block size in pixels
        self.__screen_size = screen_size  # (width, height)

        self.__foods: List[PowerUpOrDebuff] = [] 
        self.__min_foods: int = min_foods
        
        self.__snakes: Dict[str, Snake] = {}

        self.__is_game_over = False
        self.__fps = fps

        self.__frame_counter = 0
        Snake.__block_size = block_size
    
    # Setters
    def set_block_size(self, block_size):
        self.__block_size = block_size
    
    def set_screen_size(self, width, height):
        self.__screen_size = (width, height)
    
    def add_food(self, food: PowerUpOrDebuff):
        self.__foods.append(food)
    
    def set_min_foods(self, min_foods):
        self.__min_foods = min_foods

    def add_snake(self, snake: Snake):
        assert snake.get_name() not in self.__snakes, "Name already exists"
        for segment in snake.get_body_segments():
            assert segment[0] % self.__block_size == 0 and segment[1] % self.__block_size == 0, "Invalid segment position"
        self.__snakes[snake.get_name()] = snake
    
    # Getters
    def get_block_size(self):
        return self.__block_size
    
    def get_screen_size(self):
        return self.__screen_size

    def get_available_foods(self):
        return self.__foods.copy()
    
    def get_min_foods(self):
        return self.__min_foods
    
    def get_snakes(self):
        return self.__snakes.copy()
    
    def get_scores(self):
        return {name: snake.get_score() for name, snake in self.__snakes.items()}

    def get_fps(self):
        return self.__fps

    def is_game_over(self):
        return self.__is_game_over

    def update_snake(self, snake: Snake):
        current_time = pygame.time.get_ticks()

        # Handle speed boost expiration
        if snake.is_speed_boosted() and current_time > snake.get_speed_boost_end_time():
            snake.remove_speed_boost()  # End speed boost after the duration expires
            print(f"{snake.get_name()} has had their speed boost removed.")
    
        # Handle slow down expiration
        if snake.is_slowed_down() and current_time > snake.get_slow_down_end_time():
            snake.remove_slow_down()  # End slow down after the duration expires
            print(f"{snake.get_name()} has recovered from slow down.")

        # Handle invincibility expiration
        if snake.is_invincible() and current_time > snake.get_invincibility_end_time():
            snake.remove_invincibility()  # End invincibility after the duration expires
            print(f"{snake.get_name()} is no longer invincible.")

        # Adjust snake's update rate based on effects
        if snake.is_slowed_down():
            # Dramatically slow down: halve the update rate, with a minimum of 1
            slow_down_update_rate = max(1, snake.get_update_rate() // 2)
            snake.set_update_rate(slow_down_update_rate)
            print(f"{snake.get_name()} is slowed down. Update rate set to {slow_down_update_rate}.")
        else:
            # Reset to default update rate if not slowed down
            default_update_rate = 15  # Adjust as per your game's default
            snake.set_update_rate(default_update_rate)
            print(f"{snake.get_name()}'s update rate reset to {default_update_rate}.")

        if snake.is_speed_boosted():
            # Double the update rate for speed boost
            boosted_update_rate = snake.get_update_rate() * 2
            snake.set_update_rate(boosted_update_rate)
            print(f"{snake.get_name()} has a speed boost. Update rate set to {boosted_update_rate}.")

        # Handle eating food
        for i, food in enumerate(self.__foods):
            if food.get_position() == snake.get_head_position():
                food.apply_effect(snake)
                self.__foods.pop(i)

        # Add food if below minimum
        if self.__min_foods > len(self.__foods):
            new_food = PowerUpOrDebuff.spawn()
            # Prevent spawning on snakes or existing foods
            while new_food.get_position() in [segment for s in self.__snakes.values() for segment in s.get_body_segments()] or new_food.get_position() in [food.get_position() for food in self.__foods]:
                new_food = PowerUpOrDebuff.spawn()
            self.__foods.append(new_food)

        # Movement logic
        frame_interval = self.__fps // snake.get_update_rate()
        if self.__frame_counter % frame_interval == 0:
            if snake.get_direction() == 'UP':
                snake.offset_head_position(offset_y=-self.__block_size)
            elif snake.get_direction() == 'DOWN':
                snake.offset_head_position(offset_y=self.__block_size)
            elif snake.get_direction() == 'LEFT':
                snake.offset_head_position(offset_x=-self.__block_size)
            elif snake.get_direction() == 'RIGHT':
                snake.offset_head_position(offset_x=self.__block_size)

            snake.insert_segment(snake.get_head_position(), 0)
            
            # Handle food stock
            if snake.get_food_stock() > 0:
                snake.add_food_stock(-1)  # Use food stock to grow
            else:
                snake.pop_segment()  # Remove last segment if not growing

        # Handle screen edge wrapping
        width, height = self.__screen_size
        head_x, head_y = snake.get_head_position()
        if head_x < 0:
            snake.set_head_positions([width - self.__block_size, head_y])
        elif head_x >= width:
            snake.set_head_positions([0, head_y])
        if head_y < 0:
            snake.set_head_positions([head_x, height - self.__block_size])
        elif head_y >= height:
            snake.set_head_positions([head_x, 0])

        # Check for collisions with other snakes and itself
        occupied_positions = []
        for s in self.__snakes.values():
            if s != snake:
                occupied_positions.extend(s.get_body_segments())
            else:
                # Exclude the head to prevent self-collision detection on head position
                occupied_positions.extend(s.get_body_segments()[1:])  # Exclude head

        if snake.get_head_position() in occupied_positions:
            snake.kill()
            print(f"{snake.get_name()} collided with another snake or its own body and is killed.")
            
    def update(self, events):
        # Check how many snakes are alive
        alive_snakes = [snake for snake in self.__snakes.values() if snake.is_alive()]
        if len(alive_snakes) <= 1:
            # Game over if one or zero snakes are alive
            self.__is_game_over = True
            if len(alive_snakes) == 1:
                winner = alive_snakes[0].get_name()
                print(f"{winner} wins the game!")
        else:
            self.__is_game_over = False

            for snake in alive_snakes:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == snake.get_key_map()['UP']:
                            snake.set_direction('UP')
                        elif event.key == snake.get_key_map()['DOWN']:
                            snake.set_direction('DOWN')
                        elif event.key == snake.get_key_map()['LEFT']:
                            snake.set_direction('LEFT')
                        elif event.key == snake.get_key_map()['RIGHT']:
                            snake.set_direction('RIGHT')
                self.update_snake(snake)
        
        self.__frame_counter += 1

    def get_random_position(self):
        width = self.__screen_size[0]
        height = self.__screen_size[1]
        block_size = self.__block_size
        return [np_random.randint(0, (width // block_size)) * block_size,
                np_random.randint(0, (height // block_size)) * block_size]
