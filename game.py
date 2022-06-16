from screen import *
import os
from item import *
from spaceship import * 
import pygame
from setting import *

N = 8 # number of asteroids
M = 1 # number of items
items = ['fuel', 'stop_fuel', 'invincible', 'guide'] # Types of items

def random_item(): # Get a random item
    x = random.random()
    if x < 0.25:
        return items[0] 
    if x < 0.5:
        return items[1]
    if x < 0.75:
        return items[2]
    return items[3]

class Background(pygame.sprite.Sprite): # Background class for objects like background or fuel gauge which doesn't collide with the spaceship
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background(os.path.join('images', 'background.png'), [0,0])
fuelGauge = Background(os.path.join('images', 'fuel_gauge.png'), [30, 9])
heart = Background(os.path.join('images', 'heart.png'), [0, 0]) # Haer

fuelGauge.image = pygame.transform.scale(fuelGauge.image, [WIDTH-50, 35]) # Image Scaling
heart.image = pygame.transform.scale(heart.image, [25, 25])

def color(t): # 0 <= t <= 1: Get the color for the fuel
    return (78 + t * (+129), 207 + t * (-125), 140 + t * (-78))


class Game(Screen): # Game Screen

    def __init__(self, width, height):
        super().__init__(width, height)

        self.objs = [] # Obstacles
        self.items = [] # Items
        self.spaceship = Spaceship(width / 2, height - 100) # spaceship
        self.score = 0 # Score : distance
        self.fpsClock = pygame.time.Clock() # clock
        self.setting = Setting() # setting

        if self.setting.settings["mode"] == 0: # EASY
            self.N = 6
            self.M = 1
        elif self.setting.settings["mode"] == 1: # HARD
            self.N = 10
            self.M = 1

        for _ in range(self.N): # N objects added
            self.objs.append(Obj(random.random() * self.width, random.random() * self.height * 2 / 3 + 1* self.height/ 3)) 
        for _ in range(self.M): # M objecs added
            self.items.append(Item(random.random() * (self.width-100) + 50, random.random() * self.height * 2 / 3 + self.height / 3, random_item()))

    def reset(self): # Reset for retrying, almost like init
        self.objs = []
        self.items = []
        self.spaceship = Spaceship(self.width / 2, self.height - 100)
        self.spaceship.heart = 3 -int(self.setting.settings["heart"])
        self.score = 0
        self.fpsClock = pygame.time.Clock()
        if self.setting.settings["mode"] == 0: # EASY
            self.N = 6
            self.M = 1
        elif self.setting.settings["mode"] == 1:
            self.N = 10
            self.M = 1
        for _ in range(self.N):
            self.objs.append(Obj(random.random() * self.width, random.random() * self.height / 3 - self.height * 2 / 3))
        for _ in range(self.M):
            self.items.append(Item(random.random() * self.width, random.random() * self.height * 2 / 3 - self.height / 3, random_item()))

    def update(self, dt, acc, trq): # update each image 
        # Increment score (distance)
        self.score += self.spaceship.vel.y * dt
        # Lower Each gauge
        if self.spaceship.invincible > 0:
            self.spaceship.invincible -= dt
        if self.spaceship.stop_fuel > 0:
            self.spaceship.stop_fuel -= dt
        if self.spaceship.guide > 0:
            self.spaceship.guide -= dt

        # update (move) objects
        self.spaceship.update(dt, acc, trq)
        for o in self.objs: 
            o.update(dt, -self.spaceship.vel.y)

            # pop objects if they get too far 
            if o.pos.y > self.height+20:
                self.objs.remove(o)
                self.objs.append(Obj(random.random() * self.width, random.random() * (-0.1 * self.height) ))
                if random.random() < 0.05: # for some chance, two obj spawns
                    self.objs.append(Obj(random.random() * self.width, random.random() * (-0.2 * self.height) ))

        for o in self.items: 
            o.update(dt, -self.spaceship.vel.y)

            if o.pos.y > self.height+20:
                self.items.remove(o)
                self.items.append(Item(random.random() * self.width, random.random() * (-0.1 * self.height), items[random.randint(0, 3)]))

    def collision(self): # Detects collision
        """
        Detects collision and returns a tuple
        tuple : (bool, object)
        - bool : if the collision happened 
        - object : if the collision happened, the collided object
        """
        # Two detection points
        pos2 = self.spaceship.pos + vec(-18 * math.sin(math.radians(self.spaceship.angle)), -18 * math.cos(math.radians(self.spaceship.angle)))
        pos3 = self.spaceship.pos + vec(-30 * math.sin(math.radians(self.spaceship.angle)), -30 * math.cos(math.radians(self.spaceship.angle)))

        # take object position and return
        collided = lambda p: ( (dist2(p, self.spaceship.pos) < (o.radius + 15) ** 2) or (dist2(p, pos2) < (o.radius + 12) ** 2) or (dist2(p, pos3) < (o.radius + 6) ** 2))

        for o in self.objs:
            if collided(o.pos):
                return (True, o) # Collision O
                #pygame.mixer.Sound.play(self.sounds["collision"][0])

        # Item 
        for i in self.items:
            if collided(i.pos):
                if i.skill == 'fuel':
                    self.spaceship.fuel += 30
                    self.spaceship.fuel = min(100, self.spaceship.fuel)
                elif i.skill == 'invincible':
                    self.spaceship.invincible += 15
                elif i.skill == 'stop_fuel':
                    self.spaceship.stop_fuel += 15
                elif i.skill == 'guide':
                    self.spaceship.guide += 50

                self.items.remove(i)
                self.items.append(Item(random.random() * self.width, random.random() * (-0.1 * self.height), random_item()))

        # Edge detection, checks for if loop is enabled
        if not(0 <= self.spaceship.pos.x <= self.width):
            if self.setting.settings["loop"] == 0:
                self.spaceship.pos.x %= self.width
            else:
                return (True, None)
        return (False, None)

    def display(self, WIN):
        """display"""
        WIN.blit(BackGround.image, BackGround.rect)

        # spaceship.damage is the counter for the screen urning red.
        if self.spaceship.damage > 0:
            WIN.fill((255, 0, 0))
            self.spaceship.damage -= 1

        # display each items
        for o in self.objs + self.items:
            o.display(WIN)

        # display spaceship
        self.spaceship.display(WIN)
        
        # display fuel gauge
        pygame.draw.rect(WIN, color(1 - self.spaceship.fuel / 100), pygame.Rect(30, 10, (self.width - 90) * self.spaceship.fuel /100, 30))
        WIN.blit(fuelGauge.image, fuelGauge.rect)

        # display some texts ( score )
        my_font = pygame.font.SysFont("monaco", 15, True, False)

        score_text = my_font.render(str(int(self.score)), True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        score_text_rect.centerx = 60
        score_text_rect.centery = 60
        WIN.blit(score_text, score_text_rect)

        # Heart 
        for i in range(self.spaceship.heart):
            heart.rect.centerx = 500 - 30 * i
            heart.rect.centery = 130
            WIN.blit(heart.image, heart.rect)


        # Invincibility / stop_fuel bar
        if self.spaceship.invincible > 0:
            pygame.draw.rect(WIN, (255, 217, 0), pygame.Rect(90, 50, (self.width - 300) * self.spaceship.invincible / 15, 20))
            if self.spaceship.stop_fuel > 0:
                pygame.draw.rect(WIN, (0, 179, 255), pygame.Rect(90, 80, (self.width - 300) * self.spaceship.stop_fuel / 15, 20))
        else:
            if self.spaceship.stop_fuel > 0:
                pygame.draw.rect(WIN, (0, 179, 255), pygame.Rect(90, 50, (self.width - 300) * self.spaceship.stop_fuel / 15, 20))
        


    def do(self, WIN): # It is called every frame
        """
        Do returns a tuple
        (bool, extra_information)
        bool is False if quitting
        """
        acc = 0
        trq = 0

        # Get some inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (False, [])

        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.spaceship.fuel > 0:
                acc += -ACC
                if self.spaceship.stop_fuel <= 0:
                    self.spaceship.fuel -= 3 * dt

            
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            # acc += -ACC / 2
            if self.spaceship.fuel > 0:
                trq += TRQ
                
                if self.spaceship.stop_fuel <= 0:
                    self.spaceship.fuel -= 1 * dt

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            # acc += -ACC / 2
            if self.spaceship.fuel > 0:
                trq += -TRQ
                if self.spaceship.stop_fuel <= 0:
                    self.spaceship.fuel -= 1 * dt

        # 'reset' goes to the reset screen
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            return ('reset', {"score" : self.score})

        # Actually displays something
        WIN.fill((0, 0, 0))

        self.update(dt, acc, trq)
        if self.collision()[0]: # gets the collision data and does things...

            # the collision happened, so spawns a new object
            self.objs.append(Obj(random.random() * self.width, random.random() * (-0.1 * self.height) ))
            if random.random() < 0.05:
                self.objs.append(Obj(random.random() * self.width, random.random() * (-0.1 * self.height) ))

            if self.collision()[1] == None: # Hit the wall
                self.spaceship.heart -= 1
                self.spaceship.damage = 3
            else:
                self.objs.remove(self.collision()[1]) # removes the object hit.
                if (self.spaceship.invincible <= 0): # invincible?
                    self.spaceship.heart -= 1
                    self.spaceship.vel = self.spaceship.vel * 0.3
                    self.spaceship.angular_vel = self.spaceship.angular_vel * 0.3
                    self.spaceship.damage = 3
                else:
                    self.spaceship.invincible = max(0, self.spaceship.invincible - 3)


        if self.spaceship.heart <= 0 or (self.spaceship.fuel == 0 and abs(self.spaceship.vel.y) < 1): # DEATH
            return ('reset', {"score" : self.score})
        self.display(WIN)        

        # UPDATES
        self.fpsClock.tick(FPS)
        pygame.display.flip()
        return (True, [])












