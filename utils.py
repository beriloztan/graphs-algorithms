import pygame


def get_algorithm(name):
    """Returns the algorithm function by name."""
    from algorithms.bfs import bfs
    from algorithms.dfs import dfs
    from algorithms.dijkstra import dijkstra

    return {"BFS": bfs, "DFS": dfs, "Dijkstra": dijkstra}.get(name)


def handle_events_during_algo(visualizer):
    """Process events during algorithm animation (allow quit)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False  # Signal to stop
    return True
