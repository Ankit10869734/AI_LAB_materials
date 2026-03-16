# 8-Puzzle Solver for Google Colab
# Run each cell in order

# ============================================================
# CELL 1: Install required packages (if needed)
# ============================================================
# !pip install ipywidgets matplotlib

# ============================================================
# CELL 2: Import libraries
# ============================================================
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output, display
import ipywidgets as widgets
from ipywidgets import Button, IntSlider, Dropdown, HBox, VBox, Output
import time

# ============================================================
# CELL 3: Define PuzzleState class and A* algorithm
# ============================================================

class PuzzleState:
    def __init__(self, board, parent=None, move=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = self.g + self.h

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
        moves = [(0, 1, 'Right'), (0, -1, 'Left'), (1, 0, 'Down'), (-1, 0, 'Up')]

        for dr, dc, move_name in moves:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_board = [list(row) for row in self.board]
                new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
                neighbors.append(PuzzleState(tuple(tuple(row) for row in new_board), self, move_name, self.g + 1))
        return neighbors


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
    initial_state = PuzzleState(initial_board, g=0, h=heuristic_func(initial_board, goal_board))
    
    open_set = [initial_state]
    closed_set = set()
    g_scores = {initial_state: 0}
    
    while open_set:
        current_state = heapq.heappop(open_set)
        
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
            
            if neighbor not in g_scores or neighbor.g < g_scores[neighbor]:
                g_scores[neighbor] = neighbor.g
                heapq.heappush(open_set, neighbor)
                
    return None

print("✅ A* Algorithm loaded successfully!")

# ============================================================
# CELL 4: Simple visualization function
# ============================================================

def draw_board(board, title=""):
    """Draw a single puzzle board"""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            
            if value == 0:
                color = '#e0e0e0'
            else:
                color = '#4CAF50'
            
            rect = patches.Rectangle((j, 2-i), 1, 1, 
                                    linewidth=3, 
                                    edgecolor='white', 
                                    facecolor=color)
            ax.add_patch(rect)
            
            if value != 0:
                ax.text(j + 0.5, 2-i + 0.5, str(value),
                       ha='center', va='center',
                       fontsize=50, fontweight='bold',
                       color='white')
    
    if title:
        plt.title(title, fontsize=14, pad=20, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

print("✅ Visualization function loaded!")

# ============================================================
# CELL 5: Test the solver (Quick demo)
# ============================================================

# Define puzzle
initial = (
    (1, 2, 3),
    (0, 4, 6),
    (7, 5, 8)
)

goal = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

print("🧩 Initial Puzzle:")
draw_board(initial, "Initial State")

print("\n🎯 Goal:")
draw_board(goal, "Goal State")

print("\n🔍 Solving with A*...")
solution = a_star_solver(initial, goal, manhattan_distance)

if solution:
    print(f"✅ Solution found in {len(solution)-1} moves!")
    print(f"📊 Explored {len(solution)} states")
else:
    print("❌ No solution found")

# ============================================================
# CELL 6: Display solution step by step (Manual)
# ============================================================

if solution:
    print(f"Showing all {len(solution)} steps:\n")
    
    for i, state in enumerate(solution):
        move = state.move if state.move else "Initial"
        title = f"Step {i}/{len(solution)-1} | Move: {move} | g={state.g}, h={state.h}, f={state.f}"
        draw_board(state.board, title)
        print("-" * 60)

# ============================================================
# CELL 7: Interactive Widget-based GUI
# ============================================================

class InteractivePuzzle:
    def __init__(self, initial_board, goal_board):
        self.initial_board = initial_board
        self.goal_board = goal_board
        self.solution_path = None
        self.current_step = 0
        
        # Create widgets
        self.output = Output()
        self.step_slider = IntSlider(min=0, max=0, value=0, description='Step:', 
                                     style={'description_width': '60px'}, 
                                     layout={'width': '500px'})
        self.solve_btn = Button(description='🔍 Solve', button_style='primary')
        self.reset_btn = Button(description='🔄 Reset', button_style='danger')
        self.heuristic = Dropdown(options=['Manhattan', 'Hamming'], 
                                 value='Manhattan', 
                                 description='Heuristic:')
        
        self.status = widgets.HTML(value='<h3 style="text-align:center;">Ready to solve</h3>')
        
        # Connect events
        self.solve_btn.on_click(self.solve)
        self.reset_btn.on_click(self.reset)
        self.step_slider.observe(self.on_step_change, 'value')
        
        # Layout
        controls = HBox([self.solve_btn, self.reset_btn, self.heuristic])
        self.gui = VBox([controls, self.step_slider, self.status, self.output])
        
        # Initial display
        self.display_current()
    
    def display_current(self):
        with self.output:
            clear_output(wait=True)
            if self.solution_path:
                state = self.solution_path[self.current_step]
                move = state.move if state.move else "Initial"
                title = f"Step {self.current_step}/{len(self.solution_path)-1} | Move: {move} | g={state.g}, h={state.h}, f={state.f}"
                draw_board(state.board, title)
            else:
                draw_board(self.initial_board, "Initial State")
    
    def solve(self, b):
        self.status.value = '<h3 style="text-align:center; color:orange;">⏳ Solving...</h3>'
        
        heuristic_func = manhattan_distance if self.heuristic.value == 'Manhattan' else hamming_distance
        self.solution_path = a_star_solver(self.initial_board, self.goal_board, heuristic_func)
        
        if self.solution_path:
            self.current_step = 0
            self.step_slider.max = len(self.solution_path) - 1
            self.step_slider.value = 0
            self.status.value = f'<h3 style="text-align:center; color:green;">✅ Solved in {len(self.solution_path)-1} moves!</h3>'
            self.display_current()
        else:
            self.status.value = '<h3 style="text-align:center; color:red;">❌ No solution found</h3>'
    
    def reset(self, b):
        self.solution_path = None
        self.current_step = 0
        self.step_slider.value = 0
        self.step_slider.max = 0
        self.status.value = '<h3 style="text-align:center;">Ready to solve</h3>'
        self.display_current()
    
    def on_step_change(self, change):
        self.current_step = change['new']
        self.display_current()
    
    def show(self):
        display(self.gui)


# Create interactive puzzle
puzzle = InteractivePuzzle(initial, goal)
puzzle.show()

print("\n📝 Instructions:")
print("1. Click 'Solve' to find the solution")
print("2. Use the slider to navigate through steps")
print("3. Try different heuristics (Manhattan vs Hamming)")
print("4. Click 'Reset' to start over")
