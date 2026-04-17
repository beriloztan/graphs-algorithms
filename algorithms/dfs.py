def dfs(grid, draw_callback):
    """
    Depth-First Search
    Does NOT guarantee shortest path.
    Uses a stack (iterative implementation to avoid recursion limit).
    Time complexity: O(V + E)
    """
    start = grid.start
    goal = grid.goal

    if not start or not goal:
        return None, []

    stack = [start]
    visited = {start}
    visited_order = []

    while stack:
        node = stack.pop()

        if node == goal:
            path = reconstruct_path(goal)
            return path, visited_order

        for neighbor in grid.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = node
                neighbor.visited = True
                stack.append(neighbor)
                if neighbor != goal:
                    visited_order.append(neighbor)

        if draw_callback:
            draw_callback(visited_order, [n for n in stack if n != goal], [])

    return None, visited_order  # No path found


def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]
