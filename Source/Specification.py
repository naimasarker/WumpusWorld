import pygame
import os

# Get the absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Speed
SPEED = 100          # Change the speed of the game here.

# Window
SCREEN_WIDTH = 970
SCREEN_HEIGHT = 710
CAPTION = 'Wumpus World'

# Cell
IMG_INITIAL_CELL = os.path.join(BASE_DIR, 'Assets', 'Images', 'initial_cell.png')
IMG_DISCOVERED_CELL = os.path.join(BASE_DIR, 'Assets', 'Images', 'discovered_cell.png')

# Object
IMG_PIT = os.path.join(BASE_DIR, 'Assets', 'Images', 'pit.png')
IMG_WUMPUS = os.path.join(BASE_DIR, 'Assets', 'Images', 'wumpus.png')
IMG_GOLD = os.path.join(BASE_DIR, 'Assets', 'Images', 'gold.png')

# Hunter
IMG_HUNTER_RIGHT = os.path.join(BASE_DIR, 'Assets', 'Images', 'hunter_right.png')
IMG_HUNTER_LEFT = os.path.join(BASE_DIR, 'Assets', 'Images', 'hunter_left.png')
IMG_HUNTER_UP = os.path.join(BASE_DIR, 'Assets', 'Images', 'hunter_up.png')
IMG_HUNTER_DOWN = os.path.join(BASE_DIR, 'Assets', 'Images', 'hunter_down.png')

IMG_ARROW_RIGHT = os.path.join(BASE_DIR, 'Assets', 'Images', 'arrow_right.png')
IMG_ARROW_LEFT = os.path.join(BASE_DIR, 'Assets', 'Images', 'arrow_left.png')
IMG_ARROW_UP = os.path.join(BASE_DIR, 'Assets', 'Images', 'arrow_up.png')
IMG_ARROW_DOWN = os.path.join(BASE_DIR, 'Assets', 'Images', 'arrow_down.png')

# Map
MAP_LIST = [
    os.path.join(BASE_DIR, 'Assets', 'Input', 'map_1.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Input', 'map_2.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Input', 'map_3.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Input', 'map_4.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Input', 'map_5.txt'),
    # os.path.join(BASE_DIR, 'Assets', 'Input', 'map_6.txt')
]
MAP_NUM = len(MAP_LIST)

# Output
OUTPUT_LIST = [
    os.path.join(BASE_DIR, 'Assets', 'Output', 'result_1.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Output', 'result_2.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Output', 'result_3.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Output', 'result_4.txt'),
    os.path.join(BASE_DIR, 'Assets', 'Output', 'result_5.txt'),
    # os.path.join(BASE_DIR, 'Assets', 'Output', 'result_6.txt')
]

# Fonts
# FONT_MRSMONSTER = os.path.join(BASE_DIR, 'Assets', 'Fonts', 'mrsmonster.ttf')
FONT_MRSMONSTER = os.path.join(BASE_DIR, 'Assets', 'Fonts', 'SuperShiny-0v0rG.ttf')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0)

# state
RUNNING = 'running'
GAMEOVER = 'gameover'
WIN = 'win'
TRYBEST = 'trybest'
MAP = 'map'

LEVEL_1_POS = pygame.Rect(235, 120, 500, 50)
LEVEL_2_POS = pygame.Rect(235, 200, 500, 50)
LEVEL_3_POS = pygame.Rect(235, 280, 500, 50)
LEVEL_4_POS = pygame.Rect(235, 360, 500, 50)
LEVEL_5_POS = pygame.Rect(235, 440, 500, 50)
# LEVEL_6_POS = pygame.Rect(235, 520, 500, 50)
EXIT_POS = pygame.Rect(235, 600, 500, 50)