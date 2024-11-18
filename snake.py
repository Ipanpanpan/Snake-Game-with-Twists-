from typing import List

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

    def update(self):
        assert id(self.__head_position) != id(self.__body_segments[0])

        if self.__direction == 'UP':
            self.__head_position[1] -= Snake.__block_size
        if self.__direction == 'DOWN':
            self.__head_position[1] += Snake.__block_size
        if self.__direction == 'LEFT':
            self.__head_position[0] -= Snake.__block_size
        if self.__direction == 'RIGHT':
            self.__head_position[0] += Snake.__block_size
        
        self.__body_segments.insert(0, self.get_head_position())
        
        if self.__food_stock:
            self.__food_stock -= 1
        else: 
            self.__body_segments.pop()
        
        if self.__head_position in self.__body_segments[1:]:
            self.kill()


def main():
    x = [1,2,3]
    y = [2,3]
    x.append(y)
    y[0] += 1
    print(x, y)

if __name__ == "__main__":
    main()