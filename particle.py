import pygame
import random

class Particle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        self.radius =  float(random.randint(5, 10))
        self.color = (255, 255, 255)