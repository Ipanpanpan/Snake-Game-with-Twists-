import pygame
from typing import List, Tuple
from powerup_debuff import PowerUpOrDebuff
from numpy import random as np_random
import random

class Snake:
    __block_size = 10

    def __init__(self, positions: List[List[int]], name: str, color=(0, 255, 0), key_map=None, update_rate=15):

        self.__head_position: List[int] = positions[0].copy()

        self.__body_segments = None
        self.__init_body_segments(positions)
        
        self.__direction = None
        try:
            seg1, seg2 = self.__body_segments[0], self.__body_segments[1]
            
            if seg1[0] < seg2[0]:
                self.__direction = "LEFT"
            elif seg1[0] > seg2[0]:
                self.__direction = "RIGHT"
            elif seg1[1] < seg2[1]:
                self.__direction = "UP"
            elif seg1[1] > seg2[1]:
                self.__direction = "DOWN"
        except:
            self.__direction = "RIGHT"


        # Internal Condition
        self.__food_stock = 0
        self.__is_alive = True
        self.__is_speed_boosted = False  # Ensure speed boost is initialized
        self.__speed_boost_end_time = None  # Initialize the speed boost end time to None
        self.__is_slowed_down = False  # Initialize the slow down state to False
        self.__slow_down_end_time = None  # Initialize the slow down end time to None
        self.__is_invincible = False  # Initialize the invincibility state to False
        self.__invincibility_end_time = None  # Initialize the invincibility end time to None
        self.__invincibility_start_time = None  # Initialize invincibility start time to None
        self.__is_armor_active = False  # Initialize armor state
        self.__armor_end_time = None  # Initialize armor end time
        self.__score = 0
        self.__name = name
        self.__update_rate = update_rate

        # Cosmetic
        self.__color = color
        if key_map is None:
            self.__key_map = {"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, 
                                "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT}
        else:
            self.__key_map = key_map

    def __init_body_segments(self, positions):
        self.__body_segments: List[List[int]] = []
        for segment, segment2 in zip(positions[:-1], positions[1:]):
            
            self.__body_segments.append(segment)
            while True:
                seg = self.__body_segments[-1].copy()
                if seg[0] == segment2[0]:
                    break
                if seg[0] - segment2[0] < 0:
                    seg[0] += Snake.__block_size
                else:
                    seg[0] -= Snake.__block_size

                assert seg not in self.__body_segments, "Overlapping segments detected during initialization."
                self.__body_segments.append(seg)

            while True:
                seg = self.__body_segments[-1].copy()
                if seg[1] == segment2[1]:
                    break
                if seg[1] - segment2[1] < 0:
                    seg[1] += Snake.__block_size
                else:
                    seg[1] -= Snake.__block_size

                assert seg not in self.__body_segments, "Overlapping segments detected during initialization."
                self.__body_segments.append(seg)
        
        self.__body_segments.append(positions[-1])

    # Setters

    def set_head_positions(self, position: List[int]):
        self.__head_position = position
        self.__body_segments[0] = self.get_head_position()

    def set_direction(self, direction):
        if direction == 'UP' and self.__direction != 'DOWN'  and not (self.__head_position[1] > self.__body_segments[1][1] and abs(self.__head_position[0] - self.__body_segments[1][0]) < Snake.__block_size/2):
            self.__direction = 'UP'
        elif direction == 'DOWN' and self.__direction != 'UP' and not (self.__head_position[1] < self.__body_segments[1][1] and abs(self.__head_position[0] - self.__body_segments[1][0]) < Snake.__block_size/2):
            self.__direction = 'DOWN'
        elif direction == 'LEFT' and self.__direction != 'RIGHT' and not (self.__head_position[0] > self.__body_segments[1][0] and abs(self.__head_position[1] - self.__body_segments[1][1]) < Snake.__block_size/2):
            self.__direction = 'LEFT'
        elif direction == 'RIGHT' and self.__direction != 'LEFT'and not (self.__head_position[0] < self.__body_segments[1][0] and abs(self.__head_position[1] - self.__body_segments[1][1]) < Snake.__block_size/2):
            self.__direction = 'RIGHT'

    def set_color(self, color: Tuple):
        assert isinstance(color, tuple) and len(color) == 3, "Invalid color"
        self.__color = color 
    
    def set_score(self, score: int):
        self.__score = score
    
    def set_update_rate(self, rate: int):
        self.__update_rate = rate

    def add_score(self, score: int):
        self.__score += score

    def add_body_segment(self):
        """Add a new segment to the snake's body."""
        # Append a new body segment at the position of the last segment
        last_segment = self.__body_segments[-1].copy()
        self.__body_segments.append(last_segment)

    def offset_head_position(self, offset_x=0, offset_y=0):
        self.__head_position[0] += offset_x
        self.__head_position[1] += offset_y

    def insert_segment(self, position, index=0):
        self.__body_segments.insert(index, position)

    def add_food_stock(self, amount):
        self.__food_stock += amount

    def pop_segment(self, index=-1):
        return self.__body_segments.pop(index)

    # Getters
    def get_body_segments(self):
        return self.__body_segments.copy()
    
    def get_head_position(self):
        return self.__head_position.copy()

    def get_direction(self):
        return self.__direction
    
    def get_color(self):
        return self.__color
    
    def get_score(self):
        return self.__score

    def get_active_effects(self):
        active_effects = []
    
        if getattr(self, "__is_speed_boosted", False):
            active_effects.append("speed_boost")
    
        if getattr(self, "__is_slowed_down", False):
            active_effects.append("slow_down")
        
        if getattr(self, "__is_invincible", False):
            active_effects.append("invincibility")
        
        if getattr(self, "__is_armor_active", False):
            active_effects.append("armor")
    
        return active_effects

    def get_name(self):
        return self.__name

    def get_update_rate(self):
        return self.__update_rate

    def is_alive(self):
        return self.__is_alive
    
    def is_speed_boosted(self):
        return self.__is_speed_boosted
    
    def is_slowed_down(self):
        return self.__is_slowed_down
    
    def is_invincible(self):
        return self.__is_invincible
    
    def is_armor_active(self):
        return self.__is_armor_active
    
    def get_speed_boost_end_time(self):
        return self.__speed_boost_end_time
    
    def get_slow_down_end_time(self):
        return self.__slow_down_end_time
    
    def get_invincibility_end_time(self):
        return self.__invincibility_end_time
    
    def get_armor_end_time(self):
        return self.__armor_end_time

    def get_invincibility_start_time(self):
        return self.__invincibility_start_time
    
    def get_food_stock(self):
        return self.__food_stock
    
    def get_key_map(self):
        return self.__key_map.copy()
    # Methods

    def kill(self):
        self.__is_alive = False
        print(f"{self.__name} has been killed.")

    def eat(self, amount):
        self.__food_stock += amount
    
    def apply_speed_boost(self, duration: int):
        """Apply a speed boost to the snake for a specified duration."""
        self.__is_speed_boosted = True
        self.__speed_boost_end_time = pygame.time.get_ticks() + duration
        print(f"{self.__name} received a speed boost for {duration} ms.")

    def remove_speed_boost(self):
        """Remove the speed boost after the duration expires."""
        self.__is_speed_boosted = False
        self.__speed_boost_end_time = None
        print(f"{self.__name}'s speed boost has ended.")

    def apply_slow_down(self, duration: int):
        """Apply a slow down effect to the snake for a specified duration."""
        self.__is_slowed_down = True
        self.__slow_down_end_time = pygame.time.get_ticks() + duration
        print(f"{self.__name} has been slowed down for {duration} ms.")

    def remove_slow_down(self):
        """Remove the slow down effect after the duration expires."""
        self.__is_slowed_down = False
        self.__slow_down_end_time = None
        print(f"{self.__name} has recovered from slow down.")

    def apply_invincibility(self, duration: int):
        """Apply invincibility to the snake for a specified duration."""
        self.__is_invincible = True
        self.__invincibility_end_time = pygame.time.get_ticks() + duration
        self.__invincibility_start_time = pygame.time.get_ticks()  # Store start time
        self.__original_color = self.__color  # Store original color to revert back later
        self.__color = (0, 0, 0)  # Change color to black
        print(f"{self.__name} is now invincible for {duration} ms.")

    def remove_invincibility(self):
        """Remove invincibility after the duration expires."""
        self.__is_invincible = False
        self.__invincibility_end_time = None
        self.__invincibility_start_time = None  # Reset start time
        self.__color = self.__original_color  # Revert to original color
        print(f"{self.__name} is no longer invincible.")

    def apply_armor(self, duration: int):
        """Activate armor for the snake for a specified duration."""
        self.__is_armor_active = True
        self.__armor_end_time = pygame.time.get_ticks() + duration
        print(f"{self.__name} has activated armor for {duration} ms.")

    def remove_armor(self):
        """Deactivate armor after the duration expires."""
        self.__is_armor_active = False
        self.__armor_end_time = None
        print(f"{self.__name} has deactivated armor.")

    def get_armor_positions(self):
        """Calculate and return all armor block positions based on the snake's body directions."""
        if not self.__is_armor_active:
            return []
        armor_positions = []
        body_segments = self.get_body_segments()
        num_segments = len(body_segments)
        for i in range(num_segments - 1):
            current = body_segments[i]
            next_seg = body_segments[i + 1]
            dx = next_seg[0] - current[0]
            dy = next_seg[1] - current[1]
            if dx > 0:
                direction = 'RIGHT'
            elif dx < 0:
                direction = 'LEFT'
            elif dy > 0:
                direction = 'DOWN'
            elif dy < 0:
                direction = 'UP'
            else:
                direction = 'NONE'
            
            if direction == 'UP':
                left_armor = [current[0] - self.__block_size, current[1]]
                right_armor = [current[0] + self.__block_size, current[1]]
            elif direction == 'DOWN':
                left_armor = [current[0] + self.__block_size, current[1]]
                right_armor = [current[0] - self.__block_size, current[1]]
            elif direction == 'LEFT':
                left_armor = [current[0], current[1] + self.__block_size]
                right_armor = [current[0], current[1] - self.__block_size]
            elif direction == 'RIGHT':
                left_armor = [current[0], current[1] - self.__block_size]
                right_armor = [current[0], current[1] + self.__block_size]
            else:
                # Default positions if direction is undefined
                left_armor = [current[0] - self.__block_size, current[1]]
                right_armor = [current[0] + self.__block_size, current[1]]

            # Ensure armor blocks are within screen bounds
            # Assuming screen size is 1280x720; adjust if different
            if 0 <= left_armor[0] < 1280 and 0 <= left_armor[1] < 720:
                armor_positions.append(left_armor)
            if 0 <= right_armor[0] < 1280 and 0 <= right_armor[1] < 720:
                armor_positions.append(right_armor)
        
        # Handle last segment (tail) direction same as previous
        if num_segments >= 2:
            last_seg = body_segments[-1]
            second_last_seg = body_segments[-2]
            dx = second_last_seg[0] - last_seg[0]
            dy = second_last_seg[1] - last_seg[1]
            if dx > 0:
                direction = 'RIGHT'
            elif dx < 0:
                direction = 'LEFT'
            elif dy > 0:
                direction = 'DOWN'
            elif dy < 0:
                direction = 'UP'
            else:
                direction = 'NONE'
            
            if direction == 'UP':
                left_armor = [last_seg[0] - self.__block_size, last_seg[1]]
                right_armor = [last_seg[0] + self.__block_size, last_seg[1]]
            elif direction == 'DOWN':
                left_armor = [last_seg[0] + self.__block_size, last_seg[1]]
                right_armor = [last_seg[0] - self.__block_size, last_seg[1]]
            elif direction == 'LEFT':
                left_armor = [last_seg[0], last_seg[1] + self.__block_size]
                right_armor = [last_seg[0], last_seg[1] - self.__block_size]
            elif direction == 'RIGHT':
                left_armor = [last_seg[0], last_seg[1] - self.__block_size]
                right_armor = [last_seg[0], last_seg[1] + self.__block_size]
            else:
                left_armor = [last_seg[0] - self.__block_size, last_seg[1]]
                right_armor = [last_seg[0] + self.__block_size, last_seg[1]]

            if 0 <= left_armor[0] < 1280 and 0 <= left_armor[1] < 720:
                armor_positions.append(left_armor)
            if 0 <= right_armor[0] < 1280 and 0 <= right_armor[1] < 720:
                armor_positions.append(right_armor)

        # Remove duplicate armor positions
        armor_positions = [list(x) for x in set(tuple(x) for x in armor_positions)]
        
        print(f"{self.get_name()} Armor Positions: {armor_positions}")  # Debugging statement
        return armor_positions

    def score_debuff(self, score: int):
        self.__score -= score        

    def __eq__(self, other):
        if not isinstance(other, Snake):
            return False
        return self.__name == other.get_name()
