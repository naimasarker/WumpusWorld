import pygame
import math

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 64, bold=True)
        self.font_button = pygame.font.SysFont("arial", 36)
        self.font_small = pygame.font.SysFont("arial", 24)
        
        # Animation variables
        self.title_pulse = 0
        self.button_hover = {"play": False, "quit": False}
        self.button_scale = {"play": 1.0, "quit": 1.0}
        
    def update_layout(self):
        """Update button positions based on current screen size"""
        screen_width, screen_height = self.screen.get_size()
        
        button_width = min(300, screen_width // 3)
        button_height = 70
        
        # Center buttons on screen
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        self.play_button = pygame.Rect(
            center_x - button_width // 2,
            center_y - 40,
            button_width,
            button_height
        )
        
        self.quit_button = pygame.Rect(
            center_x - button_width // 2,
            center_y + 60,
            button_width,
            button_height
        )

    def draw(self):
        screen_width, screen_height = self.screen.get_size()
        
        for y in range(screen_height):
            ratio = y / screen_height
            r = int(25 + ratio * 35)  # 25-60
            g = int(35 + ratio * 45)  # 35-80
            b = int(60 + ratio * 50)  # 60-110
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (screen_width, y))
        
        title_text = "WUMPUS WORLD"
        title_font = pygame.font.SysFont("arial", 64, bold=True)
        
        title_surf = title_font.render(title_text, True, (255, 193, 7))
        title_rect = title_surf.get_rect(center=(screen_width // 2, screen_height // 4))
        
        shadow_surf = title_font.render(title_text, True, (30, 30, 30))
        shadow_rect = shadow_surf.get_rect(center=(screen_width // 2 + 3, screen_height // 4 + 3))
        self.screen.blit(shadow_surf, shadow_rect)
        
        self.screen.blit(title_surf, title_rect)
        
        subtitle_surf = self.font_small.render("Enter the mysterious world of the Wumpus", True, (220, 220, 220))
        subtitle_rect = subtitle_surf.get_rect(center=(screen_width // 2, screen_height // 4 + 80))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        self.update_layout()
        
        self.draw_button(self.play_button, "Play Game", "play", (76, 175, 80), (102, 187, 106))
        self.draw_button(self.quit_button, "Quit", "quit", (244, 67, 54), (229, 115, 115))
        
        # self.draw_decorations()

    
    def draw_button(self, rect, text, button_id, base_color, hover_color):
        """Draw a button with hover and scale effects"""
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = rect.collidepoint(mouse_pos)
        
        # Update hover state
        self.button_hover[button_id] = is_hovering
        
        # Smooth scaling animation
        target_scale = 1.05 if is_hovering else 1.0
        self.button_scale[button_id] += (target_scale - self.button_scale[button_id]) * 0.1
        
        # Calculate scaled rect
        scale = self.button_scale[button_id]
        scaled_width = int(rect.width * scale)
        scaled_height = int(rect.height * scale)
        scaled_rect = pygame.Rect(
            rect.centerx - scaled_width // 2,
            rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Choose color based on hover state
        color = hover_color if is_hovering else base_color
        
        # Draw button shadow
        shadow_rect = scaled_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Draw main button
        pygame.draw.rect(self.screen, color, scaled_rect, border_radius=12)
        
        # Draw button border
        border_color = (255, 255, 255, 150) if is_hovering else (255, 255, 255, 80)
        pygame.draw.rect(self.screen, border_color, scaled_rect, width=2, border_radius=12)
        
        # Draw button text
        text_color = (255, 255, 255) if is_hovering else (240, 240, 240)
        text_surf = self.font_button.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        self.screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return "play"
            elif self.quit_button.collidepoint(event.pos):
                return "quit"
        return None


class GameUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 32, bold=True)
        self.font_text = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)
        
        # Game state
        self.score = 0
        self.moves = 0
        self.arrows = 1
        self.gold_collected = 0
        
        # UI elements
        self.sidebar_width = 280
        self.margin = 20
        
    def get_board_area(self):
        """Get the area available for the game board"""
        screen_width, screen_height = self.screen.get_size()
        board_width = screen_width - self.sidebar_width - self.margin * 3
        board_height = screen_height - self.margin * 2
        
        # Make it square
        board_size = min(board_width, board_height)
        
        return pygame.Rect(self.margin, self.margin, board_size, board_size)
    
    def draw_sidebar(self):
        """Draw the right sidebar with game information"""
        screen_width, screen_height = self.screen.get_size()
        
        # Sidebar background
        sidebar_rect = pygame.Rect(
            screen_width - self.sidebar_width - self.margin,
            self.margin,
            self.sidebar_width,
            screen_height - self.margin * 2
        )
        
        # Gradient background for sidebar
        for y in range(sidebar_rect.height):
            ratio = y / sidebar_rect.height
            r = int(45 + ratio * 15)
            g = int(50 + ratio * 20)
            b = int(65 + ratio * 25)
            color = (r, g, b)
            pygame.draw.line(
                self.screen, 
                color, 
                (sidebar_rect.x, sidebar_rect.y + y), 
                (sidebar_rect.right, sidebar_rect.y + y)
            )
        
        # Border
        pygame.draw.rect(self.screen, (100, 100, 100), sidebar_rect, width=2, border_radius=10)
        
        # Title
        title_surf = self.font_title.render("GAME STATUS", True, (255, 235, 59))
        title_rect = title_surf.get_rect(centerx=sidebar_rect.centerx, y=sidebar_rect.y + 20)
        self.screen.blit(title_surf, title_rect)
        
        # Game stats
        y_offset = 80
        stats = [
            ("Score", self.score, (76, 175, 80)),
            ("Moves", self.moves, (33, 150, 243)),
            ("Arrows", self.arrows, (255, 152, 0)),
            ("Gold", self.gold_collected, (255, 215, 0))
        ]
        
        for label, value, color in stats:
            # Label
            label_surf = self.font_text.render(f"{label}:", True, (220, 220, 220))
            self.screen.blit(label_surf, (sidebar_rect.x + 20, sidebar_rect.y + y_offset))
            
            # Value with colored background
            value_surf = self.font_text.render(str(value), True, (255, 255, 255))
            value_bg = pygame.Rect(sidebar_rect.right - 80, sidebar_rect.y + y_offset - 5, 60, 30)
            pygame.draw.rect(self.screen, color, value_bg, border_radius=5)
            value_rect = value_surf.get_rect(center=value_bg.center)
            self.screen.blit(value_surf, value_rect)
            
            y_offset += 50
        
        # Controls section
        controls_y = sidebar_rect.y + 350
        controls_title = self.font_text.render("CONTROLS", True, (255, 235, 59))
        self.screen.blit(controls_title, (sidebar_rect.x + 20, controls_y))
        
        controls = [
            "Arrow Keys: Move",
            "Space: Shoot Arrow",
            "G: Grab Gold",
            "ESC: Main Menu"
        ]
        
        for i, control in enumerate(controls):
            control_surf = self.font_small.render(control, True, (200, 200, 200))
            self.screen.blit(control_surf, (sidebar_rect.x + 20, controls_y + 40 + i * 25))
        
        # Back to menu button
        menu_button = pygame.Rect(
            sidebar_rect.x + 20,
            sidebar_rect.bottom - 80,
            sidebar_rect.width - 40,
            50
        )
        
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = menu_button.collidepoint(mouse_pos)
        button_color = (244, 67, 54) if is_hovering else (200, 50, 50)
        
        pygame.draw.rect(self.screen, button_color, menu_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_button, width=2, border_radius=8)
        
        menu_text = self.font_text.render("Main Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_rect)
        
        return menu_button
    
    def handle_event(self, event):
        """Handle UI events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            menu_button = self.draw_sidebar()  # Get button rect
            if menu_button.collidepoint(event.pos):
                return "menu"
        return None