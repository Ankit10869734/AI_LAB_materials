# 8-Puzzle Solver with A* Algorithm

A Python implementation of the 8-puzzle game solver using the A* search algorithm with a graphical user interface.

## Features

- **A* Algorithm Implementation**: Efficient pathfinding using Manhattan and Hamming distance heuristics
- **Interactive GUI**: Visual representation of the puzzle and solution steps
- **Step-by-Step Playback**: Watch the solution unfold with adjustable speed
- **Manual Navigation**: Use Previous/Next buttons to explore each step
- **Two Heuristics**: Compare solutions using Manhattan or Hamming distance

## What Was Fixed

The original code had an issue in the A* solver where duplicate states in the open set weren't properly handled. The improved version:

1. **Tracks g-scores**: Maintains a dictionary of best known g-scores for each state
2. **Skips processed states**: Avoids reprocessing states that are already in the closed set
3. **Updates only when better**: Only adds a neighbor to the open set if it offers a better path

## Files

- `puzzle_solver.py` - Core A* algorithm implementation
- `puzzle_gui.py` - GUI interface using tkinter
- `test_solver.py` - Command-line test script

## How to Run

### GUI Version (Recommended)
```bash
python puzzle_gui.py
```

### Command Line Version
```bash
python test_solver.py
```

## GUI Controls

1. **Solve**: Runs the A* algorithm to find the solution
2. **Play**: Automatically plays through the solution steps
3. **Pause**: Pauses the automatic playback
4. **Reset**: Returns to the initial puzzle state
5. **Previous/Next**: Manually navigate through solution steps
6. **Speed Slider**: Adjust playback speed (100-2000 ms between steps)
7. **Heuristic Dropdown**: Choose between Manhattan or Hamming distance

## Understanding the Display

- **Green tiles**: Numbers in the puzzle
- **Gray tile**: Empty space (0)
- **Info bar**: Shows current step, move direction, and A* costs:
  - `g`: Cost from start to current state
  - `h`: Estimated cost from current to goal (heuristic)
  - `f`: Total cost (g + h)

## Example Puzzle

The default puzzle:
```
1 2 3        1 2 3
0 4 6   →    4 5 6
7 5 8        7 8 0
```

Solution: 3 moves (Right → Down → Right)

## How A* Works in This Solver

1. **Start**: Begin with the initial puzzle state
2. **Evaluate**: Calculate f(n) = g(n) + h(n) for each state
   - g(n): Number of moves taken so far
   - h(n): Estimated moves remaining (Manhattan or Hamming)
3. **Explore**: Always pick the state with lowest f(n) value
4. **Expand**: Generate all possible moves (Up, Down, Left, Right)
5. **Track**: Keep visited states to avoid cycles
6. **Goal**: Continue until reaching the goal state

## Heuristics Explained

### Manhattan Distance
Calculates the sum of horizontal and vertical distances each tile must travel to reach its goal position. More accurate but slightly more computation.

### Hamming Distance
Counts how many tiles are in the wrong position (ignoring the blank). Simpler but less accurate heuristic.

Manhattan distance typically finds solutions faster because it provides better guidance to the goal state.

## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## Learning Points for Python/React Developers

### Python Concepts Used:
- **Classes and OOP**: PuzzleState class with dunder methods
- **heapq**: Priority queue for efficient state selection
- **Tuples**: Immutable board representation for hashing
- **List comprehensions**: Creating board copies
- **tkinter**: GUI development with event-driven programming

### Translating to React:
The GUI structure is similar to React components:
- State management (board state, solution path, animation)
- Event handlers (button clicks)
- Conditional rendering (enable/disable buttons)
- Animation with timers (similar to useEffect cleanup)

If you were to build this in React, you'd use:
- `useState` for board, solution, currentStep, isPlaying
- `useEffect` for animation timer
- Component composition for buttons and board display
- CSS-in-JS or Tailwind for styling
