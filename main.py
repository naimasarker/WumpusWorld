import pygame
from BoardLoader import load_board_from_file
from BoardRenderer import BoardRenderer
from GameState import GameState
from UI import Menu, GameUI

pygame.init()

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Wumpus World")

pygame.display.set_mode((1000, 700), pygame.RESIZABLE)

state = "menu"
menu = Menu(screen)
game_ui = GameUI(screen)

board = None
game_state = None
renderer = None

clock = pygame.time.Clock()
running = True

def handle_game_input(event):
    """Handle game input with proper movement and arrow shooting logic"""
    if not game_state or not game_state.hunter_alive:
        return
    
    if event.type == pygame.KEYDOWN:
        # Movement keys 
        if event.key == pygame.K_UP:
            game_state.try_move_or_turn("UP")
        elif event.key == pygame.K_DOWN:
            game_state.try_move_or_turn("DOWN")
        elif event.key == pygame.K_LEFT:
            game_state.try_move_or_turn("LEFT")
        elif event.key == pygame.K_RIGHT:
            game_state.try_move_or_turn("RIGHT")
        
        # Action keys
        elif event.key == pygame.K_g:
            game_state.grab_gold()
        elif event.key == pygame.K_SPACE:
            # Shoot arrow in current facing direction
            game_state.shoot_arrow()
        
        # Arrow shooting in specific directions 
        elif event.key == pygame.K_s:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                print("Hold Shift + S and press arrow key to shoot in that direction")
            else:
                game_state.shoot_arrow()
        
        elif event.key == pygame.K_d:
            game_ui.discovery_mode = True
    
    elif event.type == pygame.MOUSEBUTTONDOWN and hasattr(game_ui, 'discovery_mode') and game_ui.discovery_mode:
        if renderer:
            cell_pos = renderer.get_cell_from_mouse(event.pos)
            if cell_pos:
                row, col = cell_pos
                game_state.discover_cell(row, col)
                print(f"Discovered cell ({row}, {col})")
        game_ui.discovery_mode = False

def handle_directional_shooting(event):
    """Handle directional arrow shooting with Shift modifier"""
    if not game_state or not game_state.hunter_alive:
        return
    
    if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if event.key == pygame.K_UP:
                game_state.shoot_arrow("UP")
                print("Shooting arrow UP")
            elif event.key == pygame.K_DOWN:
                game_state.shoot_arrow("DOWN")
                print("Shooting arrow DOWN")
            elif event.key == pygame.K_LEFT:
                game_state.shoot_arrow("LEFT")
                print("Shooting arrow LEFT")
            elif event.key == pygame.K_RIGHT:
                game_state.shoot_arrow("RIGHT")
                print("Shooting arrow RIGHT")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            width = max(1000, event.w)
            height = max(700, event.h)
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            
            menu.screen = screen
            game_ui.screen = screen
            
            if renderer:
                renderer.screen = screen

        if state == "menu":
            action = menu.handle_event(event)
            if action == "play":
                # Load board and create game state
                board = load_board_from_file("Assets/Input/map_1.txt")
                game_state = GameState(board)
                
                # Get the actual board area for proper sizing
                board_area = game_ui.get_board_area()
                cell_size = min(board_area.width // 12, board_area.height // 12)  # 12 for 10 cells + spacing
                
                renderer = BoardRenderer(screen, board, game_state, cell_size=cell_size)

                print("Game Started!")
                print("Gold:", board.gold_positions)
                print("Pits:", board.pit_positions)
                print("Wumpus:", board.wumpus_positions)
                print("Hunter starts at:", game_state.hunter_pos)
                print("\nControls:")
                print("Arrow keys: Move/Turn hunter")
                print("  - First press: Turn to face direction")
                print("  - Second press: Move in that direction")
                print("G: Grab gold")
                print("Space: Shoot arrow in current facing direction")
                print("Shift + Arrow: Shoot arrow in specific direction")
                print("D + Click: Discover cell (for testing)")
                print("ESC: Back to menu")

                state = "play"
            elif action == "quit":
                running = False
        
        elif state == "play":
            action = game_ui.handle_event(event)
            if action == "menu":
                state = "menu"
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"
            
            handle_game_input(event)
            handle_directional_shooting(event)
            
            if game_state:
                stats = game_state.get_game_stats()
                game_ui.score = stats['score']
                game_ui.moves = stats['moves']
                game_ui.arrows = stats['arrows']
                game_ui.gold_collected = stats['gold_collected']

    if state == "menu":
        menu.draw()
    elif state == "play":
        screen.fill((25, 25, 25))
        
        board_area = game_ui.get_board_area()
        
        board_surface = screen.subsurface(board_area)
        
        original_screen = renderer.screen
        renderer.screen = board_surface
        
        board_surface.fill((35, 35, 35))
        
        pygame.draw.rect(screen, (100, 100, 100), board_area, width=2, border_radius=8)
        
        renderer.draw_board()
        
        renderer.screen = original_screen
        
        game_ui.draw_sidebar()
        
        if game_state and not game_state.hunter_alive:
            font = pygame.font.SysFont("arial", 48, bold=True)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(screen.get_width()//2, 100))
            
            bg_rect = game_over_rect.copy()
            bg_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect, border_radius=10)
            screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()