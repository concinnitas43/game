from screen import *
import pygame
# Menu
COOL_TIME = 5

# Different option types
options = ['game', 'help', 'setting']

# Menu (Screen)
class Menu(Screen):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.fpsClock = pygame.time.Clock()
        self.selected = 0
        self.cooltime = COOL_TIME

    def update(self, *args):
        pass

    def reset(self, *args): # you don't need to reset the menu class
        pass

    def do(self, WIN):
        for event in pygame.event.get():  # Basic stuff
            if event.type == pygame.QUIT:
                return (False, [])

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.cooltime == 0:
                #print(options[self.selected])
                return (options[self.selected], []) # Goes to the selected

        if pygame.key.get_pressed()[pygame.K_DOWN]: # Goes down the index
            if self.cooltime == 0:
                self.selected = (self.selected + 1) % len(options)
                self.cooltime = COOL_TIME

        if pygame.key.get_pressed()[pygame.K_UP]: # Goes up the index
            if self.cooltime == 0:
                self.selected = (self.selected - 1) % len(options)
                self.cooltime = COOL_TIME


        self.cooltime = max(0, self.cooltime - 1) # decrease the cooltime

        WIN.fill((0, 0, 0))

        # Just displays everything

        my_font = pygame.font.SysFont("monaco", 30, True, False)

        text_title = my_font.render(self.config["title"], True, (255, 255, 255))
        text_title_rect = text_title.get_rect()
        text_title_rect.centerx = self.width // 2
        text_title_rect.centery = self.height // 2
        WIN.blit(text_title, text_title_rect)


        for i in range(len(self.config["others"])):
            if i == self.selected:
                tfont = pygame.font.SysFont("monaco", 20, True, False)
            else:
                tfont = pygame.font.SysFont("monaco", 15, True, False)
            some_text = self.config["others"][i]
            text = tfont.render(some_text["content"], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = some_text["pos"][0]
            text_rect.centery = some_text["pos"][1]
            WIN.blit(text, text_rect)

        self.fpsClock.tick(FPS)
        pygame.display.flip()
        return (True, [])





        


