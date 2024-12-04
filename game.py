from powerup_debuff import PowerUpOrDebuff
from typing import List, Dict
import numpy.random as np_random
from snake import Snake
import pygame
import numpy as np
from map import Map
from map import Room


class Game:

    def __init__(self, screen_size, block_size, min_foods=10, fps=60):
        self.__block_size = block_size  # block size in pixels
        self.__screen_size = screen_size  # (width, height)

        self.__map : Map = Map(width=screen_size[0] // block_size, height=screen_size[1] // block_size, block_size=block_size)
        self.__init_map()

        self.__foods: List[PowerUpOrDebuff] = [] 
        self.__min_foods: int = min_foods
        
        self.__snakes: Dict[str, Snake] = {}

        self.__is_game_over = False
        self.__fps = fps

        self.__frame_counter = 0
        Snake.__block_size = block_size
    
    def __init_map(self):
        width, height = self.__screen_size

        room1 = Room(width // self.get_block_size() //2, height // self.get_block_size() //2)

        map_pos_x = ((self.__screen_size[0] // self.get_block_size() - room1.get_width()) //2) * self.get_block_size()
        map_pos_y = ((self.__screen_size[1] // self.get_block_size() - room1.get_height()) //2) * self.get_block_size()
        

        room1.add_door("right", (room1.height // 2 - room1.height // 4, room1.height // 2 + room1.height // 4))
        room1.add_door("left", (room1.height // 2 - room1.height // 4, room1.height // 2 + room1.height // 4))
        room1.add_door("bottom", (room1.width // 2 - room1.width // 4, room1.width // 2 + room1.width // 4))
        room1.add_door("top", (room1.width // 2 - room1.width // 4, room1.width // 2 + room1.width // 4))
        
        self.__map.add_room(room1, (map_pos_x, map_pos_y))       


        room2 = Room(width // self.get_block_size() //4, height // self.get_block_size() //4)
        map_pos_x2 = map_pos_x - (room2.get_width()//2) * self.get_block_size() 
        map_pos_y2 = map_pos_y - (room2.get_height()//2) * self.get_block_size()
        room2.add_door("right", (room2.height //2  , room2.height))
        room2.add_door("bottom", (room2.width // 2  , room2.width))
        self.__map.add_room(room2 , (map_pos_x2, map_pos_y2))


        room3 = Room(width // self.get_block_size() //4, height // self.get_block_size() //4)
        map_pos_x3 = map_pos_x + room1.width * self.get_block_size() - (room3.get_width()//2) * self.get_block_size() 
        map_pos_y3 = map_pos_y + room1.height * self.get_block_size() - (room3.get_height()//2) * self.get_block_size()
        room3.add_door("left", (0, room3.height //2))
        room3.add_door("top", (0, room3.width // 2))
        self.__map.add_room(room3 , (map_pos_x3, map_pos_y3))

        room4 = Room(width // self.get_block_size() //4, height // self.get_block_size() //4)
        map_pos_x4 = map_pos_x + room1.width * self.get_block_size() - (room4.get_width()//2) * self.get_block_size() 
        map_pos_y4 = map_pos_y - (room4.get_height()//2) * self.get_block_size()
        room4.add_door("left", (room4.height //2, room4.height))
        room4.add_door("bottom", (0, room4.width // 2))
        self.__map.add_room(room4 , (map_pos_x4, map_pos_y4))

        room5 = Room(width // self.get_block_size() //4, height // self.get_block_size() //4)
        map_pos_x5 = map_pos_x - (room5.get_width()//2) * self.get_block_size()
        map_pos_y5 = map_pos_y + room1.height * self.get_block_size() - (room3.get_height()//2) * self.get_block_size()
        room5.add_door("right", (0, room5.height //2))
        room5.add_door("top", (room5.width // 2, room5.width))
        self.__map.add_room(room5 , (map_pos_x5, map_pos_y5))

        

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
    def get_map(self):
        return self.__map
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

        # Handle armor expiration
        if snake.is_armor_active() and current_time > snake.get_armor_end_time():
            snake.remove_armor()  # End armor after the duration expires
            print(f"{snake.get_name()}'s armor has expired.")

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
            distance_from_food = np.linalg.norm(np.array(food.get_position()) - np.array(snake.get_head_position()))
            if distance_from_food < self.__block_size / 2:
                food.apply_effect(snake, self)  # Pass both snake and game
                self.__foods.pop(i)
                print(f"{snake.get_name()} consumed a {food.item_type} at {food.position}.")
                break  # Only one food can be consumed at a time

        # Add food if below minimum
        if self.__min_foods > len(self.__foods):
            new_food = PowerUpOrDebuff.spawn()
            # Prevent spawning on snakes or existing foods
            while new_food.get_position() in [segment for s in self.__snakes.values() for segment in s.get_body_segments()] or new_food.get_position() in [food.get_position() for food in self.__foods]:
                new_food = PowerUpOrDebuff.spawn()
            self.__foods.append(new_food)
            print(f"Spawned new {new_food.item_type} at {new_food.position}.")

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

        # **Self-Collision Check**
        body_segments = snake.get_body_segments()[1:]  # Exclude head
        head_position = snake.get_head_position()
        if head_position in body_segments:
            snake.kill()
            print(f"{snake.get_name()} collided with itself and is killed.")
            return  # Early exit since the snake is dead

        # Check for collisions with other snakes and their armor blocks
        occupied_positions = []
        armor_positions = []
        for s in self.__snakes.values():
            if s != snake and s.is_alive():
                occupied_positions.extend(s.get_body_segments())
                armor_blocks = s.get_armor_positions()
                armor_positions.extend(armor_blocks)

        if head_position in occupied_positions or head_position in armor_positions:
            snake.kill()
        
        # Increment frame counter
        self.__frame_counter += 1

        #wall collision
        x_head = snake.get_head_position()[0] // self.get_block_size()
        y_head = snake.get_head_position()[1] // self.get_block_size()
        if self.__map.pixels[y_head, x_head] == 1:
            snake.kill()
            print(f"{snake.get_name()} collided with a wall and is killed.")
        elif self.__map.pixels[y_head, x_head] != 0:
            room = self.__map.get_room(self.__map.pixels[y_head, x_head])
            room.isoccupied = True
            
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

    def add_food_to_room(self, room_id):
        room = self.__map.get_room(room_id)
        if room.isoccupied:
            return
        food = PowerUpOrDebuff.spawn()
        x, y = room.pos
        rand_pos = room.get_random_position()
        x, y = x + rand_pos[0] * self.get_block_size(), y + rand_pos[1] * self.get_block_size()
        food.set_position((x // self.get_block_size() * self.get_block_size(), y// self.get_block_size() * self.get_block_size()))
        self.__foods.append(food)

    def add_food_randomly(self):
        pos = self.get_random_position()
        food = PowerUpOrDebuff.spawn()
        food.set_position(pos)
        self.__foods.append(food)