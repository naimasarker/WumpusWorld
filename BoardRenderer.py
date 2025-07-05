import pygame
from typing import List
from assets import load_assets
from BoardLoader import Board

class BoardRenderer:
    def __init__(self, screen: pygame.Surface, board: Board, cell_size=64, spacing=6):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size
        self.spacing = spacing
        self.assets = load_assets()

    def draw_board(self):
        for i in range(10):
            for j in range(10):
                x = j * (self.cell_size + self.spacing) + self.spacing
                y = i * (self.cell_size + self.spacing) + self.spacing

                # Draw base cell background
                self.screen.blit(self.assets['cell'], (x, y))

                # Overlay object if exists
                objects = self.board.get_cell_objects(i, j)
                if 'G' in objects:
                    self.screen.blit(self.assets['gold'], (x, y))
                elif 'P' in objects:
                    self.screen.blit(self.assets['pit'], (x, y))
                elif 'W' in objects:
                    self.screen.blit(self.assets['wumpus'], (x, y))
