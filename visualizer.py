import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (66, 135, 245)        # visited
LIGHT_BLUE = (173, 216, 230) # frontier
GREEN = (50, 205, 50)        # final path
RED = (220, 50, 50)          # goal
ORANGE = (255, 165, 0)       # start
YELLOW = (255, 220, 0)       # frontier highlight
PURPLE = (150, 50, 200)      # dijkstra visited
BG_COLOR = (30, 30, 30)
PANEL_COLOR = (45, 45, 45)
BORDER_COLOR = (80, 80, 80)

CELL_SIZE = 20
PANEL_HEIGHT = 90
FONT_SIZE = 18
TITLE_FONT_SIZE = 22


class Visualizer:
    def __init__(self, grid):
        self.grid = grid
        self.width = grid.cols * CELL_SIZE
        self.height = grid.rows * CELL_SIZE + PANEL_HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Search & Pathfinding Visualizer")
        self.font = pygame.font.SysFont("Segoe UI", FONT_SIZE)
        self.title_font = pygame.font.SysFont("Segoe UI", TITLE_FONT_SIZE, bold=True)
        self.clock = pygame.time.Clock()
        self.selected_algo = "BFS"
        self.mode = "wall"  # "wall", "start", "goal"
        self.status = "Set start (S), goal (G), draw walls, then press SPACE"
        self.path_nodes = []
        self.visited_nodes = []
        self.frontier_nodes = []
        self.running_algo = False

    def draw_grid(self):
        self.screen.fill(BG_COLOR)
        # Draw cells
        for row in self.grid.nodes:
            for node in row:
                self._draw_node(node)

        # Draw grid lines
        for r in range(self.grid.rows + 1):
            pygame.draw.line(self.screen, DARK_GRAY,
                             (0, r * CELL_SIZE),
                             (self.width, r * CELL_SIZE))
        for c in range(self.grid.cols + 1):
            pygame.draw.line(self.screen, DARK_GRAY,
                             (c * CELL_SIZE, 0),
                             (c * CELL_SIZE, self.grid.rows * CELL_SIZE))

        self._draw_panel()
        pygame.display.flip()

    def _draw_node(self, node):
        x = node.col * CELL_SIZE
        y = node.row * CELL_SIZE
        rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 1, CELL_SIZE - 1)

        if node.is_start:
            pygame.draw.rect(self.screen, ORANGE, rect)
            # Draw 'S' label
            label = self.font.render("S", True, BLACK)
            self.screen.blit(label, (x + 5, y + 3))
        elif node.is_goal:
            pygame.draw.rect(self.screen, RED, rect)
            label = self.font.render("G", True, WHITE)
            self.screen.blit(label, (x + 5, y + 3))
        elif node.is_wall:
            pygame.draw.rect(self.screen, BLACK, rect)
        elif node in self.path_nodes:
            pygame.draw.rect(self.screen, GREEN, rect)
        elif node in self.frontier_nodes:
            pygame.draw.rect(self.screen, YELLOW, rect)
        elif node in self.visited_nodes:
            if self.selected_algo == "Dijkstra":
                pygame.draw.rect(self.screen, PURPLE, rect)
            else:
                pygame.draw.rect(self.screen, BLUE, rect)
        else:
            pygame.draw.rect(self.screen, WHITE, rect)

    def _draw_panel(self):
        panel_y = self.grid.rows * CELL_SIZE
        panel_rect = pygame.Rect(0, panel_y, self.width, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect)
        pygame.draw.line(self.screen, BORDER_COLOR, (0, panel_y), (self.width, panel_y), 2)

        # Algorithm buttons
        algos = ["BFS", "DFS", "Dijkstra"]
        btn_w, btn_h = 90, 30
        btn_y = panel_y + 10
        for i, algo in enumerate(algos):
            btn_x = 10 + i * (btn_w + 8)
            color = ORANGE if self.selected_algo == algo else DARK_GRAY
            border = ORANGE if self.selected_algo == algo else GRAY
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, border, btn_rect, 2, border_radius=5)
            label = self.font.render(algo, True, WHITE if self.selected_algo != algo else BLACK)
            self.screen.blit(label, (btn_x + btn_w // 2 - label.get_width() // 2,
                                     btn_y + btn_h // 2 - label.get_height() // 2))

        # Mode buttons
        modes = [("Wall", "wall"), ("Start", "start"), ("Goal", "goal")]
        for i, (label_text, mode_key) in enumerate(modes):
            btn_x = 310 + i * (btn_w + 8)
            color = LIGHT_BLUE if self.mode == mode_key else DARK_GRAY
            border = LIGHT_BLUE if self.mode == mode_key else GRAY
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, border, btn_rect, 2, border_radius=5)
            lbl = self.font.render(label_text, True, BLACK if self.mode == mode_key else WHITE)
            self.screen.blit(lbl, (btn_x + btn_w // 2 - lbl.get_width() // 2,
                                   btn_y + btn_h // 2 - lbl.get_height() // 2))

        # Action buttons
        actions = [("SPACE: Run", GREEN), ("R: Reset Search", GRAY), ("C: Clear All", GRAY)]
        for i, (text, color) in enumerate(actions):
            btn_x = 620 + i * 135
            lbl = self.font.render(text, True, color)
            self.screen.blit(lbl, (btn_x, btn_y + 8))

        # Status bar
        status_y = panel_y + 55
        status_surf = self.font.render(self.status, True, YELLOW)
        self.screen.blit(status_surf, (10, status_y))

        # Legend
        legend = [
            (ORANGE, "Start"), (RED, "Goal"), (BLACK, "Wall"),
            (BLUE, "Visited"), (YELLOW, "Frontier"), (GREEN, "Path"),
        ]
        legend_x = self.width - 10
        for color, text in reversed(legend):
            lbl = self.font.render(text, True, WHITE)
            legend_x -= lbl.get_width() + 20
            pygame.draw.rect(self.screen, color, pygame.Rect(legend_x - 14, status_y + 2, 12, 12))
            self.screen.blit(lbl, (legend_x, status_y))

    def get_cell_from_mouse(self, pos):
        x, y = pos
        if y >= self.grid.rows * CELL_SIZE:
            return None
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row, col

    def handle_panel_click(self, pos):
        panel_y = self.grid.rows * CELL_SIZE
        x, y = pos
        if y < panel_y or y > panel_y + 50:
            return

        algos = ["BFS", "DFS", "Dijkstra"]
        btn_w, btn_h = 90, 30
        btn_y = panel_y + 10
        for i, algo in enumerate(algos):
            btn_x = 10 + i * (btn_w + 8)
            if btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h:
                self.selected_algo = algo
                self.status = f"{algo} selected. Press SPACE to run."
                return

        modes = [("Wall", "wall"), ("Start", "start"), ("Goal", "goal")]
        for i, (_, mode_key) in enumerate(modes):
            btn_x = 310 + i * (btn_w + 8)
            if btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h:
                self.mode = mode_key
                return

    def animate_search(self, visited_order, frontier, path):
        self.visited_nodes = list(visited_order)
        self.frontier_nodes = list(frontier)
        self.draw_grid()
        self.clock.tick(60)

    def draw_path(self, path):
        self.path_nodes = path
        self.draw_grid()
