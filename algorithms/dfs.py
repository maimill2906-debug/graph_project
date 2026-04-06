"""
DFS — Depth-First Search
Tách từ graph_gui.py :: GraphApp.handle_dfs()
"""


def dfs_traversal(graph: dict, start) -> list:
    """
    Duyệt đồ thị theo thuật toán DFS (iterative, dùng stack).

    Args:
        graph: adjacency list dạng dict
        start: node bắt đầu

    Returns:
        Danh sách các node theo thứ tự DFS.
        Trả về [] nếu start không tồn tại trong graph.
    """
    if start not in graph:
        return []

    visited = []
    stack = [start]
    parent = {start: None}

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.append(u)

        neighbors = list(graph.get(u, []))
        neighbors.reverse()
        for v in neighbors:
            if v not in visited:
                if v not in parent:
                    parent[v] = u
                stack.append(v)

    return visited


def dfs_path(graph: dict, start, end) -> list:
    """
    Tìm đường đi từ start đến end bằng DFS.

    Args:
        graph: adjacency list dạng dict
        start: node bắt đầu
        end:   node đích

    Returns:
        Danh sách node trên đường đi [start, ..., end].
        Trả về [] nếu không tìm được đường đi hoặc start/end không hợp lệ.
    """
    if start not in graph or end not in graph:
        return []
    if start == end:
        return [start]

    visited = []
    stack = [start]
    parent = {start: None}

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.append(u)

        neighbors = list(graph.get(u, []))
        neighbors.reverse()
        for v in neighbors:
            if v not in visited:
                if v not in parent:
                    parent[v] = u
                stack.append(v)

    if end not in parent:
        return []

    path = []
    x = end
    while x is not None:
        path.append(x)
        x = parent[x]
    path.reverse()
    return path
