import heapq
from itertools import count

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0) # 0 represents the blank tile

MOVES = { # blank moves: name -> (row change, col change)
    "Up": (-1, 0),
    "Down": (1, 0),
    "Left": (0, -1),
    "Right": (0, 1),
}


# ---------------- Heuristics ----------------


def manhattan_distance(state, goal=GOAL):
    """Sum of |row difference| + |column difference| for every tile (excluding blank)."""
    goal_pos = {tile: (i // 3, i % 3) for i, tile in enumerate(goal)}
    total = 0
    for i, tile in enumerate(state):
        if tile != 0:
            r, c = divmod(i, 3)
            gr, gc = goal_pos[tile]
            total += abs(r - gr) + abs(c - gc)
    return total


# ---------------- Helpers ----------------
def get_neighbors(state):
    """Yield (move_name, next_state) for every legal blank move."""
    b = state.index(0)
    r, c = divmod(b, 3)
    for move, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nb = nr * 3 + nc
            s = list(state)
            s[b], s[nb] = s[nb], s[b]
            yield move, tuple(s)


def is_solvable(state, goal=GOAL):
    """An 8-puzzle is solvable iff start and goal have the same inversion parity."""
    def inversions(s):
        tiles = [t for t in s if t != 0]
        return sum(1 for i in range(len(tiles))
                   for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inversions(state) % 2 == inversions(goal) % 2


def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join("_" if t == 0 else str(t) for t in state[i:i + 3]))
    print()


# ---------------- A* Search ----------------
def a_star(start, heuristic, goal=GOAL):
    """
    Returns (path_of_moves, list_of_states, nodes_expanded) or None if unsolvable.
    f(n) = g(n) + h(n), where g(n) = depth of the node.
    """
    if not is_solvable(start, goal):
        return None

    tie = count() # tie-breaker for equal f
    g_start = 0
    open_list = [(g_start + heuristic(start, goal), next(tie), g_start, start)]
    parent = {start: (None, None)} # state -> (prev_state, move)
    best_g = {start: 0}
    closed = set()
    expanded = 0

    while open_list:
        f, _, g, state = heapq.heappop(open_list)
        if state in closed:
            continue
        if state == goal:
            # Reconstruct path
            moves, states = [], [state]
            while parent[state][0] is not None:
                prev, move = parent[state]
                moves.append(move)
                states.append(prev)
                state = prev
            return moves[::-1], states[::-1], expanded

        closed.add(state)
        expanded += 1

        for move, nxt in get_neighbors(state):
            new_g = g + 1 # depth increases by 1
            if nxt not in closed and new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                parent[nxt] = (state, move)
                f_nxt = new_g + heuristic(nxt, goal)
                heapq.heappush(open_list, (f_nxt, next(tie), new_g, nxt))
    return None


def solve(start, heuristic, name):
    print("=" * 45)
    print(f"A* with g(n) = depth, h(n) = {name}")
    print("=" * 45)
    result = a_star(start, heuristic)
    if result is None:
        print("This puzzle is not solvable.\n")
        return
    moves, states, expanded = result
    for step, s in enumerate(states):
        g = step
        h = heuristic(s)
        label = "Start" if step == 0 else f"Step {step}: move blank {moves[step - 1]}"
        print(f"{label} g={g}, h={h}, f={g + h}")
        print_state(s)
    print(f"Solution depth (moves): {len(moves)}")
    print(f"Moves: {' -> '.join(moves)}")
    print(f"Nodes expanded: {expanded}\n")


# ---------------- Main ----------------
if __name__ == "__main__":
    # Example start state (0 = blank)
    start = (1, 2, 3,
             0, 4, 6,
             7, 5, 8)

    # To enter your own: uncomment the line below and type 9 numbers, e.g. 1 2 3 0 4 6 7 5 8
    # start = tuple(map(int, input("Enter start state (0 = blank): ").split()))

    print("Initial state:")
    print_state(start)
    print("Goal state:")
    print_state(GOAL)

    solve(start, manhattan_distance, "Manhattan Distance")

    # Comparison on a harder puzzle
    hard = (8, 6, 7, 2, 5, 4, 3, 0, 1)
    print("Comparison on a harder puzzle:", hard)
    for name, h in [("Manhattan Distance", manhattan_distance)]:
        moves, _, expanded = a_star(hard, h)
        print(f" {name:20s} -> depth {len(moves)}, nodes expanded {expanded}")
