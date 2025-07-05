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
        'hunter_up': load_image(os.path.join(asset_dir, 'hunter_up.png')),
        'hunter_down': load_image(os.path.join(asset_dir, 'hunter_down.png')),
        'hunter_left': load_image(os.path.join(asset_dir, 'hunter_left.png')),
        'hunter_right': load_image(os.path.join(asset_dir, 'hunter_right.png')),
        'arrow_up': load_image(os.path.join(asset_dir, 'arrow_up.png')),
        'arrow_down': load_image(os.path.join(asset_dir, 'arrow_down.png')),
        'arrow_left': load_image(os.path.join(asset_dir, 'arrow_left.png')),
        'arrow_right': load_image(os.path.join(asset_dir, 'arrow_right.png')),
    }
