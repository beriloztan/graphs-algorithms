import heapq


def dijkstra(grid, draw_callback):
    """
    Dijkstra's Algorithm
    Finds shortest path on weighted graphs (all weights = 1 here).
    Uses a min-heap priority queue.
    Time complexity: O(E log V)
    """
    start = grid.start
    goal = grid.goal

    if not start or not goal:
        return None, []

    start.g_cost = 0
    heap = [(0, start)]
    visited = set()
    visited_order = []

    while heap:
        cost, node = heapq.heappop(heap)

        if node in visited:
            continue
        visited.add(node)
        node.visited = True

        if node == goal:
            path = reconstruct_path(goal)
            return path, visited_order

        for neighbor in grid.get_neighbors(node):
            if neighbor not in visited:
                new_cost = cost + 1  # uniform weight
                if new_cost < neighbor.g_cost:
                    neighbor.g_cost = new_cost
                    neighbor.parent = node
                    heapq.heappush(heap, (new_cost, neighbor))
                    if neighbor != goal:
                        visited_order.append(neighbor)

        if draw_callback:
            draw_callback(visited_order, [], [])

    return None, visited_order  # No path found


def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]
