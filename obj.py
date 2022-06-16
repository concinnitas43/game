from vec import *
import os
import pygame
import random


# obj (asteroid / items)
asteroid = [pygame.image.load(os.path.join('images', 'asteroid' + str(i) + '.png')) for i in range(1, 4)]

# Scaling images to be the same size..
scale_factor = [5/3+1, 5/3+0.25, 5/3-0.2]

for i in range(0, 3):
    asteroid[i] = pygame.transform.scale(asteroid[i], (30 * scale_factor[i], 30 * scale_factor[i]))

class Obj:
    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.radius = 15 
        self.icon = random.randint(1, 3)

    def update(self, dt, vel):
        self.pos = vec(self.pos.x + self.vel.x * dt, self.pos.y + self.vel.y*dt - dt * vel) # update accordingly to rockets y vel

    def display(self, surface):
        # Simple displaying
        asteroid_rect = asteroid[self.icon-1].get_rect()

        asteroid_rect.centerx = self.pos.x
        asteroid_rect.centery = self.pos.y

        # pygame.draw.circle(surface, (255, 255, 255), (self.pos.x, self.pos.y), self.radius)
        surface.blit(asteroid[self.icon-1], asteroid_rect)


        
        


