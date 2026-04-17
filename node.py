class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.parent = None
        self.is_wall = False
        self.is_start = False
        self.is_goal = False
        self.g_cost = float('inf')  # For Dijkstra

    def reset(self):
        self.visited = False
        self.parent = None
        self.g_cost = float('inf')

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __lt__(self, other):
        return self.g_cost < other.g_cost

    def __repr__(self):
        return f"Node({self.row}, {self.col})"
