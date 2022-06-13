from screen import *
import pygame
COOL_TIME = 7

class Menu(Screen):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.fpsClock = pygame.time.Clock()
        self.selected = 0
        self.cooltime = COOL_TIME

    def update(self, *args):
        pass

    def reset(self, *args):
        pass

    def do(self, WIN):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (False, [])

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.cooltime == 0:
                if self.selected == 1:
                    return ('game', [])
                if self.selected == 1:
                    return ('help', [])

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.cooltime == 0:
                if self.selected == 0:
                    self.selected = 1
                else:
                    self.selected = 3 - self.selected
                self.cooltime = COOL_TIME

        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.cooltime == 0:
                if self.selected == 0:
                    self.selected = 2
                else:
                    self.selected = 3 - self.selected
                self.cooltime = COOL_TIME

        self.cooltime = max(0, self.cooltime - 1)

        WIN.fill((0, 0, 0))

        my_font = pygame.font.SysFont("monaco", 30, True, False)

        text_title = my_font.render(self.config["title"], True, (255, 255, 255))
        text_title_rect = text_title.get_rect()
        text_title_rect.centerx = self.width // 2
        text_title_rect.centery = self.height // 2
        WIN.blit(text_title, text_title_rect)


        for i in range(len(self.config["others"])):
            if i == self.selected-1:
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





        


