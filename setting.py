from screen import *
import pygame

# FILE foro managing the setting screen

COOL_TIME = 6

# Different options
index_to_option = ["mode", "loop", "heart"]

# Just one object in this class, so just dumped everything on the init 
class Setting:

    def __init__(self):
        self.options = { # All the different options
                "mode" : ["easy", "hard"],
                "loop" : ["on", "off"],
                "heart": ["3", "2", "1"],
                }
        self.settings = { # The ""Current"" setting
                "mode" : 0,
                "loop" : 0,
                "heart" : 0,
                }

class SettingScreen(Screen):

    def __init__(self, width, height, setting):
        super().__init__(width, height)

        self.fpsClock = pygame.time.Clock()

        self.setting = setting

        self.selected = 0

        self.cooltime = COOL_TIME

    def update(self, *args):
        pass

    def reset(self, *args):
        pass


    def do(self, WIN): # Everything is almost same as menu or other screens..

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (False, [])

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.cooltime == 0:
                self.selected = (self.selected + 1) % len(self.setting.options)
                self.cooltime = COOL_TIME
        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.cooltime == 0:
                self.selected = (self.selected - 1) % len(self.setting.options)
                self.cooltime = COOL_TIME

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.cooltime == 0:

                self.setting.settings[index_to_option[self.selected]] = (self.setting.settings[index_to_option[self.selected]] + 1) % len(self.setting.options[index_to_option[self.selected]])

                self.cooltime = COOL_TIME

        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            if self.cooltime == 0:
                return ('menu', [])

        self.cooltime = max(0, self.cooltime - 1)
        WIN.fill((0, 0, 0))

        my_font = pygame.font.SysFont("monaco", 30, True, False)

        text_title = my_font.render("Settings", True, (255, 255, 255))
        text_title_rect = text_title.get_rect()
        text_title_rect.centerx = self.width // 2
        text_title_rect.centery = self.height // 3
        WIN.blit(text_title, text_title_rect)

        pygame.draw.rect(WIN, (64, 64, 64), pygame.Rect(0, self.height // 3 + 60 + 90 * self.selected, self.width, 60)) 

        for option in self.setting.options.keys(): # Display he options,
            for mode_index in range(len(self.setting.options[option])):
                l = len(self.setting.options[option])
                mode = self.setting.options[option][mode_index]
                # if mode == self.setting.settings[option]:

                if mode_index == self.setting.settings[option]: # Display the seleced ones big
                    bfont = pygame.font.SysFont("monaco", 20, True, False)
                    text = bfont.render(mode, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.centerx = (mode_index + 1) * self.width // (l + 1)
                    text_rect.centery = self.height // 3 + 90 + 90 * list(self.setting.options.keys()).index(option)
                    WIN.blit(text, text_rect)

                else: # Display the not selected ones small
                    tfont = pygame.font.SysFont("monaco", 15, True, False)
                    text = tfont.render(mode, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.centerx = (mode_index + 1) * self.width // (l + 1)
                    text_rect.centery = self.height // 3 + 90 + 90 * list(self.setting.options.keys()).index(option)
                    WIN.blit(text, text_rect)

        for option_index in range(len(index_to_option)): # Display the names of the option

            tfont = pygame.font.SysFont("monaco", 15, True, False)
            text = tfont.render(index_to_option[option_index], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = self.width / 2
            text_rect.centery = self.height // 3 + 45 + 90 * option_index
            WIN.blit(text, text_rect)

                   
        self.fpsClock.tick(FPS)
        pygame.display.flip()
        return (True, [])






