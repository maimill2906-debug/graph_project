"""
BFS — Breadth-First Search
Tách từ graph_gui.py :: GraphApp.handle_bfs()
"""
from collections import deque


def bfs_traversal(graph: dict, start) -> list:
    """
    Duyệt đồ thị theo thuật toán BFS.

    Args:
        graph: adjacency list dạng dict, ví dụ {'A': ['B','C'], 'B': ['A'], ...}
        start: node bắt đầu

    Returns:
        Danh sách các node theo thứ tự BFS.
        Trả về [] nếu start không tồn tại trong graph.
    """
    if start not in graph:
        return []

    visited = []
    q = deque([start])
    seen = {start}

    while q:
        u = q.popleft()
        visited.append(u)
        for v in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)

    return visited


def bfs_shortest_path(graph: dict, start, end) -> list:
    """
    Tìm đường đi ngắn nhất (theo số cạnh) từ start đến end bằng BFS.

    Args:
        graph: adjacency list dạng dict
        start: node bắt đầu
        end:   node đích

    Returns:
        Danh sách node trên đường đi ngắn nhất [start, ..., end].
        Trả về [] nếu không có đường đi hoặc start/end không hợp lệ.
    """
    if start not in graph or end not in graph:
        return []
    if start == end:
        return [start]

    parent = {start: None}
    q = deque([start])

    while q:
        u = q.popleft()
        if u == end:
            break
        for v in graph.get(u, []):
            if v not in parent:
                parent[v] = u
                q.append(v)

    if end not in parent:
        return []

    path = []
    x = end
    while x is not None:
        path.append(x)
        x = parent[x]
    path.reverse()
    return path
