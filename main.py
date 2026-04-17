import pygame
import sys
from grid import Grid
from visualizer import Visualizer
from utils import get_algorithm, handle_events_during_algo

ANIMATION_DELAY_MS = 5  # milliseconds between each step


def run_algorithm(visualizer, grid):
    algo_fn = get_algorithm(visualizer.selected_algo)
    if not algo_fn:
        return

    grid.reset_search()
    visualizer.path_nodes = []
    visualizer.visited_nodes = []
    visualizer.frontier_nodes = []
    visualizer.status = f"Running {visualizer.selected_algo}..."
    visualizer.running_algo = True

    # Collect all steps first, then animate
    steps = []  # list of (visited_snapshot, frontier_snapshot)

    # We'll run the algorithm and capture steps via callback
    visited_so_far = []
    frontier_so_far = []

    def step_callback(visited, frontier, path):
        steps.append((list(visited), list(frontier)))

    path, visited_order = algo_fn(grid, step_callback)

    # Animate the recorded steps
    for visited_snap, frontier_snap in steps:
        if not handle_events_during_algo(visualizer):
            visualizer.running_algo = False
            return
        visualizer.visited_nodes = visited_snap
        visualizer.frontier_nodes = frontier_snap
        visualizer.draw_grid()
        pygame.time.delay(ANIMATION_DELAY_MS)

    # Show final state
    visualizer.visited_nodes = visited_order
    visualizer.frontier_nodes = []

    if path:
        # Animate path drawing
        for i in range(1, len(path) - 1):  # skip start and goal nodes
            if not handle_events_during_algo(visualizer):
                break
            visualizer.path_nodes = path[1:i + 1]
            visualizer.draw_grid()
            pygame.time.delay(30)
        visualizer.path_nodes = path[1:-1]  # final path without start/goal markers
        visualizer.status = (
            f"{visualizer.selected_algo} done! "
            f"Path length: {len(path) - 1} steps | "
            f"Nodes visited: {len(visited_order)}"
        )
    else:
        visualizer.status = f"{visualizer.selected_algo}: No path found!"

    visualizer.running_algo = False
    visualizer.draw_grid()


def main():
    grid = Grid()
    vis = Visualizer(grid)

    mouse_held = False
    mouse_button = None

    while True:
        vis.draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---------- Keyboard ----------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not vis.running_algo:
                    if not grid.start or not grid.goal:
                        vis.status = "Please set a start (S mode) and goal (G mode) first!"
                    else:
                        run_algorithm(vis, grid)

                elif event.key == pygame.K_r and not vis.running_algo:
                    grid.reset_search()
                    vis.path_nodes = []
                    vis.visited_nodes = []
                    vis.frontier_nodes = []
                    vis.status = "Search reset. Press SPACE to run again."

                elif event.key == pygame.K_c and not vis.running_algo:
                    grid.full_reset()
                    vis.path_nodes = []
                    vis.visited_nodes = []
                    vis.frontier_nodes = []
                    vis.status = "Cleared. Set start, goal and walls."

                elif event.key == pygame.K_1:
                    vis.selected_algo = "BFS"
                    vis.status = "BFS selected."
                elif event.key == pygame.K_2:
                    vis.selected_algo = "DFS"
                    vis.status = "DFS selected."
                elif event.key == pygame.K_3:
                    vis.selected_algo = "Dijkstra"
                    vis.status = "Dijkstra selected."
                elif event.key == pygame.K_w:
                    vis.mode = "wall"
                elif event.key == pygame.K_s:
                    vis.mode = "start"
                elif event.key == pygame.K_g:
                    vis.mode = "goal"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # ---------- Mouse ----------
            if event.type == pygame.MOUSEBUTTONDOWN and not vis.running_algo:
                mouse_held = True
                mouse_button = event.button
                pos = event.pos
                panel_y = grid.rows * 20  # CELL_SIZE = 20
                if pos[1] >= panel_y:
                    vis.handle_panel_click(pos)
                else:
                    cell = vis.get_cell_from_mouse(pos)
                    if cell:
                        row, col = cell
                        if vis.mode == "start":
                            grid.set_start(row, col)
                        elif vis.mode == "goal":
                            grid.set_goal(row, col)
                        elif vis.mode == "wall":
                            grid.toggle_wall(row, col)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
                mouse_button = None

            if event.type == pygame.MOUSEMOTION and mouse_held and not vis.running_algo:
                pos = event.pos
                cell = vis.get_cell_from_mouse(pos)
                if cell and vis.mode == "wall":
                    row, col = cell
                    node = grid.get_node(row, col)
                    if node and not node.is_start and not node.is_goal:
                        if mouse_button == 1:
                            node.is_wall = True
                        elif mouse_button == 3:
                            node.is_wall = False

        vis.clock.tick(60)


if __name__ == "__main__":
    main()
