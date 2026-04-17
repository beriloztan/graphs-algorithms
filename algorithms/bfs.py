from collections import deque


def bfs(grid, draw_callback):
    """
    Breadth-First Search
    Guarantees shortest path on unweighted graphs.
    Time complexity: O(V + E)
    """
    start = grid.start
    goal = grid.goal

    if not start or not goal:
        return None, []

    queue = deque([start])
    visited = {start}
    visited_order = []

    while queue:
        node = queue.popleft()

        if node == goal:
            path = reconstruct_path(goal)
            return path, visited_order

        for neighbor in grid.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = node
                neighbor.visited = True
                queue.append(neighbor)
                if neighbor != goal:
                    visited_order.append(neighbor)

        if draw_callback:
            draw_callback(visited_order, [n for n in queue if n != goal], [])

    return None, visited_order  # No path found


def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]
