from screen import *
import pygame

class Reset(Screen):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.fpsClock = pygame.time.Clock()
        self.username = ""
        self.scoreboard = dict()
        self.scores = []

    def update(self, *args):
        pass

    def reset(self, *args):
        pass


    def do(self, WIN):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (False, [])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.username = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.username in self.scoreboard.keys():
                        self.scoreboard[self.username].append(int(self.config["others"][1]["content"]))
                        self.scores.append((self.config["others"][1]["content"], self.username))
                    else:
                        self.scoreboard[self.username] = [ int(self.config["others"][1]["content"]) ]
                        self.scores.append((self.config["others"][1]["content"], self.username))
                    self.username = ""
                    self.scores.sort()
                    print(self.scoreboard)
                else:
                    self.username += event.unicode

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.selected == 0:
                self.selected = 1
            else:
                self.selected = 3 - self.selected

        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.selected == 0:
                self.selected = 2
            else:
                self.selected = 3 - self.selected

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            return ('game', [])

        
        WIN.fill((0, 0, 0))

        my_font = pygame.font.SysFont("monaco", 30, True, False)

        text_title = my_font.render(self.config["title"], True, (255, 255, 255))
        text_title_rect = text_title.get_rect()
        text_title_rect.centerx = self.width // 2
        text_title_rect.centery = self.height // 4
        WIN.blit(text_title, text_title_rect)


        for i in range(len(self.config["others"])):
            tfont = pygame.font.SysFont("monaco", 15, True, False)
            some_text = self.config["others"][i]
            text = tfont.render(some_text["content"], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = some_text["pos"][0]
            text_rect.centery = some_text["pos"][1]
            WIN.blit(text, text_rect)

        
        if self.username == "":
            display_user = "Type Username to Save"
        else:
            display_user = self.username

        ufont = pygame.font.SysFont("monaco", 15, True, False)
        text = ufont.render(display_user, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = WIDTH / 2
        text_rect.centery = HEIGHT / 4 + 170
        WIN.blit(text, text_rect)

        sfont = pygame.font.SysFont("monaco", 20, True, False)
        text = sfont.render("Score Board", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = WIDTH / 2
        text_rect.centery = HEIGHT / 4 + 240
        WIN.blit(text, text_rect)

        sfont = pygame.font.SysFont("monaco", 15, True, False)
        for i in range(min(5, len(self.scores))):
            text = sfont.render(self.scores[i][1] + ": " + self.scores[i][0], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = WIDTH / 2
            text_rect.centery = HEIGHT / 4 + 270 + 30*i
            WIN.blit(text, text_rect)

        self.fpsClock.tick(FPS)
        pygame.display.flip()
        return (True, [])


