import random
from typing import List

class PowerUpOrDebuff:
    def __init__(self, item_type: str, duration: int, position: List[int]):
        """
        Initialize a power-up or debuff.
        
        :param item_type: Type of the power-up or debuff (e.g., 'speed_boost', 'freeze')
        :param duration: Duration of the effect in milliseconds
        :param position: Position on the screen where the item appears
        """
        self.item_type = item_type  # Can be "speed_boost", "freeze", etc.
        self.duration = duration  # Duration in milliseconds
        self.position = position  # Position on the screen

    def get_position(self):
        return self.position

    def apply_effect(self, snake):
        """Apply the effect to the snake."""
        if self.item_type == "speed_boost":
            snake.apply_speed_boost(self.duration)
        elif self.item_type == "freeze":
            snake.apply_freeze(self.duration)
        elif self.item_type == "score_decrease":
            snake.score_debuff(60)
        snake.eat(1)
        snake.add_score(10)

        
        # You can add more effects here (e.g., size change, temporary invincibility, etc.)

    @staticmethod
    def spawn():
        """Spawn a random power-up or debuff."""
        # We'll ensure that the "blue fruit" (or freeze item) is always a "freeze" debuff
        item_type = random.choice(["speed_boost", "freeze","score_decrease"])  # Randomly decide between speed_boost and freeze
        if item_type == "freeze":
            item_type = "freeze"  # Ensure blue fruit is always freeze debuff
        elif item_type == "score_decrease":
            item_type = "score_decrease"

        # Adjust duration based on the item type
        if item_type == "speed_boost":
            duration = random.randint(5000, 10000)  # Duration in milliseconds for speed_boost
        else:
            duration = random.randint(3000, 5000)  # Duration in milliseconds for freeze debuff

        # Random position on the grid (assuming 10x10 grid and 600x400 screen)
        position = [random.randint(0, 59) * 10, random.randint(0, 39) * 10]  
        return PowerUpOrDebuff(item_type, duration, position)

    @staticmethod
    def get_item_type_list():
        return ["speed boost", "freeze", "normal","score_decrease"]