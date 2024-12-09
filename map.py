import numpy as np
from typing import Tuple
import pygame
import sys
import random

class Map:
    id_type_map = {0 : "air", 1 : "wall"}
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.pixels = np.full((height, width), fill_value= 0)
        self.block_size = block_size
        self.rooms = {}

    def draw_hollow_rect(self,value,  left_top : Tuple[int, int], right_bot : Tuple[int, int]):
        """draw a hollow rectangle on the map"""
        self.pixels[left_top[1], left_top[0] : right_bot[0]] = value
        self.pixels[right_bot[1] - 1, left_top[0] : right_bot[0]] = value
        self.pixels[left_top[1] : right_bot[1], left_top[0]] = value
        self.pixels[left_top[1] : right_bot[1], right_bot[0] - 1] = value

    def draw_filled_rect(self, value, left_top : Tuple[int, int], right_bot : Tuple[int, int]):
        """draw a filled rectangle on the map"""
        self.pixels[left_top[1] : right_bot[1], left_top[0] : right_bot[0]] = value

    def add_room(self, room : "Room", left_top_pos : Tuple[int, int]):
        """draw a room on the map"""
        room.pos = left_top_pos
        self.rooms[room.get_id()] = room
        coor_left_top = (left_top_pos[0] // self.block_size, left_top_pos[1] // self.block_size)
        coor_right_bot = (left_top_pos[0] //self.block_size + room.get_width(), left_top_pos[1]// self.block_size + room.get_height())
        self.draw_hollow_rect(1, coor_left_top, coor_right_bot)
        self.draw_filled_rect(room.get_id(), (coor_left_top[0] + 1, coor_left_top[1] + 1), (coor_right_bot[0] - 1, coor_right_bot[1] - 1))
        for side, interval in room.doors.items():
            if side == "left":
                self.pixels[coor_left_top[1] + interval[0] : coor_left_top[1] + interval[1], coor_left_top[0]] = 0
            elif side =="right":
                self.pixels[coor_left_top[1] + interval[0] : coor_left_top[1] + interval[1], coor_right_bot[0] - 1] = 0
            elif side == "top":
                self.pixels[coor_left_top[1] : coor_left_top[1] + 1, coor_left_top[0] + interval[0] :coor_left_top[0] +  interval[1]] = 0
            elif side == "bottom":
                self.pixels[coor_right_bot[1] - 1, coor_left_top[0] + interval[0] :coor_left_top[0] +  interval[1]] = 0
    # Getters
    def get_room(self, room_id):
        """get a room by id"""
        return self.rooms[room_id]
    def get_width(self):
        return self.width  
    def get_height(self):
        return self.height
    def get_pixels(self):    
        return self.pixels
        
class Room:
    id_iter = 2
    def __init__(self, width = 10, height = 10):
        self.id = Room.id_iter
        Room.id_iter += 1
        self.width = width
        self.height = height
        self.pos = (0, 0)
        self.doors = {}
        self.isoccupied = False
    # Getters
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_id(self):
        return self.id
    
    def is_occupied(self):
        return self.isoccupied
    
    def add_door(self, side, interval : Tuple[int, int]):
        """add a door on the room"""
        self.doors[side] = interval
    def get_random_position(self):
        """get a random position in room"""
        return random.randint(0, self.width - 1), random.randint(0, self.height - 1)


class Pixel:
    # id_type_map = {"air" : 0}
    # type_id_map = {item[1] : item[0] for item in id_type_map.items()}
    
    def __init__(self, type = "air"):
        self.type = type
        
        if type == "air":
            self.color = (0, 0, 0)
        elif type == "wall":
            self.color = (50, 50, 50)
        elif type == "ceiling":
            self.color = (100, 100, 100)
        else:
            raise ValueError("Invalid pixel type")
    def get_color(self):
        return self.color
