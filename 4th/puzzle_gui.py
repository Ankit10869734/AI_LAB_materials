import tkinter as tk
from tkinter import ttk, messagebox
import time
from puzzle_solver import PuzzleState, a_star_solver, manhattan_distance, hamming_distance

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver with A*")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')
        
        # Solution path
        self.solution_path = None
        self.current_step = 0
        self.is_playing = False
        self.speed = 500  # milliseconds between steps
        
        # Default puzzle
        self.initial_board = (
            (1, 2, 3),
            (0, 4, 6),
            (7, 5, 8)
        )
        
        self.goal_board = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 0)
        )
        
        self.current_board = self.initial_board
        
        self.setup_gui()
        self.update_board_display()
        
    def setup_gui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="8-Puzzle Solver (A* Algorithm)", 
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Board display frame
        board_frame = tk.Frame(self.root, bg='#f0f0f0')
        board_frame.pack(pady=20)
        
        self.tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(
                    board_frame,
                    text="",
                    font=('Arial', 32, 'bold'),
                    width=4,
                    height=2,
                    relief='raised',
                    bd=3,
                    bg='#4CAF50',
                    fg='white'
                )
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)
        
        # Info display
        self.info_label = tk.Label(
            self.root,
            text="Step: 0 | g: 0 | h: 0 | f: 0",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#555'
        )
        self.info_label.pack(pady=10)
        
        # Speed control
        speed_frame = tk.Frame(self.root, bg='#f0f0f0')
        speed_frame.pack(pady=10)
        
        tk.Label(speed_frame, text="Speed:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        self.speed_slider = tk.Scale(
            speed_frame,
            from_=100,
            to=2000,
            orient=tk.HORIZONTAL,
            length=200,
            command=self.update_speed,
            bg='#f0f0f0'
        )
        self.speed_slider.set(500)
        self.speed_slider.pack(side=tk.LEFT, padx=5)
        
        tk.Label(speed_frame, text="(ms)", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        
        # Heuristic selection
        heuristic_frame = tk.Frame(self.root, bg='#f0f0f0')
        heuristic_frame.pack(pady=5)
        
        tk.Label(heuristic_frame, text="Heuristic:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        self.heuristic_var = tk.StringVar(value="Manhattan")
        heuristic_dropdown = ttk.Combobox(
            heuristic_frame,
            textvariable=self.heuristic_var,
            values=["Manhattan", "Hamming"],
            state="readonly",
            width=15
        )
        heuristic_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        self.solve_btn = tk.Button(
            button_frame,
            text="Solve",
            command=self.solve_puzzle,
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            width=10,
            height=2,
            cursor='hand2'
        )
        self.solve_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = tk.Button(
            button_frame,
            text="Play",
            command=self.play_solution,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=10,
            height=2,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.pause_btn = tk.Button(
            button_frame,
            text="Pause",
            command=self.pause_solution,
            font=('Arial', 12, 'bold'),
            bg='#FF9800',
            fg='white',
            width=10,
            height=2,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.pause_btn.grid(row=0, column=2, padx=5)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_puzzle,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            width=10,
            height=2,
            cursor='hand2'
        )
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # Step buttons
        step_frame = tk.Frame(self.root, bg='#f0f0f0')
        step_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(
            step_frame,
            text="◀ Previous",
            command=self.previous_step,
            font=('Arial', 10),
            bg='#607D8B',
            fg='white',
            width=12,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(
            step_frame,
            text="Next ▶",
            command=self.next_step,
            font=('Arial', 10),
            bg='#607D8B',
            fg='white',
            width=12,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to solve",
            font=('Arial', 10, 'italic'),
            bg='#f0f0f0',
            fg='#666'
        )
        self.status_label.pack(pady=5)
        
    def update_board_display(self):
        """Update the visual display of the puzzle"""
        for i in range(3):
            for j in range(3):
                value = self.current_board[i][j]
                if value == 0:
                    self.tiles[i][j].config(text="", bg='#e0e0e0')
                else:
                    self.tiles[i][j].config(text=str(value), bg='#4CAF50')
    
    def update_info_display(self):
        """Update the step information"""
        if self.solution_path and self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
            move = state.move if state.move else "Initial"
            self.info_label.config(
                text=f"Step: {self.current_step}/{len(self.solution_path)-1} | Move: {move} | g: {state.g} | h: {state.h} | f: {state.f}"
            )
        else:
            self.info_label.config(text="Step: 0 | g: 0 | h: 0 | f: 0")
    
    def update_speed(self, value):
        """Update animation speed"""
        self.speed = int(value)
    
    def solve_puzzle(self):
        """Solve the puzzle using A* algorithm"""
        self.status_label.config(text="Solving puzzle...", fg='#FF9800')
        self.root.update()
        
        # Select heuristic
        if self.heuristic_var.get() == "Manhattan":
            heuristic = manhattan_distance
        else:
            heuristic = hamming_distance
        
        # Solve
        self.solution_path = a_star_solver(self.initial_board, self.goal_board, heuristic)
        
        if self.solution_path:
            self.current_step = 0
            self.current_board = self.solution_path[0].board
            self.update_board_display()
            self.update_info_display()
            
            self.play_btn.config(state=tk.NORMAL)
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
            
            self.status_label.config(
                text=f"Solution found! {len(self.solution_path)-1} moves", 
                fg='#4CAF50'
            )
            messagebox.showinfo(
                "Success", 
                f"Solution found in {len(self.solution_path)-1} moves!\n\nClick 'Play' to watch the solution."
            )
        else:
            self.status_label.config(text="No solution found", fg='#f44336')
            messagebox.showerror("Error", "No solution found for this puzzle!")
    
    def play_solution(self):
        """Play the solution animation"""
        if not self.solution_path:
            return
        
        self.is_playing = True
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.solve_btn.config(state=tk.DISABLED)
        
        self.animate_step()
    
    def animate_step(self):
        """Animate one step of the solution"""
        if not self.is_playing:
            return
        
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_board = self.solution_path[self.current_step].board
            self.update_board_display()
            self.update_info_display()
            
            self.root.after(self.speed, self.animate_step)
        else:
            self.is_playing = False
            self.pause_btn.config(state=tk.DISABLED)
            self.solve_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Solution complete!", fg='#4CAF50')
    
    def pause_solution(self):
        """Pause the solution animation"""
        self.is_playing = False
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.solve_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Paused", fg='#FF9800')
    
    def next_step(self):
        """Go to next step"""
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_board = self.solution_path[self.current_step].board
            self.update_board_display()
            self.update_info_display()
    
    def previous_step(self):
        """Go to previous step"""
        if self.solution_path and self.current_step > 0:
            self.current_step -= 1
            self.current_board = self.solution_path[self.current_step].board
            self.update_board_display()
            self.update_info_display()
    
    def reset_puzzle(self):
        """Reset the puzzle to initial state"""
        self.is_playing = False
        self.current_step = 0
        self.current_board = self.initial_board
        self.solution_path = None
        
        self.update_board_display()
        self.update_info_display()
        
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.solve_btn.config(state=tk.NORMAL)
        
        self.status_label.config(text="Ready to solve", fg='#666')

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
