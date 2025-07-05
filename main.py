import pygame
from BoardLoader import load_board_from_file
from BoardRenderer import BoardRenderer
from UI import Menu

pygame.init()

screen = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
pygame.display.set_caption("Wumpus World")

state = "menu"
menu = Menu(screen)

board = None
renderer = None

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            action = menu.handle_event(event)
            if action == "play":
                # Load board and renderer
                board = load_board_from_file("Assets/Input/map_1.txt")
                renderer = BoardRenderer(screen, board)

                print("Gold:", board.gold_positions)
                print("Pits:", board.pit_positions)
                print("Wumpus:", board.wumpus_positions)

                state = "play"
            elif action == "quit":
                running = False

    # Draw based on state
    if state == "menu":
        menu.draw()
    elif state == "play":
        screen.fill((30, 30, 30))
        renderer.draw_board()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()