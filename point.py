from random import randrange
from pygame import Vector2

class Point:
    
    force = Vector2(0, 0.3)
    
    def __init__(self, position, velocity, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.max_life_time = randrange(200, 500)
        self.life_time = self.max_life_time

    def update(self, dtime):
        self.position += self.velocity * dtime + self.force * dtime * dtime // 2
        self.velocity += self.force * dtime
        self.life_time -= 1
        
    def life_left(self):
        return self.life_time / self.max_life_time