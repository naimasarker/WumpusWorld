import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 64, bold=True)
        self.font_button = pygame.font.SysFont("arial", 36)

        # Define buttons
        self.play_button = pygame.Rect(275, 300, 200, 60)
        self.quit_button = pygame.Rect(275, 400, 200, 60)

    def draw(self):
        self.screen.fill((25, 25, 25))

        # Draw title
        title_surf = self.font_title.render("WUMPUS WORLD", True, (255, 195, 0))
        title_rect = title_surf.get_rect(center=(375, 120))
        self.screen.blit(title_surf, title_rect)

        # Draw buttons
        pygame.draw.rect(self.screen, (101, 67, 133), self.play_button, border_radius=8)
        pygame.draw.rect(self.screen, (101, 67, 133), self.quit_button, border_radius=8)

        play_text = self.font_button.render("Play Game", True, (255, 255, 255))
        quit_text = self.font_button.render("Quit", True, (255, 255, 255))

        self.screen.blit(play_text, play_text.get_rect(center=self.play_button.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return "play"
            elif self.quit_button.collidepoint(event.pos):
                return "quit"
        return None
