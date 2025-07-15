# BoardRenderer.py
import pygame
from typing import List
from assets import load_assets
from BoardLoader import Board
from GameState import GameState, CellState
from enum import Enum  # Add this import

# Add this ColorTheme enum
class ColorTheme(Enum):
    CLASSIC = 0
    DARK = 1
    PASTEL = 2
    FOREST = 3

class BoardRenderer:
    def __init__(self, screen: pygame.Surface, board: Board, game_state: GameState, cell_size=50, spacing=4):
        self.screen = screen
        self.board = board
        self.game_state = game_state
        self.cell_size = cell_size
        self.spacing = spacing
        self.assets = load_assets()
        
        # Calculate board dimensions
        self.board_width = 10 * (self.cell_size + self.spacing) - self.spacing
        self.board_height = 10 * (self.cell_size + self.spacing) - self.spacing
        
        # Initialize fonts for text rendering
        self.font = pygame.font.SysFont("arial", max(16, self.cell_size // 8))
        self.font_small = pygame.font.SysFont("arial", max(12, self.cell_size // 12))
        self.font_tiny = pygame.font.SysFont("arial", max(6, self.cell_size // 10))
        
        # Initialize theme
        self.theme = ColorTheme.CLASSIC
        self.set_theme_colors()  # Set initial theme colors
    
    def set_theme(self, theme: ColorTheme):
        """Set a new color theme"""
        self.theme = theme
        self.set_theme_colors()
    
    def set_theme_colors(self):
        """Define color schemes based on current theme"""
        if self.theme == ColorTheme.CLASSIC:
            # Classic theme (original colors)
            self.colors = {
                'unknown_bg': (40, 40, 40),
                'unknown_border': (80, 80, 80),
                'discovered_bg': (70, 70, 70),
                'discovered_border': (120, 120, 120),
                'visited_bg': (90, 90, 90),
                'visited_border': (150, 150, 150),
                'text': (200, 200, 200),
                'coordinate_text': (200, 200, 200),
                'perception_text': (0, 0, 0)
            }
        elif self.theme == ColorTheme.DARK:
            # Dark theme
            self.colors = {
                'unknown_bg': (20, 20, 20),
                'unknown_border': (40, 40, 40),
                'discovered_bg': (30, 30, 30),
                'discovered_border': (60, 60, 60),
                'visited_bg': (40, 40, 40),
                'visited_border': (80, 80, 80),
                'text': (180, 180, 180),
                'coordinate_text': (150, 150, 150),
                'perception_text': (220, 220, 220)
            }
        elif self.theme == ColorTheme.PASTEL:
            # Pastel theme
            self.colors = {
                'unknown_bg': (230, 230, 250),
                'unknown_border': (200, 200, 220),
                'discovered_bg': (240, 248, 255),
                'discovered_border': (210, 218, 225),
                'visited_bg': (255, 250, 240),
                'visited_border': (225, 220, 210),
                'text': (70, 70, 70),
                'coordinate_text': (100, 100, 100),
                'perception_text': (50, 50, 50)
            }
        elif self.theme == ColorTheme.FOREST:
            # Forest theme
            self.colors = {
                'unknown_bg': (34, 51, 34),
                'unknown_border': (60, 80, 60),
                'discovered_bg': (68, 85, 68),
                'discovered_border': (90, 110, 90),
                'visited_bg': (102, 119, 102),
                'visited_border': (120, 140, 120),
                'text': (220, 220, 180),
                'coordinate_text': (200, 200, 160),
                'perception_text': (240, 240, 200)
            }

    # ... rest of the class remains the same ...

    def draw_cell(self, x: int, y: int, row: int, col: int, cell_info: dict):
        """Draw a single cell with its state and contents"""
        cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        if cell_info['state'] == CellState.UNKNOWN:
            bg_color = self.colors['unknown_bg']
            border_color = self.colors['unknown_border']
        elif cell_info['state'] == CellState.DISCOVERED:
            bg_color = self.colors['discovered_bg']
            border_color = self.colors['discovered_border']
        elif cell_info['state'] == CellState.VISITED:
            bg_color = self.colors['visited_bg']
            border_color = self.colors['visited_border']
        
        # Draw cell background
        pygame.draw.rect(self.screen, bg_color, cell_rect, border_radius=4)
        pygame.draw.rect(self.screen, border_color, cell_rect, width=1, border_radius=4)
        
        if cell_info['state'] != CellState.UNKNOWN and 'cell' in self.assets:
            cell_image = pygame.transform.scale(self.assets['cell'], (self.cell_size, self.cell_size))
            cell_image.set_alpha(100)
            self.screen.blit(cell_image, (x, y))
        
        if cell_info['state'] != CellState.UNKNOWN:
            self.draw_cell_contents(x, y, cell_info)
        
        # Draw hunter
        if cell_info['is_hunter']:
            self.draw_hunter(x, y)
        
        # Draw arrow if arrow was shot from this cell
        if self.game_state.arrow_used and cell_info['is_hunter']:
            self.draw_arrow(x, y)
        
        # Draw perceptions text
        if cell_info['perceptions'] and cell_info['state'] != CellState.UNKNOWN:
            self.draw_perceptions(x, y, cell_info['perceptions'])
    
    def draw_perceptions(self, x: int, y: int, perceptions: List[str]):
        """Draw perception text on the cell"""
        if not perceptions:
            return
        
        start_text_y = y + self.cell_size - 30
        line_height = 15  # Height between each line of text
        
        for i, perception in enumerate(perceptions):
            color = self.colors['perception_text']  # Use theme color
            
            # Color code perceptions
            if perception == "BREEZE":
                text = "Breeze"
            elif perception == "STENCH":
                text = "Stench"
            elif perception == "GLITTER":
                text = "Glitter"
            else:
                text = perception[0]  # First letter
            
            text_y = start_text_y + (i * line_height)
            
            # Draw text
            text_surface = self.font_small.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = x + self.cell_size // 2
            text_rect.centery = text_y
            
            self.screen.blit(text_surface, text_rect)
    
    def draw_coordinates(self, offset_x, offset_y):
        """Draw coordinate labels around the board"""
        font = pygame.font.SysFont("arial", 16)
        
        # Draw column numbers (top)
        for j in range(10):
            x = offset_x + j * (self.cell_size + self.spacing) + self.cell_size // 2
            y = offset_y - 25
            
            text = font.render(str(j), True, self.colors['coordinate_text'])  # Use theme color
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Draw row numbers (left)
        for i in range(10):
            x = offset_x - 25
            y = offset_y + i * (self.cell_size + self.spacing) + self.cell_size // 2
            
            text = font.render(str(i), True, self.colors['coordinate_text'])  # Use theme color
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)