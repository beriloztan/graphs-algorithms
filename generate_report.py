from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "C:/Users/beril.oztan/Desktop/graph-algorithms/Project_Report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.5 * cm,
    rightMargin=2.5 * cm,
    topMargin=2.5 * cm,
    bottomMargin=2.5 * cm,
)

styles = getSampleStyleSheet()
W = A4[0] - 5 * cm  # usable width

# ── Custom styles ────────────────────────────────────────────────────────────
title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=22,
    leading=28,
    textColor=colors.HexColor("#1a1a2e"),
    spaceAfter=4,
    alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=11,
    leading=16,
    textColor=colors.HexColor("#4a4a6a"),
    spaceAfter=2,
    alignment=TA_CENTER,
)
h1_style = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#16213e"),
    spaceBefore=18,
    spaceAfter=6,
    borderPad=0,
)
h2_style = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#0f3460"),
    spaceBefore=12,
    spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#2c2c2c"),
    alignment=TA_JUSTIFY,
    spaceAfter=6,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=18,
    bulletIndent=6,
    spaceAfter=3,
)
code_style = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontSize=8.5,
    leading=12,
    backColor=colors.HexColor("#f4f4f8"),
    borderColor=colors.HexColor("#ccccdd"),
    borderWidth=0.5,
    borderPad=6,
    fontName="Courier",
    spaceAfter=8,
)
link_style = ParagraphStyle(
    "Link",
    parent=body_style,
    textColor=colors.HexColor("#0066cc"),
)
info_box_style = ParagraphStyle(
    "InfoBox",
    parent=body_style,
    backColor=colors.HexColor("#eef4ff"),
    borderColor=colors.HexColor("#3a86ff"),
    borderWidth=1,
    borderPad=8,
    spaceAfter=10,
)

def hr():
    return HRFlowable(width="100%", thickness=1,
                      color=colors.HexColor("#ccccdd"), spaceAfter=6)

def h1(text):
    return Paragraph(text, h1_style)

def h2(text):
    return Paragraph(text, h2_style)

def body(text):
    return Paragraph(text, body_style)

def bullet(text):
    return Paragraph(f"&bull; &nbsp; {text}", bullet_style)

def code(text):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)

def sp(n=8):
    return Spacer(1, n)

# ── Content ──────────────────────────────────────────────────────────────────
story = []

# ── Cover / Header ───────────────────────────────────────────────────────────
story.append(sp(20))
story.append(Paragraph("Artificial Intelligence in Action", title_style))
story.append(Paragraph("Applied Programming Project Report", subtitle_style))
story.append(sp(6))
story.append(Paragraph("Search &amp; Pathfinding Visualizer", ParagraphStyle(
    "Sub2", parent=subtitle_style, fontSize=13,
    textColor=colors.HexColor("#0f3460"), spaceBefore=0)))
story.append(sp(10))

# Info table
info_data = [
    ["Student", "Beril Oztan"],
    ["Topic", "Search & Pathfinding Visualizer (Topic 2)"],
    ["Language", "Python 3 with Pygame"],
    ["Algorithms", "BFS, DFS, Dijkstra's Shortest Path"],
    ["GitHub", "https://github.com/beriloztan/graphs-algorithms"],
    ["Demo Video", "https://youtu.be/_DrxCjlE78g"],
]
info_table = Table(
    [[Paragraph(k, ParagraphStyle("TK", parent=body_style, fontName="Helvetica-Bold")),
      Paragraph(v, link_style if "http" in v else body_style)]
     for k, v in info_data],
    colWidths=[3.5 * cm, W - 3.5 * cm],
)
info_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef4ff")),
    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f9f9ff")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccccdd")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(info_table)
story.append(sp(16))
story.append(hr())

# ── 1. Introduction ──────────────────────────────────────────────────────────
story.append(h1("1. Introduction"))
story.append(body(
    "This project was developed as part of the <i>Artificial Intelligence in Action</i> "
    "Applied Programming Project assignment. The goal of the assignment is to bridge the "
    "gap between theoretical AI concepts and practical software development by implementing "
    "one of the core algorithms covered in the course."
))
story.append(body(
    "The chosen topic is <b>Topic 2 — Search &amp; Pathfinding Visualizer</b>. The "
    "application allows users to interactively build a grid environment with custom "
    "obstacles, then observe how three classical graph-traversal algorithms — "
    "Breadth-First Search (BFS), Depth-First Search (DFS), and Dijkstra's Shortest "
    "Path Algorithm — navigate from a start node to a goal node, with real-time "
    "step-by-step animation."
))

# ── 2. Problem Description ───────────────────────────────────────────────────
story.append(h1("2. Problem Description"))
story.append(body(
    "Pathfinding is one of the most fundamental problems in computer science and AI. "
    "Given a grid or graph, the challenge is to find a route from a source node to a "
    "target node while avoiding blocked cells (walls). This problem arises in robotics, "
    "GPS navigation, video games, and network routing."
))
story.append(body(
    "The application models the environment as a <b>30 x 50 grid</b>, where each cell "
    "is a graph node connected to its four cardinal neighbours (up, down, left, right). "
    "The user designates a start cell, a goal cell, and any number of wall cells. "
    "Pressing SPACE triggers the selected algorithm, which then searches for a path."
))

# ── 3. Theoretical Background ────────────────────────────────────────────────
story.append(h1("3. Theoretical Background"))

story.append(h2("3.1 Breadth-First Search (BFS)"))
story.append(body(
    "BFS explores the graph level by level using a <b>FIFO queue</b>. It visits all "
    "nodes at distance <i>d</i> from the source before visiting any node at distance "
    "<i>d + 1</i>. Because every edge has the same cost (= 1) in an unweighted grid, "
    "BFS is guaranteed to find the <b>shortest path</b>."
))
story.append(body(
    "<b>Time Complexity:</b> O(V + E) &nbsp;&nbsp; "
    "<b>Space Complexity:</b> O(V) &nbsp;&nbsp; "
    "<b>Optimal:</b> Yes (uniform cost) &nbsp;&nbsp; "
    "<b>Complete:</b> Yes"
))

story.append(h2("3.2 Depth-First Search (DFS)"))
story.append(body(
    "DFS explores as far as possible along each branch before backtracking, using a "
    "<b>LIFO stack</b>. An iterative implementation is used here to avoid Python's "
    "recursion limit on large grids. DFS is <b>not</b> guaranteed to find the shortest "
    "path; the returned path depends on the order neighbours are explored."
))
story.append(body(
    "<b>Time Complexity:</b> O(V + E) &nbsp;&nbsp; "
    "<b>Space Complexity:</b> O(V) &nbsp;&nbsp; "
    "<b>Optimal:</b> No &nbsp;&nbsp; "
    "<b>Complete:</b> Yes (finite graphs)"
))

story.append(h2("3.3 Dijkstra's Shortest Path Algorithm"))
story.append(body(
    "Dijkstra's algorithm generalises BFS to <b>weighted graphs</b>. It maintains a "
    "<b>min-heap priority queue</b> ordered by cumulative cost g(n). At each step the "
    "node with the smallest known cost is expanded. In this implementation all edge "
    "weights are 1, making the result equivalent to BFS — but the full weighted "
    "generalisation is implemented and visible through the purple visited-node colour."
))
story.append(body(
    "<b>Time Complexity:</b> O(E log V) &nbsp;&nbsp; "
    "<b>Space Complexity:</b> O(V) &nbsp;&nbsp; "
    "<b>Optimal:</b> Yes (non-negative weights) &nbsp;&nbsp; "
    "<b>Complete:</b> Yes"
))

# Comparison table
story.append(sp(4))
comp_header = ["Property", "BFS", "DFS", "Dijkstra"]
comp_rows = [
    ["Data structure", "Queue (FIFO)", "Stack (LIFO)", "Min-Heap"],
    ["Optimal (shortest path)", "Yes", "No", "Yes"],
    ["Complete", "Yes", "Yes", "Yes"],
    ["Time complexity", "O(V + E)", "O(V + E)", "O(E log V)"],
    ["Best for", "Unweighted grid", "Exploring space", "Weighted graph"],
]
comp_table = Table(
    [[Paragraph(c, ParagraphStyle("TH", parent=body_style, fontName="Helvetica-Bold",
                                   textColor=colors.white)) for c in comp_header]] +
    [[Paragraph(cell, body_style) for cell in row] for row in comp_rows],
    colWidths=[3.5 * cm, (W - 3.5 * cm) / 3, (W - 3.5 * cm) / 3, (W - 3.5 * cm) / 3],
    repeatRows=1,
)
comp_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f3460")),
    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9ff")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9f9ff"), colors.HexColor("#eef4ff")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccccdd")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(comp_table)
story.append(sp(10))

# ── 4. Application Features ──────────────────────────────────────────────────
story.append(h1("4. Application Features"))
features = [
    "<b>Interactive grid editor</b> — click/drag to draw or erase walls; dedicated buttons for Wall, Start, and Goal modes.",
    "<b>Algorithm selection</b> — switch between BFS, DFS, and Dijkstra at runtime via keyboard shortcuts (1 / 2 / 3) or on-screen buttons.",
    "<b>Step-by-step animation</b> — visited nodes and the active frontier are rendered frame by frame so the exploration pattern is clearly visible.",
    "<b>Colour-coded visualisation</b> — orange = start, red = goal, black = wall, blue/purple = visited, yellow = frontier, green = final path.",
    "<b>Statistics</b> — after each run the status bar shows the path length (in steps) and the total number of nodes visited.",
    "<b>Reset controls</b> — R resets the search while keeping walls; C clears the entire grid.",
    "<b>60 FPS rendering loop</b> powered by Pygame for smooth interaction.",
]
for f in features:
    story.append(bullet(f))

# ── 5. Code Architecture ─────────────────────────────────────────────────────
story.append(h1("5. Code Architecture"))
story.append(body(
    "The project follows a clean separation-of-concerns design split across six modules:"
))

arch_data = [
    ["Module", "Responsibility"],
    ["node.py", "Node class — stores per-cell state: wall, start, goal, visited, parent, g_cost."],
    ["grid.py", "Grid class — 2-D array of Nodes; provides get_neighbors(), set_start/goal(), reset helpers."],
    ["algorithms/bfs.py", "BFS implementation using collections.deque; calls draw_callback at each step."],
    ["algorithms/dfs.py", "Iterative DFS using a list-as-stack; same step-callback interface as BFS."],
    ["algorithms/dijkstra.py", "Dijkstra using heapq min-heap; tracks g_cost per node."],
    ["visualizer.py", "Pygame rendering — draws cells, panel, buttons, legend, and status bar."],
    ["main.py", "Entry point — event loop, keyboard/mouse handling, algorithm runner with animation."],
    ["utils.py", "Helper: maps algorithm name to function; event-handling during animation."],
]
arch_table = Table(
    [[Paragraph(cell, ParagraphStyle("TH", parent=body_style,
                                      fontName="Helvetica-Bold",
                                      textColor=colors.white if i == 0 else colors.HexColor("#2c2c2c")))
      if (i == 0) else Paragraph(cell, body_style)
      for cell in row]
     for i, row in enumerate(arch_data)],
    colWidths=[4 * cm, W - 4 * cm],
)
# Re-build with proper header
arch_rows_formatted = []
for i, row in enumerate(arch_data):
    if i == 0:
        arch_rows_formatted.append([
            Paragraph(cell, ParagraphStyle("TH", parent=body_style,
                                           fontName="Helvetica-Bold",
                                           textColor=colors.white))
            for cell in row
        ])
    else:
        arch_rows_formatted.append([
            Paragraph(row[0], ParagraphStyle("TCode", parent=body_style, fontName="Courier", fontSize=9)),
            Paragraph(row[1], body_style),
        ])
arch_table = Table(arch_rows_formatted, colWidths=[4 * cm, W - 4 * cm])
arch_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f3460")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9f9ff"), colors.HexColor("#eef4ff")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccccdd")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(arch_table)

story.append(h2("5.1 Algorithm Step-Callback Pattern"))
story.append(body(
    "All three algorithms share a uniform interface: they accept a <i>draw_callback(visited, "
    "frontier, path)</i> function. Each iteration appends a snapshot to a <i>steps</i> list. "
    "After the search completes, <tt>main.py</tt> replays these snapshots through Pygame "
    "with a 5 ms delay between frames, decoupling the algorithm logic from the rendering loop."
))

story.append(h2("5.2 Path Reconstruction"))
story.append(body(
    "Every algorithm sets a <tt>parent</tt> pointer on each visited node. Once the goal is "
    "reached, <tt>reconstruct_path(goal)</tt> follows parent links back to the start, "
    "producing the final path list. The visualiser then animates the path cell by cell "
    "with a 30 ms delay per step."
))

# ── 6. How to Run ────────────────────────────────────────────────────────────
story.append(h1("6. How to Run the Application"))
steps_run = [
    "Install dependencies: <tt>pip install pygame</tt>",
    "Clone or download the repository.",
    "Navigate to the project directory and run: <tt>python main.py</tt>",
    "Press <b>S</b> to enter Start mode, click a cell to place the start node.",
    "Press <b>G</b> to enter Goal mode, click a cell to place the goal node.",
    "Press <b>W</b> (default) to draw walls by clicking/dragging.",
    "Select an algorithm with keys <b>1</b> (BFS), <b>2</b> (DFS), or <b>3</b> (Dijkstra).",
    "Press <b>SPACE</b> to start the search and watch the animation.",
    "Press <b>R</b> to reset the search, <b>C</b> to clear the entire grid.",
]
for i, step in enumerate(steps_run, 1):
    story.append(Paragraph(f"{i}. {step}", bullet_style))

# ── 7. Results & Observations ────────────────────────────────────────────────
story.append(h1("7. Results &amp; Observations"))
obs = [
    "<b>BFS</b> consistently finds the shortest path and explores nodes in a systematic wave pattern radiating from the start.",
    "<b>DFS</b> often finds a path quickly but it is rarely the shortest; it dives deep into one branch before backtracking, which can be seen visually as long, winding exploration.",
    "<b>Dijkstra</b> produces results identical to BFS on this uniform-cost grid, confirming the theoretical equivalence. The purple colour differentiates it visually.",
    "In open grids (no walls) BFS and Dijkstra visit significantly fewer nodes than DFS.",
    "Complex maze-like wall configurations highlight the backtracking nature of DFS most clearly.",
]
for o in obs:
    story.append(bullet(o))

# ── 8. Links ─────────────────────────────────────────────────────────────────
story.append(h1("8. Project Links"))
story.append(sp(4))

links_data = [
    ["GitHub Repository", "https://github.com/beriloztan/graphs-algorithms",
     "Source code, all modules, and version history."],
    ["Demo Video (YouTube)", "https://youtu.be/_DrxCjlE78g",
     "Screen recording demonstrating BFS, DFS and Dijkstra in action (max 2 min)."],
]
links_rows = [
    [
        Paragraph("<b>GitHub Repository</b>", body_style),
        Paragraph(
            '<a href="https://github.com/beriloztan/graphs-algorithms" color="blue">'
            'github.com/beriloztan/graphs-algorithms</a>', link_style),
        Paragraph("Source code, all modules, and version history.", body_style),
    ],
    [
        Paragraph("<b>Demo Video (YouTube)</b>", body_style),
        Paragraph(
            '<a href="https://youtu.be/_DrxCjlE78g" color="blue">'
            'youtu.be/_DrxCjlE78g</a>', link_style),
        Paragraph("Screen recording demonstrating BFS, DFS and Dijkstra in action (max 2 min).", body_style),
    ],
]
links_table = Table(
    links_rows,
    colWidths=[4 * cm, 6.5 * cm, W - 10.5 * cm],
)
links_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef4ff")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#3a86ff")),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(links_table)

# ── 9. Conclusion ────────────────────────────────────────────────────────────
story.append(h1("9. Conclusion"))
story.append(body(
    "This project successfully implements and visualises three fundamental AI search "
    "algorithms — BFS, DFS, and Dijkstra's — within an interactive Pygame application. "
    "The implementation demonstrates the theoretical differences between the algorithms "
    "in a concrete, observable way: BFS and Dijkstra produce optimal paths via systematic "
    "level-order exploration, while DFS quickly dives deep at the cost of optimality."
))
story.append(body(
    "The modular architecture cleanly separates data modelling (Node, Grid), algorithm "
    "logic (algorithms/), rendering (Visualizer), and application flow (main.py). "
    "The step-callback animation pattern allows any future algorithm to be plugged in "
    "with minimal changes, making the codebase easily extensible."
))
story.append(body(
    "Overall, the project bridges theoretical knowledge and practical implementation, "
    "fulfilling the objectives of the Applied Programming Project assignment."
))

story.append(sp(20))
story.append(hr())
story.append(Paragraph(
    "Artificial Intelligence in Action — Applied Programming Project &nbsp;|&nbsp; "
    "Search &amp; Pathfinding Visualizer",
    ParagraphStyle("Footer", parent=body_style, fontSize=8,
                   textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
))

# ── Build ────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved to: {OUTPUT}")
