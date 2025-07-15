import pygame
import random
from dataclasses import dataclass
from typing import List, Tuple
import pygame.gfxdraw
import sys
from Map import *
from Agent import *
from Graphic import *
from Algorithms import *

@dataclass
class GameColors:
    PRIMARY = (255, 99, 71)  # Tomato red
    SECONDARY = (255, 182, 193)  # Light pink
    ACCENT = (255, 215, 0)  # Gold for contrast
    BACKGROUND = (30, 50, 30)  # Deep green
    TEXT_PRIMARY = (255, 255, 255)  # White for readability
    TEXT_SECONDARY = (180, 180, 180)
    BUTTON_HOVER = (255, 105, 97)  # Coral
    BUTTON_ACTIVE = (200, 50, 50)  # Dark red
    TRANSPARENT = (0, 0, 0, 0)
    LIGHT_ACCENT = (255, 230, 180)
class ParticleSystem:
    def __init__(self):
        self.particles: List[dict] = []
        
    def create_particle(self, x: int, y: int, color: Tuple[int, int, int]):
        self.particles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-1, 1),
            'dy': random.uniform(-1, 1),
            'lifetime': random.uniform(0.5, 2.0),
            'color': color,
            'size': random.uniform(2, 4)
        })
    
    def update(self, dt: float):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= dt
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / 2.0))
            color = (*particle['color'], alpha)
            pygame.gfxdraw.filled_circle(
                screen,
                int(particle['x']),
                int(particle['y']),
                int(particle['size']),
                color
            )

class AnimatedButton:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hover = False
        self.scale = 1.0
        self.target_scale = 1.0
        
    def update(self, mouse_pos: Tuple[int, int], dt: float):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.1 if self.hover else 1.0
        self.scale += (self.target_scale - self.scale) * dt * 10
        
    def draw(self, screen: pygame.Surface):
        scaled_rect = self.rect.copy()
        scaled_rect.width *= self.scale
        scaled_rect.height *= self.scale
        scaled_rect.center = self.rect.center
        
        # Draw button background with gradient
        gradient_rect = scaled_rect.copy()
        for i in range(scaled_rect.height):
            progress = i / scaled_rect.height
            if self.hover:
                color = tuple(map(lambda x, y: int(x + (y - x) * progress),
                                GameColors.BUTTON_ACTIVE,
                                GameColors.BUTTON_HOVER))
            else:
                color = tuple(map(lambda x, y: int(x + (y - x) * progress),
                                GameColors.PRIMARY,
                                GameColors.SECONDARY))
            pygame.draw.line(screen, color,
                           (scaled_rect.left, scaled_rect.top + i),
                           (scaled_rect.right, scaled_rect.top + i))
        
        # Draw text
        text_surf = self.font.render(self.text, True, GameColors.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)
        
        # Draw border
        pygame.draw.rect(screen, GameColors.ACCENT, scaled_rect, 2, border_radius=10)

class EnhancedGraphic(Graphic):
    def __init__(self):
        super().__init__()
        self.particles = ParticleSystem()
        self.buttons = []
        self.score_animation = {'current': 0, 'target': 0}
        self.setup_buttons()
        self.action_text = ""  # Store action feedback
        
    def setup_buttons(self):
        self.buttons = []
        # Grid layout for MAP buttons (2x3 grid)
        grid_x_start = (SCREEN_WIDTH - 600) // 2  # 600 = 3 * 200 (button width)
        grid_y_start = 150
        button_width = 200
        button_height = 80
        for i in range(5):  # MAP 1 to MAP 5
            row = i // 3
            col = i % 3
            x = grid_x_start + col * (button_width + 20)
            y = grid_y_start + row * (button_height + 20)
            self.buttons.append(
                AnimatedButton(x, y, button_width, button_height, f"MAP {i+1}", self.font)
            )
        # Additional buttons below grid
        extra_buttons = ["CUSTOM MAP", "CREATE MAP", "EXIT"]
        for i, text in enumerate(extra_buttons):
            x = (SCREEN_WIDTH - (len(extra_buttons) * (button_width + 20) - 20)) // 2 + i * (button_width + 20)
            y = grid_y_start + 2 * (button_height + 20) + 50
            self.buttons.append(
                AnimatedButton(x, y, button_width, button_height, text, self.font)
            )
    
    def home_draw(self):
        # Create atmospheric background with new color
        self.screen.fill(GameColors.BACKGROUND)
        
        # Draw animated particles
        self.particles.update(1/60)
        for _ in range(2):
            self.particles.create_particle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                GameColors.ACCENT
            )
        self.particles.draw(self.screen)
        
        # Draw title
        title = self.victory.render("WUMPUS WORLD", True, GameColors.ACCENT)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH//2, top=50)
        self.screen.blit(title, title_rect)
        
        # Draw animated buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos, 1/60)
            button.draw(self.screen)
    def running_draw(self):
        self.screen.fill(GameColors.BACKGROUND)
        self.map.draw(self.screen)
        
        # Animate score
        score = self.agent.get_score()
        self.score_animation['target'] = score
        self.score_animation['current'] += (self.score_animation['target'] - 
                                        self.score_animation['current']) * 0.1
        
        # Draw modern HUD (score only)
        self._draw_hud()
        
        # Draw action text at the bottom in white
        if self.action_text:
            print(f"Rendering action text: {self.action_text} with color (255, 255, 255)")  # Debug message
            action_surf = self.noti.render(self.action_text, True, (255, 255, 255))  # Explicitly white
            action_rect = action_surf.get_rect(bottom=SCREEN_HEIGHT - 10, centerx=SCREEN_WIDTH // 2)
            self.screen.blit(action_surf, action_rect)
    def _draw_hud(self):
        # Floating score text with shadow effect
        score_text = f"SCORE: {int(self.score_animation['current']):,}"
        score_surf = self.font.render(score_text, True, GameColors.TEXT_PRIMARY)
        
        # Create shadow effect
        shadow_surf = self.font.render(score_text, True, (50, 50, 50))
        shadow_x, shadow_y = SCREEN_WIDTH - 260, 20
        
        # Blit shadow with offset
        self.screen.blit(shadow_surf, (shadow_x + 2, shadow_y + 2))
        
        # Blit main score text
        self.screen.blit(score_surf, (shadow_x, shadow_y))
    
    def win_draw(self):
        self.screen.fill(GameColors.BACKGROUND)
        # self.screen.fill((135, 206, 235))
        
        # Create victory/defeat effects
        for _ in range(5):
            self.particles.create_particle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                GameColors.ACCENT
            )
        self.particles.update(1/60)
        self.particles.draw(self.screen)
        
        # Draw victory/defeat message
        if self.state == WIN:
            message = 'VICTORY!!!'
            color = GameColors.ACCENT
        else:
            message = 'TRY BEST!!!'
            color = GameColors.TEXT_SECONDARY
            
        text = self.victory.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        
        # Add glow effect
        glow_surf = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        glow_color = (*color, 100)
        glow_text = self.victory.render(message, True, glow_color)
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_surf.blit(glow_text, offset)
        self.screen.blit(glow_surf, text_rect)
        self.screen.blit(text, text_rect)
        
        # Draw animated score
        score = self.agent.get_score()
        score_text = self.victory.render(f'Score: {score}', True, GameColors.TEXT_PRIMARY)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Add return to menu button
        return_button = AnimatedButton(
            SCREEN_WIDTH//4, 
            3*SCREEN_HEIGHT//4,
            SCREEN_WIDTH//2,
            50,
            "Return to Menu",
            self.font
        )
        return_button.update(pygame.mouse.get_pos(), 1/60)
        return_button.draw(self.screen)



def display_action(self, action: Algorithms.Action):
    
    i, j = self.agent.get_pos()
    screen_x = j * 2 + 2
    screen_y = i * 2 + 2
    
    if action in [Algorithms.Action.MOVE_FORWARD, Algorithms.Action.GRAB_GOLD]:
        for _ in range(10):
            self.particles.create_particle(screen_x, screen_y, GameColors.ACCENT)
        self.action_text = "Grabbed Gold!" if action == Algorithms.Action.GRAB_GOLD else "Moved Forward"
    elif action == Algorithms.Action.KILL_WUMPUS:
        for _ in range(10):
            self.particles.create_particle(screen_x, screen_y, GameColors.ACCENT)
        self.action_text = "Killed Wumpus!"
    elif action == Algorithms.Action.SHOOT:
        self.action_text = "Shot Arrow!"
    
    self.running_draw()
    pygame.display.update()
    
    super().display_action(action)