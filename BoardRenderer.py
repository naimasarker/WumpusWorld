import pygame
from typing import List
from assets import load_assets
from BoardLoader import Board
from GameState import GameState, CellState

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
        self.font = pygame.font.SysFont("arial", max(16, self.cell_size // 8))  # Bigger font
        self.font_small = pygame.font.SysFont("arial", max(12, self.cell_size // 12))
        self.font_tiny = pygame.font.SysFont("arial", max(6, self.cell_size // 10))
    
    def get_board_center_offset(self):
        """Calculate offset to center the board in the available space"""
        screen_width, screen_height = self.screen.get_size()
        
        offset_x = (screen_width - self.board_width) // 2
        offset_y = (screen_height - self.board_height) // 2
        
        return offset_x, offset_y

    def draw_board(self):
        """Draw the game board with proper centering and cell states"""
        offset_x, offset_y = self.get_board_center_offset()
        
        # Draw background grid
        for i in range(10):
            for j in range(10):
                x = offset_x + j * (self.cell_size + self.spacing)
                y = offset_y + i * (self.cell_size + self.spacing)

                # Get cell display info
                cell_info = self.game_state.get_cell_display_info(i, j)
                
                # Draw cell based on state
                self.draw_cell(x, y, i, j, cell_info)
        
        # Draw coordinate labels 
        self.draw_coordinates(offset_x, offset_y)
    
    def draw_cell(self, x: int, y: int, row: int, col: int, cell_info: dict):
        """Draw a single cell with its state and contents"""
        cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        if cell_info['state'] == CellState.UNKNOWN:
            bg_color = (40, 40, 40)  
            border_color = (80, 80, 80)
        elif cell_info['state'] == CellState.DISCOVERED:
            bg_color = (70, 70, 70)  
            border_color = (120, 120, 120)
        elif cell_info['state'] == CellState.VISITED:
            bg_color = (90, 90, 90)  
            border_color = (150, 150, 150)
        
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
    
    def draw_cell_contents(self, x: int, y: int, cell_info: dict):
        """Draw the contents of a discovered cell"""
        # Draw pit
        if cell_info['has_pit'] and 'pit' in self.assets:
            pit_image = pygame.transform.scale(self.assets['pit'], (self.cell_size, self.cell_size))
            self.screen.blit(pit_image, (x, y))
        
        # Draw gold
        elif cell_info['has_gold'] and 'gold' in self.assets:
            gold_image = pygame.transform.scale(self.assets['gold'], (self.cell_size, self.cell_size))
            self.screen.blit(gold_image, (x, y))
        
        # Draw wumpus
        elif cell_info['has_wumpus'] and 'wumpus' in self.assets:
            wumpus_image = pygame.transform.scale(self.assets['wumpus'], (self.cell_size, self.cell_size))
            self.screen.blit(wumpus_image, (x, y))
    
    def draw_hunter(self, x: int, y: int):
        """Draw the hunter at the given position using hunter image"""

        hunter_direction = self.game_state.get_hunter_direction()
        
        # Select appropriate hunter image based on direction
        hunter_image_key = f"hunter_{hunter_direction.lower()}"
        
        if hunter_image_key in self.assets:
            hunter_image = pygame.transform.scale(self.assets[hunter_image_key], (self.cell_size, self.cell_size))
            self.screen.blit(hunter_image, (x, y))
        else:
            center_x = x + self.cell_size // 2
            center_y = y + self.cell_size // 2
            radius = max(8, self.cell_size // 6)
            
            pygame.draw.circle(self.screen, (0, 150, 255), (center_x, center_y), radius)
            pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), radius, 2)
            
            arrow_size = radius // 2
            if hunter_direction == "UP":
                points = [
                    (center_x, center_y - arrow_size),
                    (center_x - arrow_size//2, center_y + arrow_size//2),
                    (center_x + arrow_size//2, center_y + arrow_size//2)
                ]
            elif hunter_direction == "DOWN":
                points = [
                    (center_x, center_y + arrow_size),
                    (center_x - arrow_size//2, center_y - arrow_size//2),
                    (center_x + arrow_size//2, center_y - arrow_size//2)
                ]
            elif hunter_direction == "LEFT":
                points = [
                    (center_x - arrow_size, center_y),
                    (center_x + arrow_size//2, center_y - arrow_size//2),
                    (center_x + arrow_size//2, center_y + arrow_size//2)
                ]
            else:  # RIGHT
                points = [
                    (center_x + arrow_size, center_y),
                    (center_x - arrow_size//2, center_y - arrow_size//2),
                    (center_x - arrow_size//2, center_y + arrow_size//2)
                ]
            
            pygame.draw.polygon(self.screen, (255, 255, 255), points)
    
    def draw_arrow(self, x: int, y: int):
        """Draw arrow indicator when arrow is used"""
        hunter_direction = self.game_state.get_hunter_direction()
        arrow_image_key = f"arrow_{hunter_direction.lower()}"
        
        # Draw arrow image if available
        if arrow_image_key in self.assets:
            # Draw arrow smaller and in corner
            arrow_size = self.cell_size // 3
            arrow_image = pygame.transform.scale(self.assets[arrow_image_key], (arrow_size, arrow_size))
            # Position arrow in top-right corner
            arrow_x = x + self.cell_size - arrow_size - 2
            arrow_y = y + 2
            self.screen.blit(arrow_image, (arrow_x, arrow_y))
        else:
            # Fallback arrow indicator
            center_x = x + self.cell_size - 10
            center_y = y + 10
            pygame.draw.circle(self.screen, (255, 255, 0), (center_x, center_y), 5)
            pygame.draw.circle(self.screen, (0, 0, 0), (center_x, center_y), 5, 2)

    def draw_perceptions(self, x: int, y: int, perceptions: List[str]):
        """Draw perception text on the cell"""
        if not perceptions:
            return
        
        start_text_y = y + self.cell_size - 30
        line_height = 15  # Height between each line of text
        
        for i, perception in enumerate(perceptions):
            color = (0, 0, 0)
            
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
            
            text = font.render(str(j), True, (200, 200, 200))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Draw row numbers (left)
        for i in range(10):
            x = offset_x - 25
            y = offset_y + i * (self.cell_size + self.spacing) + self.cell_size // 2
            
            text = font.render(str(i), True, (200, 200, 200))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def get_cell_from_mouse(self, mouse_pos):
        """Get the board cell coordinates from mouse position"""
        offset_x, offset_y = self.get_board_center_offset()
        
        # Adjust mouse position relative to board
        rel_x = mouse_pos[0] - offset_x
        rel_y = mouse_pos[1] - offset_y
        
        if rel_x < 0 or rel_y < 0 or rel_x >= self.board_width or rel_y >= self.board_height:
            return None
        
        col = rel_x // (self.cell_size + self.spacing)
        row = rel_y // (self.cell_size + self.spacing)
        
        if 0 <= row < 10 and 0 <= col < 10:
            return (row, col)
        
        return None
    
    def highlight_cell(self, row, col, color=(255, 255, 0), width=3):
        """Highlight a specific cell with a colored border"""
        offset_x, offset_y = self.get_board_center_offset()
        
        x = offset_x + col * (self.cell_size + self.spacing)
        y = offset_y + row * (self.cell_size + self.spacing)
        
        cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, cell_rect, width=width, border_radius=4)