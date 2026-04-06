"""
Check Bipartite Graph
Tách từ graph_gui.py :: GraphApp.handle_check_bipartite()
"""
from collections import deque


def check_bipartite(graph: dict):
    """
    Kiểm tra đồ thị có phải đồ thị hai phía (bipartite) không.

    Args:
        graph: adjacency list dạng dict (directed hoặc undirected).
               Ví dụ: {'A': ['B','C'], 'B': ['A'], 'C': ['A']}

    Returns:
        (is_bipartite, group0, group1)
        is_bipartite: True nếu là đồ thị hai phía, False nếu không phải.
        group0: danh sách node thuộc tập 0.
        group1: danh sách node thuộc tập 1.
        Nếu không phải bipartite → group0 = group1 = [].
    """
    if not graph:
        return True, [], []

    color = {}

    for start in graph:
        if start in color:
            continue
        color[start] = 0
        q = deque([start])

        while q:
            u = q.popleft()
            for v in graph.get(u, []):
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, [], []

    group0 = [n for n in color if color[n] == 0]
    group1 = [n for n in color if color[n] == 1]
    return True, group0, group1
