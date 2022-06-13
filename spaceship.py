import pygame
import math
import os
from vec import *

SPACESHIP_WIDTH  = 60
SPACESHIP_HEIGHT = 80

spaceship = pygame.image.load(os.path.join('images', 'spaceship.png'))
spaceship_acc = pygame.image.load(os.path.join('images', 'spaceship_acc.png'))

spaceship = pygame.transform.scale(spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_acc = pygame.transform.scale(spaceship_acc, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

class Spaceship:
    def __init__(self, x, y, width=SPACESHIP_WIDTH, height=SPACESHIP_HEIGHT):
        self.pos = vec( x, y )
        self.vel = vec( 0, 30 )

        self.angle = 0
        self.angular_vel = 0

        self.width = width
        self.height = height

        self.heart = 3
        self.invincible = 0
        self.stop_fuel = 0
        self.guide = 0

        self.damage = 0

        self.fuel = 100

        self.acc = False

    def update(self, dt, acc, trq=0):
        self.acc = (acc != 0)
        vacc = vec(math.sin(math.radians(self.angle)), -math.cos(math.radians(self.angle))) * acc
        self.vel += vacc * dt 
        self.vel *= 0.999
        self.pos.x += self.vel.x * dt
        # self.pos += self.vel * dt 

        self.angular_vel += trq * dt
        self.angle += self.angular_vel * dt 
        self.angular_vel *= 0.999
        pass

    def display(self, surface):

        if self.acc:
            image = spaceship_acc
        else:
            image = spaceship
        
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]

        box_rotate = [p.rotate(self.angle) for p in box]

        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])


        origin = (self.pos.x + min_box[0], self.pos.y - max_box[1])

        rotated_image = pygame.transform.rotate(image, self.angle)
        
        image_rect = image.get_rect(topleft = (self.pos.x - self.width/2, self.pos.y-self.height/2))
        offset_center_to_pivot = pygame.math.Vector2([self.pos.x, self.pos.y]) - image_rect.center

        rotated_offset = offset_center_to_pivot.rotate(-self.angle)

        rotated_image_center = (self.pos.x - rotated_offset.x, self.pos.y - rotated_offset.y)

        rotated_image = pygame.transform.rotate(image, self.angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        surface.blit(rotated_image, rotated_image_rect)
        if self.guide > 0:
            pygame.draw.line(surface, (5, 235, 12), (self.pos.x, self.pos.y), (self.pos.x + self.vel.x * 1.5, self.pos.y - self.vel.y * 1.5))


