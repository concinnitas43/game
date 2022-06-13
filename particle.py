from obj import *
from vec import *
import random

class Particle(Obj):
    def __init__(self, x, y, vx, vy):

        super().__init__(x, y)

        self.radius = random.random() *10 
        self.color = (200 + random.random() * 50 - 25 , 100 + random.random() * 50, 100 + random.random() * 50)
        self.vel = vec(vx, vy) * -20
        self.vel += vec(random.random(), random.random()) * 300
        self.lifetime = 3

    def display(self, surface):

        pygame.draw.circle(surface, self.color, (self.pos.x, self.pos.y), self.radius)


    def update(self, dt, vel):
        self.pos = vec(self.pos.x + self.vel.x * dt, self.pos.y + self.vel.y*dt - dt * vel)

