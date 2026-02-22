import heapq

# Estado objetivo: 

GOAL = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

# Estado inicial según tu imagen:

START = (7, 2, 4,
         5, 6, 0,
         8, 3, 1)


def manhattan_distance(state):
    """Heurística: suma de distancias Manhattan de cada ficha a su posición objetivo."""
    dist = 0
    for idx, value in enumerate(state):
        if value == 0:
            continue
        # posición actual
        x, y = divmod(idx, 3)
        # posición objetivo
        gx, gy = divmod(value, 3)
        dist += abs(x - gx) + abs(y - gy)
    return dist


def get_neighbors(state):
    """Genera estados vecinos moviendo el espacio vacío (0)."""
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, 3)

    moves = []
    if x > 0:
        moves.append((-1, 0))  # arriba
    if x < 2:
        moves.append((1, 0))   # abajo
    if y > 0:
        moves.append((0, -1))  # izquierda
    if y < 2:
        moves.append((0, 1))   # derecha

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        new_index = nx * 3 + ny
        new_state = list(state)
        # intercambiar 0 con la ficha vecina
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))

    return neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(start, goal):
    """Algoritmo A* para el 8-puzzle."""
    open_set = []
    heapq.heappush(open_set, (manhattan_distance(start), 0, start))

    came_from = {}
    g_score = {start: 0}

    visited = set()

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None


def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else " " for x in row))
    print()


if __name__ == "__main__":
    print("Estado inicial:")
    print_state(START)
    print("Buscando solución con A* (heurística Manhattan)...\n")

    path = astar(START, GOAL)

    if path is None:
        print("No se encontró solución (estado no resoluble).")
    else:
        print(f"Solución encontrada en {len(path) - 1} pasos:\n")
        for step, state in enumerate(path):
            print(f"Paso {step}:")
            print_state(state)