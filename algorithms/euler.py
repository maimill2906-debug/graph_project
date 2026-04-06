"""
Euler Path / Cycle
- Hierholzer algorithm
- Fleury algorithm
Tách từ graph_gui.py :: GraphApp.handle_euler_hierholzer() & handle_euler_fleury()
"""


def euler_hierholzer(graph: dict, start=None):
    """
    Tìm đường/chu trình Euler bằng thuật toán Hierholzer.

    Args:
        graph: undirected adjacency list dạng dict.
               Ví dụ: {'A': ['B','C'], 'B': ['A','C'], 'C': ['A','B']}
        start: node bắt đầu. Nếu None → chọn tự động.

    Returns:
        Danh sách node theo thứ tự đường/chu trình Euler.
        Trả về [] nếu đồ thị không có đường/chu trình Euler.
    """
    if not graph:
        return []

    # Kiểm tra điều kiện Euler
    odd_degree = [n for n in graph if len(graph[n]) % 2 == 1]
    if len(odd_degree) not in (0, 2):
        return []

    if start is None or start not in graph:
        start = odd_degree[0] if odd_degree else next(iter(graph))

    # Copy adjacency list để không làm thay đổi graph gốc
    adj = {u: list(v_list) for u, v_list in graph.items()}

    stack = [start]
    circuit = []

    while stack:
        u = stack[-1]
        if adj.get(u):
            v = adj[u].pop()
            if u in adj.get(v, []):
                adj[v].remove(u)
            stack.append(v)
        else:
            circuit.append(stack.pop())

    circuit.reverse()
    return circuit


def euler_fleury(graph: dict, start=None):
    """
    Tìm đường/chu trình Euler bằng thuật toán Fleury (ưu tiên cạnh không phải cầu).

    Args:
        graph: undirected adjacency list dạng dict.
        start: node bắt đầu. Nếu None → chọn tự động.

    Returns:
        Danh sách node theo thứ tự đường/chu trình Euler.
        Trả về [] nếu đồ thị không có đường/chu trình Euler.
    """
    if not graph:
        return []

    odd_degree = [n for n in graph if len(graph[n]) % 2 == 1]
    if len(odd_degree) not in (0, 2):
        return []

    if start is None or start not in graph:
        start = odd_degree[0] if odd_degree else next(iter(graph))

    adj = {u: list(v_list) for u, v_list in graph.items()}

    def _dfs_count(node, visited, adjacency):
        visited.add(node)
        for t in adjacency.get(node, []):
            if t not in visited:
                _dfs_count(t, visited, adjacency)

    def is_bridge(u, v):
        if len(adj.get(u, [])) == 1:
            return False
        visited1 = set()
        _dfs_count(u, visited1, adj)

        adj[u].remove(v)
        if v in adj:
            adj[v].remove(u)

        visited2 = set()
        _dfs_count(u, visited2, adj)

        adj[u].append(v)
        if v in adj:
            adj[v].append(u)

        return len(visited2) < len(visited1)

    path = [start]
    current = start

    while adj.get(current):
        next_v = None
        for v in adj[current]:
            if not is_bridge(current, v):
                next_v = v
                break
        if next_v is None:
            next_v = adj[current][0]

        adj[current].remove(next_v)
        if current in adj.get(next_v, []):
            adj[next_v].remove(current)

        path.append(next_v)
        current = next_v

    return path
