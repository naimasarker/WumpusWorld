import pygame
import os

def load_image(path, size=(60, 60)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

def load_assets():
    asset_dir = 'Assets/Images'
    return {
        'cell': load_image(os.path.join(asset_dir, 'initial_cell.png')),
        'pit': load_image(os.path.join(asset_dir, 'pit.png')),
        'gold': load_image(os.path.join(asset_dir, 'gold.png')),
        'wumpus': load_image(os.path.join(asset_dir, 'wumpus.png')),
    }
