from node import Node

ROWS = 30
COLS = 50


class Grid:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(r, c) for c in range(cols)] for r in range(rows)]
        self.start = None
        self.goal = None

    def get_node(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.nodes[row][col]
        return None

    def get_neighbors(self, node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for dr, dc in directions:
            neighbor = self.get_node(node.row + dr, node.col + dc)
            if neighbor and not neighbor.is_wall:
                neighbors.append(neighbor)
        return neighbors

    def set_start(self, row, col):
        if self.start:
            self.start.is_start = False
        node = self.get_node(row, col)
        if node and not node.is_wall and not node.is_goal:
            node.is_start = True
            self.start = node

    def set_goal(self, row, col):
        if self.goal:
            self.goal.is_goal = False
        node = self.get_node(row, col)
        if node and not node.is_wall and not node.is_start:
            node.is_goal = True
            self.goal = node

    def toggle_wall(self, row, col):
        node = self.get_node(row, col)
        if node and not node.is_start and not node.is_goal:
            node.is_wall = not node.is_wall

    def reset_search(self):
        for row in self.nodes:
            for node in row:
                node.reset()

    def clear_walls(self):
        for row in self.nodes:
            for node in row:
                if not node.is_start and not node.is_goal:
                    node.is_wall = False
        self.reset_search()

    def full_reset(self):
        self.nodes = [[Node(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.start = None
        self.goal = None
