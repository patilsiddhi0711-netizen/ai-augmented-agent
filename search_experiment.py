import cProfile
import heapq
import pstats
import time
from collections import deque

# --- 1. 8-PUZZLE ENVIRONMENT ---
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 represents the blank space


def get_neighbors(state):
    """Generates valid successor states for the blank space (0)."""
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)

    moves = {
        "UP": (row - 1, col),
        "DOWN": (row + 1, col),
        "LEFT": (row, col - 1),
        "RIGHT": (row, col + 1),
    }

    for _, (r, c) in moves.items():
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r * 3 + c
            state_list = list(state)
            state_list[idx], state_list[new_idx] = (
                state_list[new_idx],
                state_list[idx],
            )
            neighbors.append(tuple(state_list))

    return neighbors


def manhattan_distance(state):
    """Heuristic function h(n) for A* Search."""
    distance = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            target_row, target_col = divmod(val - 1, 3)
            current_row, current_col = divmod(i, 3)
            distance += abs(target_row - current_row) + abs(
                target_col - current_col
            )
    return distance


# --- 2. SEARCH ALGORITHMS ---


def run_bfs(start_state):
    """Breadth-First Search Algorithm."""
    nodes_expanded = 0
    queue = deque([(start_state, [])])
    visited = {start_state}

    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1

        if current == GOAL_STATE:
            return path + [current], nodes_expanded

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current]))

    return None, nodes_expanded


def run_astar(start_state):
    """A* Search Algorithm using Manhattan Distance Heuristic."""
    nodes_expanded = 0
    # Priority Queue tuple format: (f_score, g_score, current_state, path)
    pq = [(manhattan_distance(start_state), 0, start_state, [])]
    visited = {start_state: 0}

    while pq:
        f, g, current, path = heapq.heappop(pq)
        nodes_expanded += 1

        if current == GOAL_STATE:
            return path + [current], nodes_expanded

        for neighbor in get_neighbors(current):
            new_g = g + 1
            if neighbor not in visited or new_g < visited[neighbor]:
                visited[neighbor] = new_g
                h = manhattan_distance(neighbor)
                heapq.heappush(
                    pq, (new_g + h, new_g, neighbor, path + [current])
                )

    return None, nodes_expanded


# --- 3. EXPERIMENTAL BENCHMARKING SUITE ---


def benchmark_case(case_name, start_state, iterations=100):
    print(f"\n==========================================")
    print(f" TESTING: {case_name}")
    print(f" Initial State: {start_state}")
    print(f"==========================================")

    # --- Run BFS ---
    start_time = time.perf_counter()
    for _ in range(iterations):
        bfs_path, bfs_nodes = run_bfs(start_state)
    end_time = time.perf_counter()
    bfs_avg_time = ((end_time - start_time) / iterations) * 1000  # Convert to ms

    # --- Run A* ---
    start_time = time.perf_counter()
    for _ in range(iterations):
        astar_path, astar_nodes = run_astar(start_state)
    end_time = time.perf_counter()
    astar_avg_time = (
        (end_time - start_time) / iterations
    ) * 1000  # Convert to ms

    # Output Comparative Results
    print(f"{'Metric':<25} | {'BFS':<15} | {'A* Search':<15}")
    print("-" * 60)
    print(
        f"{'Solution Path Length':<25} | {len(bfs_path)-1 if bfs_path else 0:<15} | {len(astar_path)-1 if astar_path else 0:<15}"
    )
    print(
        f"{'Nodes Expanded':<25} | {bfs_nodes:<15} | {astar_nodes:<15}"
    )
    print(
        f"{'Avg Execution Time (ms)':<25} | {bfs_avg_time:<15.4f} | {astar_avg_time:<15.4f}"
    )


if __name__ == "__main__":
    # Test Cases for Best, Average, and Worst Scenarios
    TEST_CASES = {
        "BEST CASE (0 moves)": (1, 2, 3, 4, 5, 6, 7, 8, 0),
        "AVERAGE CASE (~12 moves)": (1, 2, 3, 4, 0, 6, 7, 5, 8),
        "WORST CASE (~20 moves)": (8, 6, 7, 2, 5, 4, 3, 0, 1),
    }

    # 1. Run Empirical Benchmarks
    for name, state in TEST_CASES.items():
        # Lower iteration count for worst case to save computation time
        iters = 1 if "WORST" in name else 100
        benchmark_case(name, state, iterations=iters)

    # 2. Run Built-in cProfile on Average Case
    print("\n\n------------------------------------------")
    print(" RUNNING CPROFILE ON AVERAGE CASE ")
    print("------------------------------------------")
    profiler = cProfile.Profile()
    profiler.enable()

    # Profile average case workload
    run_bfs((1, 2, 3, 4, 0, 6, 7, 5, 8))
    run_astar((1, 2, 3, 4, 0, 6, 7, 5, 8))

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats(10)