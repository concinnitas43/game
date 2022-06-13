import pygame
import random
from spaceship import *
from screen import *
from intro import *
from game import *
from reset import *
from menu import *
from obj import *
from help_screen import *

pygame.init()


FPS = 30
dt = 1 / 30
fpsClock = pygame.time.Clock()
N = 10
asteroidtimer = 100
WIDTH, HEIGHT = 480, 640
ACC = 40
TRQ = 100

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Accelerate")

master = ScreenManager()

GAME_SCREEN = Game(WIDTH, HEIGHT)
GAME_SCREEN.spaceship = Spaceship(WIDTH / 2, HEIGHT - 100)


INTRO_SCREEN = Intro(WIDTH, HEIGHT)
INTRO_SCREEN.config = {
        "title" : "Accelerate",
        "others" : [
                {
                    "content" : "Press <Space> to continue",
                    "size" : 10,
                    "pos" : [WIDTH / 2, HEIGHT / 2 + 60],
                }, 
            ]
        }

RESET_SCREEN = Reset(WIDTH, HEIGHT)
RESET_SCREEN.config = {
        "title" : "You Died",
        "others" : [
                {
                    "content" : "Press <Space> to retry",
                    "size" : 10,
                    "pos" : [WIDTH / 2, HEIGHT / 4 + 120],
                }, 
                {
                    "content" : None,
                    "pos" : [WIDTH / 2, HEIGHT / 4 + 60],
                }
            ]
        }

MENU_SCREEN = Menu(WIDTH, HEIGHT)
MENU_SCREEN.config = {
    "title" : "Menu",
    "others" : [
            {
                "content" : "Play",
                "size" : 10,
                "pos" : [WIDTH / 2, HEIGHT / 2 + 60],
            }, {
                "content" : "Help",
                "size" : 10,
                "pos" : [WIDTH / 2, HEIGHT / 2 + 120],
            }
        ]
    }



master.screens.append(INTRO_SCREEN)
master.screens.append(GAME_SCREEN)
master.screens.append(RESET_SCREEN)
master.screens.append(MENU_SCREEN)
master.current=master.screens[0]

def main():
    run = True
    while run:
        (x, data) = master.current.do(WIN)
        if x == 'menu':
            master.current = master.screens[3]
            master.current.reset()

        if x == 'game':
            master.current = master.screens[1]
            master.current.reset()

        if x == 'reset':
            master.screens[2].config["others"][1]["content"] = str(int(data["score"]))
            master.current = master.screens[2]

        if not x:
            run = False
            break
    pygame.quit()

if __name__ == "__main__":
    main()
