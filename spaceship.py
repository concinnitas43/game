import pygame
import math
import os
from vec import *

SPACESHIP_WIDTH  = 60
SPACESHIP_HEIGHT = 80

# Load some images

spaceship = pygame.image.load(os.path.join('images', 'spaceship.png'))
spaceship_acc = pygame.image.load(os.path.join('images', 'spaceship_acc.png'))
spaceship_left = pygame.image.load(os.path.join('images', 'spaceship_left.png'))
spaceship_right = pygame.image.load(os.path.join('images', 'spaceship_right.png'))

spaceship = pygame.transform.scale(spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_acc = pygame.transform.scale(spaceship_acc, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_left = pygame.transform.scale(spaceship_left, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_right = pygame.transform.scale(spaceship_right, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Rotating some image by and angle with fixed point (x, y)
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

        self.damage = 0 # Damage counter... It goes up to 3 when you take damage and gets back to 0 in 3 frames : turns the background to red for 3 frames

        self.fuel = 100 # Fuel

        self.acc = False # For choosing images
        self.trq = 0

    def update(self, dt, acc, trq=0):
        self.acc = (acc != 0)
        self.trq = trq
           

        # According to the formula 
        # a = \frac{dv}{dt}, \alpha = \frac{d\omega}{dt}
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

        # Choose the appropriate image
        if self.acc:
            image = spaceship_acc
        else:
            if self.trq == 0:
                image = spaceship
            elif self.trq > 0:
                image = spaceship_left
            else:
                image = spaceship_right

        
        # Code for rotating an image ...
        # I don't understand what happened here exactly, I just copied from stack overflow :D
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

        # Guide line
        if self.guide > 0:
            pygame.draw.line(surface, (5, 235, 12), (self.pos.x, self.pos.y), (self.pos.x + self.vel.x * 1.5, self.pos.y - self.vel.y * 1.5))

        # Hitbox
        # pygame.draw.circle(surface, (255, 255, 255), [self.pos.x, self.pos.y], 15, 2)
        # pygame.draw.circle(surface, (255, 255, 255), [self.pos.x - 18 * math.sin(math.radians(self.angle)), self.pos.y - 18 *  math.cos(math.radians(self.angle))], 12, 2)
        # pygame.draw.circle(surface, (255, 255, 255), [self.pos.x - 30 * math.sin(math.radians(self.angle)), self.pos.y - 30 *  math.cos(math.radians(self.angle))], 6, 2)


