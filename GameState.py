from typing import List, Tuple, Set
from enum import Enum
from BoardLoader import Board

class CellState(Enum):
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    VISITED = "visited"

class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.hunter_pos = (9, 0)  # Bottom-left corner (row 9, col 0)
        self.hunter_direction = "UP"  # Default direction
        self.hunter_alive = True
        self.has_gold = False
        self.arrow_used = False
        
        # Track dead wumpus positions instead of single boolean
        self.dead_wumpus_positions = set()
        
        self.score = 0
        self.moves = 0
        
        # Cell states - initially all unknown except hunter's starting position
        self.cell_states = {}
        for i in range(10):
            for j in range(10):
                self.cell_states[(i, j)] = CellState.UNKNOWN
        
        self.cell_states[(9, 0)] = CellState.VISITED
        
        self.discovered_cells = set()
        self.visited_cells = set()
        self.visited_cells.add((9, 0))
        
        # Perceptions for each cell
        self.perceptions = {} 
        
        self.update_perceptions(9, 0)
    
    def get_hunter_direction(self) -> str:
        """Get current hunter direction"""
        return self.hunter_direction
    
    def set_hunter_direction(self, direction: str):
        """Set hunter direction (UP, DOWN, LEFT, RIGHT)"""
        self.hunter_direction = direction.upper()
    
    def get_adjacent_cells(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all adjacent cells (up, down, left, right)"""
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 10 and 0 <= new_col < 10:
                adjacent.append((new_row, new_col))
        
        return adjacent
    
    def has_pit_adjacent(self, row: int, col: int) -> bool:
        """Check if there's a pit adjacent to this cell"""
        adjacent_cells = self.get_adjacent_cells(row, col)
        for adj_row, adj_col in adjacent_cells:
            if (adj_row, adj_col) in self.board.pit_positions:
                return True
        return False
    
    def has_wumpus_adjacent(self, row: int, col: int) -> bool:
        """Check if there's a LIVING wumpus adjacent to this cell"""
        adjacent_cells = self.get_adjacent_cells(row, col)
        for adj_row, adj_col in adjacent_cells:
            # Check if wumpus exists and is NOT dead
            if ((adj_row, adj_col) in self.board.wumpus_positions and 
                (adj_row, adj_col) not in self.dead_wumpus_positions):
                return True
        return False
    
    def is_wumpus_alive(self, row: int, col: int) -> bool:
        """Check if wumpus at given position is alive"""
        return ((row, col) in self.board.wumpus_positions and 
                (row, col) not in self.dead_wumpus_positions)
    
    def update_perceptions(self, row: int, col: int):
        """Update perceptions for a cell when it's discovered/visited"""
        perceptions = []
        
        if self.has_pit_adjacent(row, col):
            perceptions.append("BREEZE")
        
        if self.has_wumpus_adjacent(row, col):
            perceptions.append("STENCH")
        
        if (row, col) in self.board.gold_positions:
            perceptions.append("GLITTER")
        
        if (row, col) in self.board.pit_positions:
            perceptions.append("PIT")
        
        if self.is_wumpus_alive(row, col):
            perceptions.append("WUMPUS")
        
        self.perceptions[(row, col)] = perceptions
    
    def discover_cell(self, row: int, col: int):
        """Discover a cell (reveal its contents but don't visit)"""
        if (row, col) not in self.discovered_cells:
            self.discovered_cells.add((row, col))
            self.cell_states[(row, col)] = CellState.DISCOVERED
            self.update_perceptions(row, col)
    
    def try_move_or_turn(self, direction: str) -> bool:
        """Try to move in direction, or turn if not facing that direction"""
        direction = direction.upper()
        current_row, current_col = self.hunter_pos
        
        # Get target cell based on direction
        if direction == "UP":
            target_row, target_col = current_row - 1, current_col
        elif direction == "DOWN":
            target_row, target_col = current_row + 1, current_col
        elif direction == "LEFT":
            target_row, target_col = current_row, current_col - 1
        elif direction == "RIGHT":
            target_row, target_col = current_row, current_col + 1
        else:
            return False
        
        # Check if target is within bounds
        if not (0 <= target_row < 10 and 0 <= target_col < 10):
            return False
        
        # If hunter is already facing this direction, try to move
        if self.hunter_direction == direction:
            return self.visit_cell(target_row, target_col)
        else:
            # Turn to face the direction
            self.set_hunter_direction(direction)
            return True
    
    def visit_cell(self, row: int, col: int):
        """Visit a cell (move hunter there)"""
        # Check if move is valid (adjacent to current position)
        if not self.is_valid_move(row, col):
            return False
        
        # Update hunter direction based on movement
        current_row, current_col = self.hunter_pos
        if row < current_row:
            self.set_hunter_direction("UP")
        elif row > current_row:
            self.set_hunter_direction("DOWN")
        elif col < current_col:
            self.set_hunter_direction("LEFT")
        elif col > current_col:
            self.set_hunter_direction("RIGHT")
        
        # Check for death conditions
        if (row, col) in self.board.pit_positions:
            self.hunter_alive = False
            self.score -= 1000
            print(f"Hunter fell into pit at ({row}, {col})! Game Over!")
            return True
        
        if self.is_wumpus_alive(row, col):
            self.hunter_alive = False
            self.score -= 1000
            print(f"Hunter was eaten by Wumpus at ({row}, {col})! Game Over!")
            return True
        
        # Move hunter
        self.hunter_pos = (row, col)
        self.visited_cells.add((row, col))
        self.discovered_cells.add((row, col))
        self.cell_states[(row, col)] = CellState.VISITED
        self.moves += 1
        self.score -= 1  # Each move costs 1 point
        
        self.update_perceptions(row, col)
        
        # Auto-discover adjacent cells
        for adj_row, adj_col in self.get_adjacent_cells(row, col):
            if self.cell_states[(adj_row, adj_col)] == CellState.UNKNOWN:
                self.discover_cell(adj_row, adj_col)
        
        return True
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if move is valid (adjacent to current position)"""
        current_row, current_col = self.hunter_pos
        return (row, col) in self.get_adjacent_cells(current_row, current_col)
    
    def grab_gold(self):
        """Grab gold if present at current location"""
        if self.hunter_pos in self.board.gold_positions:
            self.has_gold = True
            self.score += 1000
            # Remove gold from board 
            self.board.gold_positions.remove(self.hunter_pos)
            print(f"Gold grabbed at {self.hunter_pos}!")
            return True
        return False
    
    def shoot_arrow(self, direction: str = None):
        """Shoot arrow in given direction (or current facing direction if None)"""
        if self.arrow_used:
            print("Arrow already used!")
            return False
        
        self.arrow_used = True
        self.score -= 10  # Cost of shooting
        
        # Use current direction if none specified
        if direction is None:
            direction = self.hunter_direction
        else:
            # Update hunter direction to match arrow direction
            self.set_hunter_direction(direction)
        
        current_row, current_col = self.hunter_pos
        
        # Determine direction
        if direction.upper() == "UP":
            dr, dc = -1, 0
        elif direction.upper() == "DOWN":
            dr, dc = 1, 0
        elif direction.upper() == "LEFT":
            dr, dc = 0, -1
        elif direction.upper() == "RIGHT":
            dr, dc = 0, 1
        else:
            print("Invalid direction!")
            return False
        
        print(f"Shooting arrow from ({current_row}, {current_col}) towards {direction}")
        
        # Check if arrow hits wumpus - arrow travels in straight line until it hits boundary
        arrow_row, arrow_col = current_row + dr, current_col + dc
        while 0 <= arrow_row < 10 and 0 <= arrow_col < 10:
            print(f"Arrow at ({arrow_row}, {arrow_col})")
            
            # Check if there's a living wumpus at this position
            if self.is_wumpus_alive(arrow_row, arrow_col):
                # Kill this specific wumpus
                self.dead_wumpus_positions.add((arrow_row, arrow_col))
                self.score += 500
                print(f"Wumpus killed at ({arrow_row}, {arrow_col})!")
                
                # Update perceptions for all discovered cells (stench may disappear)
                for pos in self.discovered_cells.union(self.visited_cells):
                    self.update_perceptions(pos[0], pos[1])
                
                return True
            
            arrow_row += dr
            arrow_col += dc
        
        print("Arrow missed!")
        return False
    
    def get_cell_display_info(self, row: int, col: int) -> dict:
        """Get display information for a cell"""
        state = self.cell_states[(row, col)]
        perceptions = self.perceptions.get((row, col), [])
        
        info = {
            'state': state,
            'perceptions': perceptions,
            'is_hunter': (row, col) == self.hunter_pos,
            'has_gold': (row, col) in self.board.gold_positions,
            'has_pit': (row, col) in self.board.pit_positions,
            'has_wumpus': self.is_wumpus_alive(row, col),
            'discovered': (row, col) in self.discovered_cells,
            'visited': (row, col) in self.visited_cells
        }
        
        return info
    
    def get_game_stats(self) -> dict:
        """Get current game statistics"""
        living_wumpus_count = len(self.board.wumpus_positions) - len(self.dead_wumpus_positions)
        
        return {
            'score': self.score,
            'moves': self.moves,
            'arrows': 0 if self.arrow_used else 1,
            'gold_collected': 1 if self.has_gold else 0,
            'hunter_alive': self.hunter_alive,
            'hunter_pos': self.hunter_pos,
            'hunter_direction': self.hunter_direction,
            'living_wumpus_count': living_wumpus_count,
            'dead_wumpus_positions': list(self.dead_wumpus_positions)
        }
    
    # Backward compatibility - deprecated property
    @property
    def wumpus_dead(self) -> bool:
        """Deprecated: Use living_wumpus_count instead"""
        return len(self.dead_wumpus_positions) == len(self.board.wumpus_positions)