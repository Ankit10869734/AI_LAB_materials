import numpy as np
import matplotlib.pyplot as plt
import random

def f(x):
    """Objective function: f(x) = -x^4 + 4x^3 + 10"""
    return -x**4 + 4*x**3 + 10

def get_neighbors(x, delta=0.1):
    """Generate neighbors by moving left and right by delta"""
    return [x - delta, x + delta]

def hill_climbing(x_min=-2, x_max=5, delta=0.1):
    """Hill Climbing algorithm implementation"""
    # Random starting point
    current_x = random.uniform(x_min, x_max)
    start_x = current_x
    current_score = f(current_x)
    path = [current_x]
    
    while True:
        # Generate neighbors
        neighbors = get_neighbors(current_x, delta)
        
        # Filter neighbors to stay within bounds
        neighbors = [n for n in neighbors if x_min <= n <= x_max]
        
        # Evaluate neighbors
        neighbor_scores = [(n, f(n)) for n in neighbors]
        
        # Find best neighbor
        best_neighbor, best_score = max(neighbor_scores, key=lambda x: x[1])
        
        # If no improvement, stop
        if best_score <= current_score:
            break
        
        # Move to best neighbor
        current_x = best_neighbor
        current_score = best_score
        path.append(current_x)
    
    return start_x, current_x, current_score, path

def plot_function():
    """Plot the function f(x) in the range [-2, 5]"""
    x = np.linspace(-2, 5, 1000)
    y = f(x)
    
    # Find global maximum
    max_idx = np.argmax(y)
    global_max_x = x[max_idx]
    global_max_y = y[max_idx]
    
    # Find local maxima by checking derivatives
    local_maxima = []
    for i in range(1, len(x) - 1):
        if y[i] > y[i-1] and y[i] > y[i+1]:
            # Check if it's a significant peak (not the global max)
            if abs(x[i] - global_max_x) > 0.5:
                local_maxima.append((x[i], y[i]))
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='f(x)')
    
    # Mark global maximum
    plt.plot(global_max_x, global_max_y, 'r*', markersize=20, 
             label=f'Global Maximum (x={global_max_x:.2f}, f(x)={global_max_y:.2f})')
    
    # Mark local maxima if any
    for lm_x, lm_y in local_maxima:
        plt.plot(lm_x, lm_y, 'go', markersize=12, 
                 label=f'Local Maximum (x={lm_x:.2f}, f(x)={lm_y:.2f})')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Function: f(x) = -x^4 + 4x^3 + 10')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    plt.savefig('function_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_with_path(path):
    """Plot function with Hill Climbing path"""
    x = np.linspace(-2, 5, 1000)
    y = f(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='f(x)')
    
    # Plot path
    path_y = [f(px) for px in path]
    plt.plot(path, path_y, 'ro-', linewidth=1.5, markersize=6, label='Hill Climbing Path')
    plt.plot(path[0], path_y[0], 'go', markersize=10, label='Start')
    plt.plot(path[-1], path_y[-1], 'rs', markersize=10, label='End')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Hill Climbing Path Visualization')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('path_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

def run_multiple_experiments(n_runs=10):
    """Run Hill Climbing multiple times and record results"""
    results = []
    
    
    print(f"{'Run':<5} {'Start x':<12} {'Final x':<12} {'f(x)':<12}")
    
    
    for i in range(1, n_runs + 1):
        start_x, final_x, final_score, path = hill_climbing()
        results.append((i, start_x, final_x, final_score, path))
        print(f"{i:<5} {start_x:<12.6f} {final_x:<12.6f} {final_score:<12.6f}")
    
    return results

def analyze_results(results):
    """Analyze and explain the results"""
    final_values = [r[2] for r in results]
    final_scores = [r[3] for r in results]
    
    print("\n\nAnalysis:")
    print(f"Minimum final x: {min(final_values):.6f}")
    print(f"Maximum final x: {max(final_values):.6f}")
    print(f"Minimum f(x): {min(final_scores):.6f}")
    print(f"Maximum f(x): {max(final_scores):.6f}")
    print(f"Number of unique solutions: {len(set([round(x, 4) for x in final_values]))}")
    
    
    
   
def main():
    # Task 1: Plot the function
    
    plot_function()
    
    
    # Task 3 & 4: Run Hill Climbing multiple times
    
    results = run_multiple_experiments(10)
    
    # Task 5: Visualize one run with path
    
    _, _, _, sample_path = hill_climbing()
    plot_with_path(sample_path)
    
    
    # Analysis
    analyze_results(results)
    
   
    

if __name__ == "__main__":
    main()
