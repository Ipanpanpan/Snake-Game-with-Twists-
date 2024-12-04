import random 
from typing import List

class PowerUpOrDebuff:
    def __init__(self, item_type: str, duration: int, position: List[int]):
        """
        Initialize a power-up or debuff.
        
        :param item_type: Type of the power-up or debuff (e.g., 'speed_boost', 'slow_down', 'invincibility', 'normal', 'armor')
        :param duration: Duration of the effect in milliseconds (0 for permanent effects like 'normal' and 'armor')
        :param position: Position on the screen where the item appears
        """
        self.item_type = item_type  # Can be "speed_boost", "slow_down", "invincibility", "normal", "armor", etc.
        self.duration = duration  # Duration in milliseconds
        self.position = position  # Position on the screen

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position
        
    def apply_effect(self, snake, game):
        """Apply the effect to the snake."""
        print(f"Applying {self.item_type} to {snake.get_name()} for {self.duration} ms")  # Debug
        if self.item_type == "speed_boost":
            snake.apply_speed_boost(self.duration)
        elif self.item_type == "slow_down":
            snake.apply_slow_down(self.duration)
        elif self.item_type == "invincibility":
            snake.apply_invincibility(self.duration)
        elif self.item_type == "score_decrease":
            snake.score_debuff(60)
        elif self.item_type == "armor":
            snake.apply_armor(self.duration)  # Activate armor with duration

        elif self.item_type == "food_party":
            fruits_spawned = 0
            max_attempts = 100  # Maximum number of attempts to find a valid position
            attempts = 0
            while fruits_spawned < 10 and attempts < max_attempts:
                attempts += 1
                current_position = self.get_position()
                new_x = random.randint(-5, 5) * game.get_block_size()
                new_y = random.randint(-5, 5) * game.get_block_size()
        
                # Calculate new positions ensuring they are within screen bounds
                new_x_pos = max(0, min(current_position[0] + new_x, game.get_screen_size()[0] - game.get_block_size()))
                new_y_pos = max(0, min(current_position[1] + new_y, game.get_screen_size()[1] - game.get_block_size()))
        
                normal_food = PowerUpOrDebuff("normal", 0, [new_x_pos, new_y_pos])

                # Check for overlaps
                if (normal_food.get_position() not in [segment for s in game.get_snakes().values() for segment in s.get_body_segments()]) and \
                    (normal_food.get_position() not in [food.get_position() for food in game.get_available_foods()]):
                    game.add_food(normal_food)
                    fruits_spawned += 1
        
        elif self.item_type == "normal":
            snake.add_score(10)
            snake.add_body_segment()
            print(f"{snake.get_name()} consumed a normal fruit. Score increased by 10 and snake length extended.")
        snake.eat(1)

    @staticmethod
    def spawn():
        """Spawn a random power-up or debuff."""
        # Define probabilities for each item type
        # Adjust probabilities as desired
        item_types = ["normal", "speed_boost", "slow_down", "invincibility", "score_decrease", "food_party", "armor"]
        probabilities = [0.5, 1/6, 1/6, 1/6, 1/6, 1/6, 1/6] 

        # Randomly choose an item type based on defined probabilities
        item_type = random.choices(item_types, weights=probabilities, k=1)[0]
    
        # Adjust duration based on the item type
        if item_type == "speed_boost":
            duration = random.randint(5000, 10000)  # 5 to 10 seconds
        elif item_type == "slow_down":
            duration = 2000  # 2 seconds
        elif item_type == "invincibility":
            duration = 5000  # 5 seconds
        elif item_type == "score_decrease":
            duration = random.randint(3000, 5000)  # 3 to 5 seconds
        elif item_type == "armor":
            duration = 5000  # 5 seconds
        elif item_type == "normal":
            duration = 0  # No duration needed for normal fruit
        elif item_type == "food_party":
            duration = 0  # No duration needed for food_party
    
        # Random position on the grid based on screen size (Assuming 1280x720 and block_size=10)
        position = [random.randint(0, 127) * 10, random.randint(0, 71) * 10]  # Adjust based on actual screen size
    
        return PowerUpOrDebuff(item_type, duration, position)

    @staticmethod
    def get_item_type_list():
        return ["speed_boost", "slow_down", "invincibility", "score_decrease", "food_party", "normal", "armor"]
