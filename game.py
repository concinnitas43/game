from screen import *
import os
from item import *
from particle import *
from spaceship import * 
import pygame

N = 8
M = 1
items = ['fuel', 'stop_fuel', 'invincible', 'guide']

def random_item():
    x = random.random()
    if x < 0.25:
        return items[0] 
    if x < 0.5:
        return items[1]
    if x < 0.75:
        return items[2]
    return items[3]

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background(os.path.join('images', 'background.png'), [0,0])
fuelGauge = Background(os.path.join('images', 'fuel_gauge.png'), [30, 9])
heart = Background(os.path.join('images', 'heart.png'), [0, 0])

fuelGauge.image = pygame.transform.scale(fuelGauge.image, [WIDTH-50, 35])
heart.image = pygame.transform.scale(heart.image, [25, 25])
# fuelGauge.rect.centerx = WIDTH / 2
# fuelGauge.rect.centery = 40


def color(t): # 0 <= t <= 1:
    return (78 + t * (+129), 207 + t * (-125), 140 + t * (-78))


class Game(Screen):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.objs = []
        self.items = []
        self.particles = [] 
        self.spaceship = Spaceship(width / 2, height - 100)
        self.score = 0
        self.fpsClock = pygame.time.Clock()
        for _ in range(N):
            self.objs.append(Obj(random.random() * self.width, random.random() * self.height * 2 / 3 - self.height/ 3))
        for _ in range(M):
            self.items.append(Item(random.random() * (self.width-100) + 50, random.random() * self.height * 2 / 3 - self.height / 3, random_item()))

    def reset(self):
        self.objs = []
        self.items = []
        self.particles = []
        self.spaceship = Spaceship(self.width / 2, self.height - 100)
        self.score = 0
        self.fpsClock = pygame.time.Clock()
        for _ in range(N):
            self.objs.append(Obj(random.random() * self.width, random.random() * self.height / 2))
        for _ in range(M):
            self.items.append(Item(random.random() * self.width, random.random() * self.height * 2 / 3 - self.height / 3, random_item()))

    def update(self, dt, acc, trq):
        self.score += self.spaceship.vel.y * dt
        if self.spaceship.invincible > 0:
            self.spaceship.invincible -= dt
        if self.spaceship.stop_fuel > 0:
            self.spaceship.stop_fuel -= dt
        if self.spaceship.guide > 0:
            self.spaceship.guide -= dt

        self.spaceship.update(dt, acc, trq)
        for o in self.objs: 
            o.update(dt, -self.spaceship.vel.y)

            if o.pos.y > self.height+20:
                self.objs.remove(o)
                self.objs.append(Obj(random.random() * self.width, random.random() * (-0.1 * self.height) ))
                if random.random() < 0.05:
                    self.objs.append(Obj(random.random() * self.width, random.random() * (-0.1 * self.height) ))

        for o in self.items: 
            o.update(dt, -self.spaceship.vel.y)

            if o.pos.y > self.height+20:
                self.items.remove(o)
                self.items.append(Item(random.random() * self.width, random.random() * (-0.1 * self.height), o.skill))


                    
    def collision(self):
        for o in self.objs:
            if dist2(o.pos, self.spaceship.pos) < 1000:
                return (True, o)

        for i in self.items:
            if dist2(i.pos, self.spaceship.pos) < 1000:
                if i.skill == 'fuel':
                    self.spaceship.fuel += 10
                    self.spaceship.fuel = min(100, self.spaceship.fuel)
                elif i.skill == 'invincible':
                    self.spaceship.invincible += 10 
                elif i.skill == 'stop_fuel':
                    self.spaceship.stop_fuel += 10
                elif i.skill == 'guide':
                    self.spaceship.guide += 15

                self.items.remove(i)
                self.items.append(Item(random.random() * self.width, random.random() * (-0.1 * self.height), random_item()))


        if not (0 <= self.spaceship.pos.x <= self.width):
            return (True, None)
        return (False, None)

    def display(self, WIN):
        WIN.blit(BackGround.image, BackGround.rect)

        if self.spaceship.damage > 0:
            WIN.fill((255, 0, 0))
            self.spaceship.damage -= 1

        for o in self.objs + self.items + self.particles:
            o.display(WIN)

        self.spaceship.display(WIN)
        pygame.draw.rect(WIN, color(1 - self.spaceship.fuel / 100), pygame.Rect(30, 10, (self.width - 90) * self.spaceship.fuel /100, 30))
        WIN.blit(fuelGauge.image, fuelGauge.rect)

        my_font = pygame.font.SysFont("monaco", 15, True, False)

        score_text = my_font.render(str(int(self.score)), True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        score_text_rect.centerx = 60
        score_text_rect.centery = 60
        WIN.blit(score_text, score_text_rect)

        for i in range(self.spaceship.heart):
            heart.rect.centerx = 500 - 30 * i
            heart.rect.centery = 130
            WIN.blit(heart.image, heart.rect)

        if self.spaceship.invincible > 0:
            pygame.draw.rect(WIN, (255, 217, 0), pygame.Rect(90, 50, (self.width - 300) * self.spaceship.invincible / 10, 20))
            if self.spaceship.stop_fuel > 0:
                pygame.draw.rect(WIN, (0, 179, 255), pygame.Rect(90, 80, (self.width - 300) * self.spaceship.stop_fuel / 5, 20))
        else:
            if self.spaceship.stop_fuel > 0:
                pygame.draw.rect(WIN, (0, 179, 255), pygame.Rect(90, 50, (self.width - 300) * self.spaceship.stop_fuel / 10, 20))
        


    def do(self, WIN):
        acc = 0
        trq = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (False, [])

        if pygame.key.get_pressed()[pygame.K_UP]:
            acc += -ACC
            if self.spaceship.stop_fuel <= 0:
                self.spaceship.fuel -= 3 * dt

            
            # for _ in range(5) : self.particles.append(Particle(self.spaceship.pos.x, self.spaceship.pos.y, math.cos(self.spaceship.angle), math.sin(self.spaceship.angle)))

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            # acc += -ACC / 2
            trq += TRQ
            if self.spaceship.stop_fuel <= 0:
                self.spaceship.fuel -= 1 * dt

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            # acc += -ACC / 2
            trq += -TRQ
            if self.spaceship.stop_fuel <= 0:
                self.spaceship.fuel -= 1 * dt



        WIN.fill((0, 0, 0))

        self.update(dt, acc, trq)
        if self.collision()[0] and (self.spaceship.invincible <= 0):
            if self.spaceship.invincible <= 0: 
                self.spaceship.heart -= 1
                self.spaceship.damage = 3
            if self.collision()[1] == None:
                self.spaceship.heart -= 1
                self.spaceship.damage = 3

        if self.collision()[1] != None:
            self.objs.remove(self.collision()[1])

        if self.spaceship.heart <= 0 or self.spaceship.fuel <= 0:
            return ('reset', {"score" : self.score})
        self.display(WIN)        

        self.fpsClock.tick(FPS)
        pygame.display.flip()
        return (True, [])












