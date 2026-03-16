import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g  # cost from start node to current node
        self.h = h  # estimated cost from current node to goal node
        self.f = self.g + self.h # total estimated cost

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def get_blank_position(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    return r, c

    def get_neighbors(self):
        neighbors = []
        r, c = self.get_blank_position()
        
        # Possible moves: (dr, dc)
        moves = [(0, 1, 'Right'), (0, -1, 'Left'), (1, 0, 'Down'), (-1, 0, 'Up')]

        for dr, dc, move_name in moves:
            new_r, new_c = r + dr, c + dc

            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_board = [list(row) for row in self.board]
                new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
                neighbors.append(PuzzleState(tuple(tuple(row) for row in new_board), self, move_name, self.g + 1))
        return neighbors

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

# Heuristic functions
def hamming_distance(board, goal_board):
    distance = 0
    for r in range(3):
        for c in range(3):
            if board[r][c] != goal_board[r][c] and board[r][c] != 0:
                distance += 1
    return distance

def manhattan_distance(board, goal_board):
    distance = 0
    goal_positions = {}
    for r in range(3):
        for c in range(3):
            goal_positions[goal_board[r][c]] = (r, c)

    for r in range(3):
        for c in range(3):
            tile = board[r][c]
            if tile != 0:
                goal_r, goal_c = goal_positions[tile]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

def a_star_solver(initial_board, goal_board, heuristic_func=manhattan_distance):
    """
    Fixed A* solver that properly handles duplicate states
    """
    initial_state = PuzzleState(initial_board, g=0, h=heuristic_func(initial_board, goal_board))
    
    open_set = [initial_state]
    closed_set = set()
    # Track best g-scores for states in open_set
    g_scores = {initial_state: 0}
    
    while open_set:
        current_state = heapq.heappop(open_set)
        
        # Skip if we've found a better path to this state already
        if current_state in closed_set:
            continue
        
        if current_state.board == goal_board:
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.parent
            return path[::-1]
            
        closed_set.add(current_state)
        
        for neighbor in current_state.get_neighbors():
            if neighbor in closed_set:
                continue
            
            neighbor.h = heuristic_func(neighbor.board, goal_board)
            neighbor.f = neighbor.g + neighbor.h
            
            # Only add if we haven't seen this state or found a better path
            if neighbor not in g_scores or neighbor.g < g_scores[neighbor]:
                g_scores[neighbor] = neighbor.g
                heapq.heappush(open_set, neighbor)
                
    return None # No solution found
