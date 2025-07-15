from typing import List, Tuple

class Board:
    def __init__(self, grid: List[List[List[str]]],
                 gold_positions: List[Tuple[int, int]],
                 pit_positions: List[Tuple[int, int]],
                 wumpus_positions: List[Tuple[int, int]]):
        self.grid = grid  
        self.gold_positions = gold_positions
        self.pit_positions = pit_positions
        self.wumpus_positions = wumpus_positions

    def get_cell_objects(self, row: int, col: int) -> List[str]:
        return self.grid[row][col]

    def print_board(self):
        for row in self.grid:
            print("".join([cell[0] if cell else '-' for cell in row]))
    
    def write_board_to_file(self, output_path: str):
        with open(output_path, 'w') as f:
            for row in self.grid:
                line = "".join([cell[0] if cell else '-' for cell in row])
                f.write(line + '\n')

def load_board_from_file(file_path: str) -> Board:
    grid = []
    gold_positions = []
    pit_positions = []
    wumpus_positions = []

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) != 10:
        raise ValueError("Board file must have exactly 10 lines")

    for i, line in enumerate(lines):
        if len(line) != 10:
            raise ValueError(f"Line {i+1} must have exactly 10 characters")

        row = []
        for j, char in enumerate(line):
            cell = []
            if char in ['G', 'P', 'W']:
                cell.append(char)
                if char == 'G':
                    gold_positions.append((i, j))
                elif char == 'P':
                    pit_positions.append((i, j))
                elif char == 'W':
                    wumpus_positions.append((i, j))
            row.append(cell)
        grid.append(row)

    return Board(grid, gold_positions, pit_positions, wumpus_positions)
