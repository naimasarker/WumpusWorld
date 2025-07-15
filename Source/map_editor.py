import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 60
MARGIN = 2
GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH + 200  # Extra space for legend
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (180, 180, 180)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
BROWN = (160, 82, 45)
LIGHT_BLUE = (160, 160, 255)
LIGHT_RED = (255, 160, 160)

# Object keys
object_keys = {
    "A": "Agent",
    "P": "Pit", 
    "W": "Wumpus",
    "G": "Gold",
    "B": "Breeze",
    "S": "Stench",
    "-": "Empty",
    ".": "Unknown"
}
object_cycle = list(object_keys.keys())

# Create grid
grid = [["." for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Map Editor - Use Mouse to Click, Tab to Change Mode")

# Fonts
font = pygame.font.SysFont("arial", 16)
big_font = pygame.font.SysFont("arial", 20, bold=True)
small_font = pygame.font.SysFont("arial", 14)

def draw_grid():
    screen.fill(WHITE)
    
    # Draw the grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN)
            pygame.draw.rect(screen, LIGHTGREY, rect)
            val = grid[row][col]
            color = BLACK
            
            # Set background color based on cell type
            if val == "A":
                color = GREEN
            elif val == "P":
                color = RED
            elif val == "W":
                color = BLUE
            elif val == "G":
                color = YELLOW
            elif val == "B":
                color = LIGHT_BLUE
            elif val == "S":
                color = LIGHT_RED
            elif val == "-":
                color = WHITE
            elif val == ".":
                color = LIGHTGREY
                
            pygame.draw.rect(screen, color, rect)
            
            # Draw text
            text = font.render(val, True, BLACK)
            screen.blit(text, text.get_rect(center=rect.center))
    
    # Draw legend
    legend_x = CELL_SIZE * GRID_WIDTH + 20
    legend_y = 20
    
    pygame.draw.rect(screen, LIGHTGREY, (legend_x - 10, legend_y - 10, 180, 300))
    
    legend_title = big_font.render("Legend:", True, BLACK)
    screen.blit(legend_title, (legend_x, legend_y))
    legend_y += 30
    
    for i, (key, name) in enumerate(object_keys.items()):
        color = WHITE
        if key == "A":
            color = GREEN
        elif key == "P":
            color = RED
        elif key == "W":
            color = BLUE
        elif key == "G":
            color = YELLOW
        elif key == "B":
            color = LIGHT_BLUE
        elif key == "S":
            color = LIGHT_RED
        elif key == "-":
            color = WHITE
        elif key == ".":
            color = LIGHTGREY
            
        # Draw small colored box
        small_rect = pygame.Rect(legend_x, legend_y + i * 25, 20, 20)
        pygame.draw.rect(screen, color, small_rect)
        pygame.draw.rect(screen, BLACK, small_rect, 1)
        
        # Draw key and name
        key_text = small_font.render(f"{key} - {name}", True, BLACK)
        screen.blit(key_text, (legend_x + 25, legend_y + i * 25 + 3))
    
    # Draw current mode
    current_mode_y = legend_y + len(object_keys) * 25 + 20
    current_text = big_font.render(f"Current: {object_cycle[current_key_idx]}", True, BLACK)
    screen.blit(current_text, (legend_x, current_mode_y))
    
    # Draw instructions
    instructions = [
        "Controls:",
        "Left Click: Place object",
        "Tab: Change mode",
        "S: Save map",
        "C: Clear grid", 
        "Esc: Cancel"
    ]
    
    instr_y = current_mode_y + 40
    for instruction in instructions:
        instr_text = small_font.render(instruction, True, BLACK)
        screen.blit(instr_text, (legend_x, instr_y))
        instr_y += 18
    
    
    pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
    text = big_font.render("Press S to Save as Custom Map | C to Clear | Esc to Cancel", True, WHITE)
    screen.blit(text, (20, SCREEN_HEIGHT - 60))

def save_map():
    folder = os.path.join("Assets", "Input")
    output_folder = os.path.join("Assets", "Output")
    os.makedirs(folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Create a copy of the grid for output
    output_grid = [row[:] for row in grid]

    # Dictionary to track adjacent effects
    adj_effects = {}
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if output_grid[row][col] == "W":
                # Add stench (S) to adjacent cells
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH:
                        pos = (new_row, new_col)
                        adj_effects[pos] = adj_effects.get(pos, "") + "S"
            elif output_grid[row][col] == "P":
                # Add breeze (B) to adjacent cells
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH:
                        pos = (new_row, new_col)
                        adj_effects[pos] = adj_effects.get(pos, "") + "B"

    # Apply effects to the grid
    for (row, col), effects in adj_effects.items():
        current = output_grid[row][col]
        if current in ["A", "P", "G", "W", "-", "B", "S"]:
            # Combine effects without duplicating
            unique_effects = "".join(sorted(set(effects)))
            if current == ".":
                output_grid[row][col] = unique_effects
            else:
                output_grid[row][col] = current + unique_effects
        elif current == ".":
            output_grid[row][col] = effects

    # Replace all remaining '.' with '-'
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if output_grid[row][col] == ".":
                output_grid[row][col] = "-"

    # Save as custom_map.txt (will overwrite if exists)
    map_path = os.path.join(folder, "custom_map.txt")
    out_path = os.path.join(output_folder, "custom_result.txt")

    with open(map_path, "w") as f:
        f.write(f"{GRID_HEIGHT}\n")
        for row in output_grid:
            # Join cells with exactly one dot
            formatted_row = ".".join(row)
            f.write(formatted_row + "\n")

    # Create empty output file
    with open(out_path, "w") as f:
        f.write("")

    print(f"Map saved as custom_map.txt in {map_path}")
    print("Format:")
    for row in output_grid:
        print(".".join(row))

def clear_grid():
    global grid
    grid = [["." for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Main loop
running = True
current_key_idx = 0

while running:
    draw_grid()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_map()
                running = False
            elif event.key == pygame.K_c:
                clear_grid()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_TAB:
                current_key_idx = (current_key_idx + 1) % len(object_cycle)
                print(f"Current mode: {object_cycle[current_key_idx]} ({object_keys[object_cycle[current_key_idx]]})")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if row < GRID_HEIGHT and col < GRID_WIDTH:
                    grid[row][col] = object_cycle[current_key_idx]
                    print(f"Placed {object_cycle[current_key_idx]} at ({row}, {col})")

pygame.quit()
sys.exit()