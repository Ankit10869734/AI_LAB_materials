import random
import time
import tkinter as tk
from tkinter import ttk

def random_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def count_attacks(board):
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                attacks += 1
            if abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks

def get_best_neighbour(board):
    n = len(board)
    best = board[:]
    best_attacks = count_attacks(board)
    for row in range(n):
        for col in range(n):
            if col == board[row]:
                continue
            neighbour = board[:]
            neighbour[row] = col
            attacks = count_attacks(neighbour)
            if attacks < best_attacks:
                best_attacks = attacks
                best = neighbour[:]
    return best, best_attacks

def hill_climbing_with_steps(n, max_restarts=1000):
    all_restarts = []
    for restart in range(max_restarts):
        board = random_board(n)
        steps = [board[:]]
        while True:
            current_attacks = count_attacks(board)
            if current_attacks == 0:
                return board, steps, restart, all_restarts
            neighbour, neighbour_attacks = get_best_neighbour(board)
            if neighbour_attacks >= current_attacks:
                all_restarts.append(steps)
                break
            board = neighbour
            steps.append(board[:])
    return None, [], max_restarts, all_restarts

def attacking_rows(board):
    n = len(board)
    bad = set()
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                bad.add(i)
                bad.add(j)
    return bad

def print_board(board, label=""):
    n = len(board)
    if label:
        print(label)
    line = "+" + ("---+" * n)
    bad = attacking_rows(board)
    for row in range(n):
        print(line)
        row_str = "|"
        for col in range(n):
            if board[row] == col:
                row_str += " Q |" if row not in bad else " X |"
            else:
                row_str += " . |"
        print(row_str)
    print(line)
    print(f"Attacks: {count_attacks(board)}")

def cmd_demo(n=8):
    print()
    print("N-QUEENS PROBLEM - Hill Climbing Algorithm")
    print(f"N = {n}")
    print()

    initial = random_board(n)
    print("INITIAL PROBLEM (random placement):")
    print_board(initial, "")
    print()

    t_start = time.time()
    solution, steps, restarts, failed_runs = hill_climbing_with_steps(n)
    t_end = time.time()
    elapsed = t_end - t_start

    if solution is None:
        print("No solution found.")
        return None, [], 0, 0

    print(f"Solving... took {len(steps)-1} steps across {restarts} restart(s).")
    print()

    for i, board in enumerate(steps):
        if i == 0:
            print(f"Step 0 - Initial state (this run):")
        elif i == len(steps) - 1:
            print(f"Step {i} - SOLUTION:")
        else:
            print(f"Step {i}:")
        print_board(board, "")
        print()

    print("SOLUTION FOUND")
    print(f"Board        : {solution}")
    print(f"Attacks      : {count_attacks(solution)}")
    print(f"Steps taken  : {len(steps) - 1}")
    print(f"Restarts     : {restarts}")
    print(f"Time taken   : {elapsed:.4f} seconds")
    print(f"Time complex.: O(n^3) per step, O(restarts * steps * n^3) total")
    print(f"Space complex: O(n)")
    print()
    print("Opening GUI for visualization...")
    print()

    return solution, steps, restarts, elapsed


CELL = 48

COLORS = {
    "light"  : "#F0D9B5",
    "dark"   : "#B58863",
    "queen"  : "#1a1a2e",
    "attack" : "#e63946",
    "solve"  : "#2a9d8f",
    "bg"     : "#1e1e2e",
    "panel"  : "#2a2a3e",
    "text"   : "#cdd6f4",
    "sub"    : "#7f849c",
    "btn"    : "#89b4fa",
    "btn_fg" : "#1e1e2e",
    "green"  : "#a6e3a1",
    "red"    : "#f38ba8",
    "yellow" : "#f9e2af",
}


class NQueensApp(tk.Tk):
    def __init__(self, n, steps, restarts, elapsed):
        super().__init__()
        self.title("N-Queens  Hill Climbing  Visualizer")
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        self.n        = n
        self.steps    = steps
        self.restarts = restarts
        self.elapsed  = elapsed
        self.cur_step = 0
        self.playing  = False
        self.after_id = None

        self._build_ui()
        self._draw(self.steps[0])

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        panel = tk.Frame(self, bg=COLORS["panel"], padx=14, pady=14)
        panel.grid(row=0, column=0, sticky="ns", padx=(10, 4), pady=10)

        tk.Label(panel, text="N-Queens", font=("Courier", 15, "bold"),
                 bg=COLORS["panel"], fg=COLORS["text"]).pack(pady=(0, 2))
        tk.Label(panel, text="Hill Climbing", font=("Courier", 9),
                 bg=COLORS["panel"], fg=COLORS["sub"]).pack(pady=(0, 12))

        tk.Label(panel, text=f"N         : {self.n}", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")
        tk.Label(panel, text=f"Total steps: {len(self.steps)-1}", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")
        tk.Label(panel, text=f"Restarts  : {self.restarts}", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")
        tk.Label(panel, text=f"Time      : {self.elapsed:.4f}s", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")
        tk.Label(panel, text=f"Time O()  : O(n^3/step)", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")
        tk.Label(panel, text=f"Space O() : O(n)", font=("Courier", 10),
                 bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x", pady=(0, 14))

        self.lbl_step    = self._info(panel, "Step    : 0")
        self.lbl_attacks = self._info(panel, "Attacks : -")
        self.lbl_status  = self._info(panel, "Status  : Problem", color=COLORS["yellow"])

        tk.Label(panel, text="", bg=COLORS["panel"]).pack(pady=4)

        self.speed_var = tk.IntVar(value=600)
        tk.Label(panel, text="Speed (ms):", font=("Courier", 9),
                 bg=COLORS["panel"], fg=COLORS["sub"]).pack(anchor="w")
        tk.Scale(panel, from_=100, to=2000, orient="horizontal",
                 variable=self.speed_var, bg=COLORS["panel"], fg=COLORS["text"],
                 highlightthickness=0, troughcolor=COLORS["bg"],
                 length=160).pack(anchor="w", pady=(0, 10))

        self._btn(panel, "Play",     self._play)
        self._btn(panel, "Pause",    self._pause)
        self._btn(panel, "Prev",     self._prev)
        self._btn(panel, "Next",     self._next)
        self._btn(panel, "Restart",  self._restart)

        right = tk.Frame(self, bg=COLORS["bg"])
        right.grid(row=0, column=1, padx=(4, 10), pady=10, sticky="nsew")

        self.step_label = tk.Label(right, text="INITIAL PROBLEM",
                                   font=("Courier", 12, "bold"),
                                   bg=COLORS["bg"], fg=COLORS["yellow"])
        self.step_label.pack(pady=(0, 6))

        self.canvas = tk.Canvas(right, bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack()

        size = self.n * CELL
        self.canvas.config(width=size, height=size)

    def _btn(self, parent, text, cmd):
        b = tk.Button(parent, text=text, command=cmd,
                      font=("Courier", 10, "bold"),
                      bg=COLORS["btn"], fg=COLORS["btn_fg"],
                      relief="flat", padx=6, pady=5, width=14, cursor="hand2")
        b.pack(pady=2)
        return b

    def _info(self, parent, text, color=None):
        lbl = tk.Label(parent, text=text, font=("Courier", 10),
                       bg=COLORS["panel"], fg=color or COLORS["text"], anchor="w")
        lbl.pack(fill="x")
        return lbl

    def _draw(self, board):
        n = self.n
        self.canvas.delete("all")
        bad = attacking_rows(board)
        attacks = count_attacks(board)
        is_solution = attacks == 0

        for row in range(n):
            for col in range(n):
                x1, y1 = col * CELL, row * CELL
                x2, y2 = x1 + CELL, y1 + CELL

                if board[row] == col and row in bad:
                    fill = COLORS["attack"]
                elif board[row] == col and is_solution:
                    fill = COLORS["solve"]
                elif (row + col) % 2 == 0:
                    fill = COLORS["light"]
                else:
                    fill = COLORS["dark"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#000000")

                if board[row] == col:
                    self.canvas.create_text(
                        x1 + CELL // 2, y1 + CELL // 2,
                        text="Q",
                        font=("Courier", int(CELL * 0.45), "bold"),
                        fill=COLORS["queen"])

        self.lbl_attacks.config(text=f"Attacks : {attacks}")
        self.lbl_step.config(text=f"Step    : {self.cur_step}")

        total = len(self.steps) - 1
        if self.cur_step == 0 and total > 0:
            self.step_label.config(text=f"INITIAL PROBLEM  (step 0 of {total})", fg=COLORS["yellow"])
            self.lbl_status.config(text="Status  : Problem", fg=COLORS["yellow"])
        elif is_solution:
            self.step_label.config(text=f"SOLUTION FOUND   (step {self.cur_step} of {total})", fg=COLORS["green"])
            self.lbl_status.config(text="Status  : Solved!", fg=COLORS["green"])
        else:
            self.step_label.config(text=f"Step {self.cur_step} of {total}", fg=COLORS["text"])
            self.lbl_status.config(text="Status  : Solving...", fg=COLORS["sub"])

    def _play(self):
        if self.playing:
            return
        self.playing = True
        self._tick()

    def _tick(self):
        if not self.playing:
            return
        if self.cur_step < len(self.steps) - 1:
            self.cur_step += 1
            self._draw(self.steps[self.cur_step])
            self.after_id = self.after(self.speed_var.get(), self._tick)
        else:
            self.playing = False

    def _pause(self):
        self.playing = False
        if self.after_id:
            self.after_cancel(self.after_id)

    def _next(self):
        self._pause()
        if self.cur_step < len(self.steps) - 1:
            self.cur_step += 1
            self._draw(self.steps[self.cur_step])

    def _prev(self):
        self._pause()
        if self.cur_step > 0:
            self.cur_step -= 1
            self._draw(self.steps[self.cur_step])

    def _restart(self):
        self._pause()
        self.cur_step = 0
        self._draw(self.steps[0])


if __name__ == "__main__":
    valid = [4, 8, 10, 12, 16, 20]
    print("N-QUEENS PROBLEM - Hill Climbing Algorithm")
    print(f"Valid values of N: {valid}")
    while True:
        try:
            N = int(input("Enter N: "))
            if N in valid:
                break
            print(f"Please enter one of {valid}")
        except ValueError:
            print("Invalid input. Enter a number.")
    solution, steps, restarts, elapsed = cmd_demo(N)
    if solution:
        app = NQueensApp(N, steps, restarts, elapsed)
        app.mainloop()
