import heapq
import time
import tkinter as tk
from collections import deque

GRID = [
    [0,0,0,1,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,1,0,0],
    [0,1,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,1,0,1,0,1],
    [0,0,0,0,0,1,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,0],
    [0,0,0,1,0,0,0,0,1,0],
    [0,1,1,1,0,1,0,1,1,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0],
]
ROWS, COLS = 10, 10
START      = (0, 0)
GOALS      = [(2, 4), (6, 5), (8, 7)]
WEIGHTS    = {(2,4): 1, (6,5): 3, (8,7): 2}
EXIT       = (9, 9)
CELL       = 52

COLORS = {
    "bg"        : "#0a0e14",
    "panel"     : "#0f1520",
    "text"      : "#c8d8e8",
    "sub"       : "#4a6080",
    "btn"       : "#00d4ff",
    "btn_fg"    : "#0a0e14",
    "open"      : "#0d1822",
    "wall"      : "#1a2535",
    "start"     : "#002a1a",
    "start_fg"  : "#00ff9d",
    "goal"      : "#2a1500",
    "goal_fg"   : "#ff6b35",
    "exit"      : "#1a0030",
    "exit_fg"   : "#aa00ff",
    "visited"   : "#001f30",
    "path"      : "#003d5c",
    "current"   : "#00d4ff",
    "collected" : "#001a00",
    "green"     : "#00ff9d",
    "yellow"    : "#f9e2af",
    "accent"    : "#00d4ff",
}


def neighbors(r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and GRID[nr][nc] == 0:
            yield (nr, nc)

def reconstruct(came, goal):
    path, cur = [goal], goal
    while cur in came:
        cur = came[cur]
        path.append(cur)
    return list(reversed(path))

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def bfs(start, goal):
    queue, came, vis, order = deque([start]), {}, {start}, []
    while queue:
        node = queue.popleft()
        order.append(node)
        if node == goal:
            return reconstruct(came, goal), order
        for nb in neighbors(*node):
            if nb not in vis:
                vis.add(nb); came[nb] = node; queue.append(nb)
    return None, order

def dfs(start, goal):
    stack, came, vis, order = [start], {}, {start}, []
    while stack:
        node = stack.pop()
        order.append(node)
        if node == goal:
            return reconstruct(came, goal), order
        for nb in neighbors(*node):
            if nb not in vis:
                vis.add(nb); came[nb] = node; stack.append(nb)
    return None, order

def astar(start, goal):
    heap, came, g, order = [(heuristic(start,goal),0,start)], {}, {start:0}, []
    while heap:
        _, cost, node = heapq.heappop(heap)
        order.append(node)
        if node == goal:
            return reconstruct(came, goal), order
        for nb in neighbors(*node):
            ng = cost + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng; came[nb] = node
                heapq.heappush(heap, (ng+heuristic(nb,goal), ng, nb))
    return None, order

def ucs(start, goal):
    heap, came, cost, order = [(0,start)], {}, {start:0}, []
    while heap:
        c, node = heapq.heappop(heap)
        order.append(node)
        if node == goal:
            return reconstruct(came, goal), order
        for nb in neighbors(*node):
            nc = c + 1
            if nb not in cost or nc < cost[nb]:
                cost[nb] = nc; came[nb] = node
                heapq.heappush(heap, (nc, nb))
    return None, order

ALGO_FN = {"BFS": bfs, "DFS": dfs, "A*": astar, "UCS": ucs}

def solve(algo_name):
    fn     = ALGO_FN[algo_name]
    goals  = sorted(GOALS, key=lambda g: WEIGHTS[g]) if algo_name == "UCS" else list(GOALS)
    cur    = START
    segs   = []
    for goal in goals:
        path, visited = fn(cur, goal)
        if path is None:
            return None
        segs.append({"goal": goal, "path": path, "visited": visited, "steps": len(path)-1})
        cur = goal
    path, visited = fn(cur, EXIT)
    if path is None:
        return None
    segs.append({"goal": EXIT, "path": path, "visited": visited, "steps": len(path)-1})
    return segs

def print_grid(path_set, collected_set, current=None, label=""):
    if label:
        print(label)
    line = "+" + ("----+" * COLS)
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            pos = (r, c)
            if GRID[r][c] == 1:
                row_str += " ## |"
            elif pos == current:
                row_str += " >> |"
            elif pos == START:
                row_str += "  S |"
            elif pos == EXIT:
                row_str += "  E |"
            elif pos in collected_set:
                row_str += "  * |"
            elif pos in GOALS:
                w = WEIGHTS[pos]
                row_str += f" G{w} |"
            elif pos in path_set:
                row_str += "  . |"
            else:
                row_str += "    |"
        print(row_str)
    print(line)

def cmd_demo(algo_name):
    print()
    print("=" * 52)
    print("  GRID NAVIGATION - Multiple Goals")
    print("=" * 52)
    print(f"  Algorithm  : {algo_name}")
    print(f"  Grid       : {ROWS}x{COLS}")
    print(f"  Start      : {START}")
    print(f"  Exit       : {EXIT}")
    print(f"  Goals      : {GOALS}")
    print(f"  Weights    : {WEIGHTS}")
    print("=" * 52)
    print()

    print("INITIAL STATE:")
    print_grid(set(), set(), label="")
    print()

    t0   = time.time()
    segs = solve(algo_name)
    elapsed = time.time() - t0

    if segs is None:
        print("No solution found.")
        return None, 0

    collected = set()
    full_path = set()
    for i, s in enumerate(segs):
        is_exit = s["goal"] == EXIT
        if is_exit:
            label = f"Segment {i+1} — Heading to EXIT {EXIT}  |  steps: {s['steps']}"
        else:
            g = s["goal"]
            label = f"Segment {i+1} — Goal {g}  weight={WEIGHTS[g]}  |  steps: {s['steps']}"

        print("-" * 52)
        print(label)
        print(f"  Path: {s['path']}")
        print()

        seg_path = set(s["path"])
        full_path |= seg_path
        print_grid(full_path, collected, current=s["goal"], label="")
        print()

        if not is_exit:
            collected.add(s["goal"])

    total = sum(s["steps"] for s in segs)
    print("=" * 52)
    print("  SOLUTION FOUND")
    print("=" * 52)
    print()
    print("FINAL STATE:")
    print_grid(full_path, collected, current=EXIT, label="")
    print()
    for i, s in enumerate(segs):
        label = "EXIT" if s["goal"] == EXIT else f"Goal {i+1} {s['goal']}  w={WEIGHTS.get(s['goal'],'-')}"
        print(f"  {label:38s} steps: {s['steps']}")
    print()
    print(f"  Total steps    : {total}")
    print(f"  Time taken     : {elapsed:.4f}s")
    print(f"  Time complex.  : O(V + E) per segment")
    print(f"  Space complex. : O(V)")
    print()
    print("  Opening GUI for visualization...")
    print()
    return segs, elapsed


class GridApp(tk.Tk):
    def __init__(self, algo_name, segs, elapsed):
        super().__init__()
        self.title("AI Lab 6 - Navigation with Multiple Goals")
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        self.algo_name   = algo_name
        self.segs        = segs
        self.elapsed     = elapsed
        self.total_steps = sum(s["steps"] for s in segs)
        self.flat        = self._flatten()
        self.cur         = 0
        self.playing     = False
        self.after_id    = None

        self._build_ui()
        self._draw(self.cur)

    def _flatten(self):
        frames, collected = [], set()
        for seg in self.segs:
            for node in seg["visited"]:
                frames.append({"type": "visited", "node": node, "collected": set(collected), "path_nodes": set()})
            path_acc = set()
            for node in seg["path"]:
                path_acc.add(node)
                frames.append({"type": "path", "node": node, "collected": set(collected), "path_nodes": set(path_acc)})
            if seg["goal"] != EXIT:
                collected.add(seg["goal"])
                frames.append({"type": "collected", "node": seg["goal"], "collected": set(collected), "path_nodes": set(path_acc)})
        return frames

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        panel = tk.Frame(self, bg=COLORS["panel"], padx=14, pady=14)
        panel.grid(row=0, column=0, sticky="ns", padx=(10,4), pady=10)

        tk.Label(panel, text="Grid Navigation", font=("Courier", 13, "bold"),
                 bg=COLORS["panel"], fg=COLORS["text"]).pack(pady=(0,2))
        tk.Label(panel, text="Multiple Goals", font=("Courier", 9),
                 bg=COLORS["panel"], fg=COLORS["sub"]).pack(pady=(0,12))

        for line in [
            f"Algorithm  : {self.algo_name}",
            f"Grid       : {ROWS}x{COLS}",
            f"Start      : {START}",
            f"Goals      : {GOALS}",
            f"Weights    : {WEIGHTS}",
            f"Exit       : {EXIT}",
            f"Total steps: {self.total_steps}",
            f"Time       : {self.elapsed:.4f}s",
            f"Time  O()  : O(n^2) per step",
            f"Space O()  : O(n^2)",
        ]:
            tk.Label(panel, text=line, font=("Courier", 9),
                     bg=COLORS["panel"], fg=COLORS["text"], anchor="w").pack(fill="x")

        tk.Label(panel, text="", bg=COLORS["panel"]).pack(pady=4)

        self.lbl_frame  = self._info(panel, "Frame   : 0")
        self.lbl_status = self._info(panel, "Status  : -",     color=COLORS["yellow"])
        self.lbl_goals  = self._info(panel, "Goals   : 0/3")

        tk.Label(panel, text="", bg=COLORS["panel"]).pack(pady=4)

        tk.Label(panel, text="Speed (ms):", font=("Courier", 9),
                 bg=COLORS["panel"], fg=COLORS["sub"]).pack(anchor="w")
        self.speed_var = tk.IntVar(value=30)
        tk.Scale(panel, from_=5, to=500, orient="horizontal",
                 variable=self.speed_var, bg=COLORS["panel"], fg=COLORS["text"],
                 highlightthickness=0, troughcolor=COLORS["bg"], length=160).pack(anchor="w", pady=(0,10))

        self._btn(panel, "Play",    self._play)
        self._btn(panel, "Pause",   self._pause)
        self._btn(panel, "Prev",    self._prev)
        self._btn(panel, "Next",    self._next)
        self._btn(panel, "Restart", self._restart)

        right = tk.Frame(self, bg=COLORS["bg"])
        right.grid(row=0, column=1, padx=(4,10), pady=10, sticky="nsew")

        self.step_label = tk.Label(right, text="",
                                   font=("Courier", 11, "bold"),
                                   bg=COLORS["bg"], fg=COLORS["yellow"])
        self.step_label.pack(pady=(0,6))

        size = COLS * CELL + (COLS - 1) * 2
        self.canvas = tk.Canvas(right, width=size, height=size,
                                bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack()

        legend = tk.Frame(right, bg=COLORS["panel"], pady=4, padx=6)
        legend.pack(fill="x", pady=(8,0))
        for lbl, fg, bg in [
            ("S Start",  COLORS["start_fg"],  COLORS["start"]),
            ("G Goal",   COLORS["goal_fg"],   COLORS["goal"]),
            ("E Exit",   COLORS["exit_fg"],   COLORS["exit"]),
            ("■ Wall",   COLORS["wall"],      COLORS["wall"]),
            ("· Visit",  "#002233",           COLORS["visited"]),
            ("▬ Path",   COLORS["accent"],    COLORS["path"]),
            ("◆ Robot",  COLORS["bg"],        COLORS["current"]),
        ]:
            tk.Label(legend, text=lbl, bg=bg, fg=fg,
                     font=("Courier", 8), padx=4, pady=2).pack(side="left", padx=2)

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

    def _draw(self, idx):
        frame      = self.flat[idx]
        ftype      = frame["type"]
        robot      = frame["node"]
        collected  = frame["collected"]
        path_nodes = frame["path_nodes"]

        visited_acc = set()
        for i in range(idx + 1):
            f = self.flat[i]
            if f["type"] == "visited":
                visited_acc.add(f["node"])

        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * (CELL + 2)
                y1 = r * (CELL + 2)
                x2, y2 = x1 + CELL, y1 + CELL
                pos = (r, c)

                if GRID[r][c] == 1:
                    fill, outline, lbl, fg = COLORS["wall"], "#0d1520", "", COLORS["wall"]
                elif pos == robot:
                    fill, outline, lbl, fg = COLORS["current"], COLORS["current"], "◆", COLORS["bg"]
                elif pos == START:
                    fill, outline, lbl, fg = COLORS["start"], COLORS["start_fg"], "S", COLORS["start_fg"]
                elif pos == EXIT:
                    fill, outline, lbl, fg = COLORS["exit"], COLORS["exit_fg"], "E", COLORS["exit_fg"]
                elif pos in collected:
                    fill, outline, lbl, fg = COLORS["collected"], COLORS["green"], "✓", COLORS["green"]
                elif pos in GOALS:
                    w = WEIGHTS[pos]
                    fill, outline, lbl, fg = COLORS["goal"], COLORS["goal_fg"], f"G{w}", COLORS["goal_fg"]
                elif pos in path_nodes:
                    fill, outline, lbl, fg = COLORS["path"], COLORS["accent"], f"{r},{c}", COLORS["sub"]
                elif pos in visited_acc:
                    fill, outline, lbl, fg = COLORS["visited"], "#002233", f"{r},{c}", COLORS["sub"]
                else:
                    fill, outline, lbl, fg = COLORS["open"], "#1e2d40", f"{r},{c}", COLORS["sub"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=1)
                font_size = 12 if lbl in ("S","E","◆","✓") else 7
                self.canvas.create_text(x1+CELL//2, y1+CELL//2, text=lbl,
                                        fill=fg, font=("Courier", font_size, "bold"))

        total = len(self.flat) - 1
        goals_done = len(collected)
        self.lbl_frame.config(text=f"Frame   : {idx} / {total}")
        self.lbl_goals.config(text=f"Goals   : {goals_done}/3")

        if goals_done == 3 and robot == EXIT:
            self.step_label.config(text="SOLUTION — all goals collected + exit reached!", fg=COLORS["green"])
            self.lbl_status.config(text="Status  : Done!", fg=COLORS["green"])
        elif ftype == "visited":
            self.step_label.config(text=f"Exploring...  frame {idx} of {total}", fg=COLORS["sub"])
            self.lbl_status.config(text="Status  : Searching", fg=COLORS["yellow"])
        elif ftype == "path":
            self.step_label.config(text=f"Moving along path...  frame {idx} of {total}", fg=COLORS["text"])
            self.lbl_status.config(text="Status  : Moving", fg=COLORS["accent"])
        elif ftype == "collected":
            self.step_label.config(text=f"Collected goal at {robot}!", fg=COLORS["green"])
            self.lbl_status.config(text="Status  : Goal!", fg=COLORS["green"])

    def _play(self):
        if self.playing:
            return
        self.playing = True
        self._tick()

    def _tick(self):
        if not self.playing:
            return
        if self.cur < len(self.flat) - 1:
            self.cur += 1
            self._draw(self.cur)
            self.after_id = self.after(self.speed_var.get(), self._tick)
        else:
            self.playing = False

    def _pause(self):
        self.playing = False
        if self.after_id:
            self.after_cancel(self.after_id)

    def _next(self):
        self._pause()
        if self.cur < len(self.flat) - 1:
            self.cur += 1
            self._draw(self.cur)

    def _prev(self):
        self._pause()
        if self.cur > 0:
            self.cur -= 1
            self._draw(self.cur)

    def _restart(self):
        self._pause()
        self.cur = 0
        self._draw(self.cur)


if __name__ == "__main__":
    algos = ["BFS", "DFS", "A*", "UCS"]
    print("GRID NAVIGATION - Multiple Goals")
    print(f"Algorithms: {algos}")
    while True:
        choice = input("Enter algorithm (BFS / DFS / A* / UCS): ").strip().upper()
        if choice in algos:
            break
        print(f"Choose from {algos}")
    segs, elapsed = cmd_demo(choice)
    if segs:
        print("Opening GUI...")
        app = GridApp(choice, segs, elapsed)
        app.mainloop()
