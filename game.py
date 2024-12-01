from powerup_debuff import PowerUpOrDebuff
from typing import List
import numpy.random as np_random
from snake import Snake
import pygame
import numpy as np

class Game:

    def __init__(self, screen_size, block_size, min_foods = 4):
        self.__block_size = block_size # block size in pixels
        self.__screen_size = screen_size #(width, height)

        self.__foods : List[PowerUpOrDebuff]= [] 
        self.__min_foods : int = 4
        
        self.__snakes = {}

        self.__is_game_over = False

        Snake.__block_size = block_size
    
    # Setters
    def set_block_size(self, block_size):
        self.__block_size = block_size
    
    def set_screen_size(self, width, height):
        self.__screen_size = (width, height)
    
    def add_food(self, food : PowerUpOrDebuff):
        self.__foods.append(food)
    
    def set_min_foods(self, min_foods):
        self.__min_foods = min_foods

    def add_snake(self, snake : Snake):
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
        return {name : snake.get_score() for name, snake in self.__snakes.items()}

    def is_game_over(self):
        return self.__is_game_over

    def update_snake(self, snake : Snake):
        if snake.is_frozen() and pygame.time.get_ticks() > snake.get_freeze_end_time():
            snake.remove_freeze()  # Unfreeze after the duration ends
        
        if snake.is_frozen():
            return  # If frozen, don't update the snake's position

        if snake.is_speed_boosted() and pygame.time.get_ticks() > snake.get_speed_boost_end_time():
            snake.remove_speed_boost()  # End speed boost after the duration expires


        if snake.get_direction() == 'UP':
            snake.offset_head_position(offset_y=-self.__block_size)
        if snake.get_direction() == 'DOWN':
            snake.offset_head_position(offset_y= self.__block_size)
        if snake.get_direction() == 'LEFT':
            snake.offset_head_position(offset_x=-self.__block_size)
        if snake.get_direction() == 'RIGHT':
            snake.offset_head_position(offset_x= self.__block_size)

        #Eat food
        for i, food in enumerate(self.__foods):
            if food.get_position() == snake.get_head_position():
                food.apply_effect(snake)
                self.__foods.pop(i)
        
        #Add food
        if self.__min_foods > len(self.__foods):
            item_type = np_random.choice(PowerUpOrDebuff.get_item_type_list(), p = [0.25, 0.25, 0.5])
            self.__foods.append(PowerUpOrDebuff(item_type, 2, self.get_random_position()))
        #Movement (adding new segment)
        snake.insert_segment(snake.get_head_position(), 0)
        
        #if food stock available
        if snake.get_food_stock() > 0:
            #Not remove last segment
            snake.add_food_stock(-1)
        else: 
            # Remove the last body segment
            snake.pop_segment()
        

        #Edge of screen handling
        width = self.__screen_size[0]
        height = self.__screen_size[1]
        if snake.get_head_position()[0] < 0:
            snake.set_head_positions([width - self.__block_size, snake.get_head_position()[1]])
        elif snake.get_head_position()[0] >= width:
            snake.set_head_positions([0, snake.get_head_position()[1]])
        elif snake.get_head_position()[1] < 0:
            snake.set_head_positions([snake.get_head_position()[0], height - self.__block_size])
        elif snake.get_head_position()[1] >= height:
            snake.set_head_positions([snake.get_head_position()[0], 0])
        

        #Gameover
        occupied_positions = []
        for s in self.__snakes.values():
            if s != snake:
                occupied_positions.extend(s.get_body_segments())
            else:
                occupied_positions.extend(s.get_body_segments()[1:])
        if snake.get_head_position() in occupied_positions:
            snake.kill()

    def update(self, events):
        self.__is_game_over = True
        for snake in self.__snakes.copy().values():
            if not snake.is_alive():
                continue

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
            self.__is_game_over = False
    



    def get_random_position(self):
        width = self.__screen_size[0]
        height = self.__screen_size[1]
        block_size = self.__block_size
        return [np_random.randint(1, (width // block_size)) * block_size,
            np_random.randint(1, (height // block_size)) * block_size]

