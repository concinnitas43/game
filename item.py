from obj import *
import os

item_fuel = pygame.image.load(os.path.join('images', 'item_fuel.png'))
item_fuel = pygame.transform.scale(item_fuel, (30, 30))

item_stop_fuel = pygame.image.load(os.path.join('images', 'item_stop_fuel.png'))
item_stop_fuel = pygame.transform.scale(item_stop_fuel, (30, 30))

item_invincible = pygame.image.load(os.path.join('images', 'item_invincible.png'))
item_invincible = pygame.transform.scale(item_invincible, (30, 30))

item_guide = pygame.image.load(os.path.join('images', 'item_guide.png'))
item_guide = pygame.transform.scale(item_guide, (30, 30))
class Item(Obj):
    def __init__(self, x, y, s):

        super().__init__(x, y)

        self.skill = s

    def display(self, surface):
        if self.skill == 'fuel':
            item_rect = item_fuel.get_rect()

            item_rect.centerx = self.pos.x
            item_rect.centery = self.pos.y

            pygame.draw.circle(surface, (78, 207, 140), (self.pos.x, self.pos.y), self.radius)
            surface.blit(item_fuel, item_rect)

        if self.skill == 'stop_fuel':
            item_rect = item_stop_fuel.get_rect()

            item_rect.centerx = self.pos.x
            item_rect.centery = self.pos.y

            pygame.draw.circle(surface, (78, 207, 140), (self.pos.x, self.pos.y), self.radius)
            surface.blit(item_stop_fuel, item_rect)

        if self.skill == 'invincible':
            item_rect = item_invincible.get_rect()

            item_rect.centerx = self.pos.x
            item_rect.centery = self.pos.y

            pygame.draw.circle(surface, (78, 207, 140), (self.pos.x, self.pos.y), self.radius)
            surface.blit(item_invincible, item_rect)
        if self.skill == 'guide':
            item_rect = item_guide.get_rect()

            item_rect.centerx = self.pos.x
            item_rect.centery = self.pos.y

            pygame.draw.circle(surface, (78, 207, 140), (self.pos.x, self.pos.y), self.radius)
            surface.blit(item_guide, item_rect)
