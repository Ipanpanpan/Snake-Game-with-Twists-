import random 
from typing import List

class PowerUpOrDebuff:
    def __init__(self, item_type: str, duration: int, position: List[int]):
        """
        Initialize a power-up or debuff.
        
        :param item_type: Type of the power-up or debuff (e.g., 'speed_boost', 'slow_down', 'invincibility', 'normal')
        :param duration: Duration of the effect in milliseconds (0 for permanent effects like 'normal')
        :param position: Position on the screen where the item appears
        """
        self.item_type = item_type  # Can be "speed_boost", "slow_down", "invincibility", "normal", etc.
        self.duration = duration  # Duration in milliseconds
        self.position = position  # Position on the screen

    def get_position(self):
        return self.position

    def apply_effect(self, snake):
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
        item_types = ["speed_boost", "slow_down", "invincibility", "score_decrease", "normal"]
        probabilities = [0.15, 0.15, 0.10, 0.10, 0.50]  # Example probabilities: 50% normal fruit

        # Randomly choose an item type based on defined probabilities
        item_type = random.choices(item_types, weights=probabilities, k=1)[0]
    
        # Adjust duration based on the item type
        if item_type == "speed_boost":
            duration = random.randint(5000, 10000)  # 5 to 10 seconds
        elif item_type == "slow_down":
            duration = 2000  # 2 seconds
        elif item_type == "invincibility":
            duration = 2000  # 2 seconds
        elif item_type == "score_decrease":
            duration = random.randint(3000, 5000)  # 3 to 5 seconds
        elif item_type == "normal":
            duration = 0  # No duration needed for normal fruit
    
        # Random position on the grid based on screen size (Assuming 1280x720 and block_size=10)
        position = [random.randint(0, 127) * 10, random.randint(0, 71) * 10]  # Adjust based on actual screen size
    
        return PowerUpOrDebuff(item_type, duration, position)

    @staticmethod
    def get_item_type_list():
        return ["speed_boost", "slow_down", "invincibility", "score_decrease", "normal"]
