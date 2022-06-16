import pygame
import random
from spaceship import *
from screen import *
from intro import *
from game import *
from reset import *
from menu import *
from obj import *
from setting import *
from help_screen import *

## INIT
pygame.init()

# Little bit of constants
FPS = 30
dt = 1 / 30
fpsClock = pygame.time.Clock()
N = 10
asteroidtimer = 100
WIDTH, HEIGHT = 480, 640
ACC = 40
TRQ = 100

# basic settings
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Accelerate")

# Screen Manager for storing the screens
master = ScreenManager()

# Game Screen
GAME_SCREEN = Game(WIDTH, HEIGHT)
GAME_SCREEN.spaceship = Spaceship(WIDTH / 2, HEIGHT - 100)

# Intro Screen
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

# Reset Screen
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

# Menu Screen
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
            }, {
                "content" : "Setting",
                "size" : 10,
                "pos" : [WIDTH / 2, HEIGHT / 2 + 180],
            }
        ]
    }

# Help Screen
HELP_SCREEN = Help(WIDTH, HEIGHT)
HELP_SCREEN.config = {
    "title" : "Help",
    "others" : [
            {
                "content" : "Space to go back",
                "size" : 10,
                "pos" : [WIDTH / 2, HEIGHT / 3 + 60],
            }, {
                "content" : "",
                "size" : 10,
                "pos" : [WIDTH / 3, HEIGHT / 3 + 120],
            }
        ]
    }

# Setting Screen. No config since everything is in __init__
SETTING_SCREEN = SettingScreen(WIDTH, HEIGHT, Setting())

master.screens.append(INTRO_SCREEN)   # 0
master.screens.append(GAME_SCREEN)    # 1
master.screens.append(RESET_SCREEN)   # 2
master.screens.append(MENU_SCREEN)    # 3
master.screens.append(HELP_SCREEN)    # 4 
master.screens.append(SETTING_SCREEN) # 5
master.current=master.screens[0] # Start with the intro

def main():
    run = True

    while run:
        (x, data) = master.current.do(WIN) # redirects the screen with the return value
        if x == 'menu':
            master.current = master.screens[3]
            master.current.reset()

        if x == 'game':
            master.current = master.screens[1]
            master.current.setting = master.screens[5].setting
            master.current.reset()

        if x == 'reset':
            master.screens[2].config["others"][1]["content"] = str(int(data["score"]))
            master.current = master.screens[2]

        if x == 'help':
            master.current = master.screens[4]
            master.current.reset()

        if x == 'setting':
            master.current = master.screens[5]
            master.current.reset()

        # Quits if returns false
        if not x:
            run = False
            break
    pygame.quit()

if __name__ == "__main__":
    main()




