import pygame
from typing import List
from powerup_debuff import PowerUpOrDebuff

class Snake:
    __block_size = None

    def set_block_size(block_size):
        assert type(block_size) == int and block_size > 0
        Snake.__block_size = block_size

    def __init__(self, positions : List[List[int]]):
        assert Snake.__block_size != None, "use Snake.set_block_size(block_size)"

        self.__head_position : List[int] = positions[0].copy()

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

        self.__food_stock = 30
        self.__is_alive = True
        self.__is_frozen = False  # Initialize the frozen state to False
        self.__freeze_end_time = None  # Initialize the freeze end time to None
        self.__is_speed_boosted = False  # Make sure speed boost is initialized
        

    def __init_body_segments(self, positions):
        self.__body_segments : List[List[int]] = []
        for segment, segment2 in zip(positions[:-1], positions[1:]):
            assert (segment[0] % Snake.__block_size == 0 and 
                    segment2[0] % Snake.__block_size == 0), (
                        "Make sure the snake positions is divisible by block size") 

            self.__body_segments.append(segment)
            while True:
                seg = self.__body_segments[-1].copy()
                if seg[0] == segment2[0]:
                    break
                if seg[0] - segment2[0] < 0:
                    seg[0] += Snake.__block_size
                else:
                    seg[0] -= Snake.__block_size

                assert seg not in self.__body_segments
                self.__body_segments.append(seg)

            while True:
                seg = self.__body_segments[-1].copy()
                if seg[1] == segment2[1]:
                    break
                if seg[1] - segment2[1] < 0:
                    seg[1] += Snake.__block_size
                else:
                    seg[1] -= Snake.__block_size

                assert seg not in self.__body_segments
                self.__body_segments.append(seg)
        
        self.__body_segments.append(positions[-1])
    

    def set_head_positions(self, position : List[int]):
        self.__head_position = position
        self.__body_segments[0] = self.get_head_position()

    def set_direction(self, direction):
        if direction == 'UP' and self.__direction != 'DOWN':
            self.__direction = 'UP'
        elif direction == 'DOWN' and self.__direction != 'UP':
            self.__direction = 'DOWN'
        elif direction == 'LEFT' and self.__direction != 'RIGHT':
            self.__direction = 'LEFT'
        elif direction == 'RIGHT' and self.__direction != 'LEFT':
            self.__direction = 'RIGHT'

    def get_body_segments(self):
        return self.__body_segments.copy()
    
    def get_head_position(self):
        return self.__head_position.copy()

    def get_direction(self):
        return self.__direction
    
    def is_alive(self):
        return self.__is_alive
    
    def kill(self):
        self.__is_alive = False

    def eat(self, amount):
        self.__food_stock += amount
    
    def apply_freeze(self, duration: int):
        """Freeze the snake for a specified duration."""
        self.__is_frozen = True
        self.__freeze_end_time = pygame.time.get_ticks() + duration

    def remove_freeze(self):
        """Remove the freeze effect after the duration expires."""
        self.__is_frozen = False
        self.__freeze_end_time = None

    def apply_speed_boost(self, duration: int):
        """Apply a speed boost to the snake for a specified duration."""
        self.__is_speed_boosted = True
        self.__speed_boost_end_time = pygame.time.get_ticks() + duration

    def remove_speed_boost(self):
        """Remove the speed boost after the duration expires."""
        self.__is_speed_boosted = False
        self.__speed_boost_end_time = None

    def get_active_effects(self):
        active_effects = []
    
        if getattr(self, "__is_frozen", False):
            active_effects.append("freeze")
    
        if getattr(self, "__is_speed_boosted", False):
            active_effects.append("speed_boost")
    
        return active_effects


    def update(self):
        assert id(self.__head_position) != id(self.__body_segments[0])

        if self.__is_frozen and pygame.time.get_ticks() > self.__freeze_end_time:
            self.remove_freeze()  # Unfreeze after the duration ends
        
        if self.__is_frozen:
            return  # If frozen, don't update the snake's position

        if self.__is_speed_boosted and pygame.time.get_ticks() > self.__speed_boost_end_time:
            self.remove_speed_boost()  # End speed boost after the duration expires


        if self.__direction == 'UP':
            self.__head_position[1] -= Snake.__block_size
        if self.__direction == 'DOWN':
            self.__head_position[1] += Snake.__block_size
        if self.__direction == 'LEFT':
            self.__head_position[0] -= Snake.__block_size
        if self.__direction == 'RIGHT':
            self.__head_position[0] += Snake.__block_size

        # Insert the new head position at the front
        self.__body_segments.insert(0, self.get_head_position())
        
        # If the snake eats food, increase the food stock and add a body segment
        if self.__food_stock:
            self.__food_stock -= 1
        else: 
            # Remove the last body segment if no food is eaten (tail moves)
            self.__body_segments.pop()
        
        if self.__head_position in self.__body_segments[1:]:
            self.kill()

    def add_body_segment(self):
        """Add a new segment to the snake's body."""
        # Append a new body segment at the position of the last segment
        self.__body_segments.append(self.__body_segments[-1].copy())

def main():
    x = [1,2,3]
    y = [2,3]
    x.append(y)
    y[0] += 1
    print(x, y)

if __name__ == "__main__":
    main()