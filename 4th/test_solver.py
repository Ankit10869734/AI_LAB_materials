from puzzle_solver import PuzzleState, a_star_solver, manhattan_distance, hamming_distance

# Test the solver
initial_board = (
    (1, 2, 3),
    (0, 4, 6),
    (7, 5, 8)
)

goal_board = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

print("Initial Board:")
PuzzleState(initial_board).print_board()
print("\nGoal Board:")
PuzzleState(goal_board).print_board()

print("\n" + "="*50)
print("Solving with A* (Manhattan Distance)...")
print("="*50)
solution_path = a_star_solver(initial_board, goal_board, heuristic_func=manhattan_distance)

if solution_path:
    print(f"\nSolution Found in {len(solution_path) - 1} moves:\n")
    for i, state in enumerate(solution_path):
        if i == 0:
            print(f"-- Initial State -- (g={state.g}, h={state.h}, f={state.f})")
        else:
            print(f"\n-- Move {i}: {state.move} -- (g={state.g}, h={state.h}, f={state.f})")
        state.print_board()
else:
    print("No solution found.")

print("\n" + "="*50)
print("Solving with A* (Hamming Distance)...")
print("="*50)
solution_path_hamming = a_star_solver(initial_board, goal_board, heuristic_func=hamming_distance)

if solution_path_hamming:
    print(f"\nSolution Found in {len(solution_path_hamming) - 1} moves using Hamming Distance")
else:
    print("No solution found with Hamming Distance heuristic.")
