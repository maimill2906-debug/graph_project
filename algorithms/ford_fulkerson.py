"""
Ford-Fulkerson — Maximum Flow
Tách từ graph_gui.py :: GraphApp.handle_ford_fulkerson()
"""
from collections import deque


def ford_fulkerson(graph: dict, source, sink):
    """
    Tính luồng cực đại từ source đến sink bằng thuật toán Ford-Fulkerson
    (sử dụng BFS — Edmonds-Karp variant).

    Args:
        graph: weighted directed adjacency list dạng dict.
               Ví dụ: {'S': [('A', 10), ('B', 5)], 'A': [('T', 10)], ...}
               Mỗi phần tử là (neighbor, capacity).
        source: node nguồn
        sink:   node đích

    Returns:
        (max_flow, augmenting_paths)
        max_flow: giá trị luồng cực đại (int/float)
        augmenting_paths: danh sách các đường tăng luồng tìm được,
                          mỗi phần tử là list node.
        Trả về (0, []) nếu source hoặc sink không hợp lệ.
    """
    if source not in graph or sink not in graph:
        return 0, []

    # Xây dựng ma trận capacity từ adjacency list
    nodes = list(graph.keys())
    # Đảm bảo sink có trong nodes
    for u, neighbors in graph.items():
        for v, _ in neighbors:
            if v not in nodes:
                nodes.append(v)

    cap = {u: {v: 0 for v in nodes} for u in nodes}
    for u, neighbors in graph.items():
        for v, w in neighbors:
            cap[u][v] += w

    def bfs_find_path(parent):
        visited = {source}
        q = deque([source])
        while q:
            u = q.popleft()
            for v in nodes:
                if v not in visited and cap[u][v] > 0:
                    parent[v] = u
                    visited.add(v)
                    if v == sink:
                        return True
                    q.append(v)
        return False

    max_flow = 0
    augmenting_paths = []

    while True:
        parent = {}
        if not bfs_find_path(parent):
            break

        # Truy vết đường tăng
        path = []
        v = sink
        while v != source:
            path.append(v)
            v = parent[v]
        path.append(source)
        path.reverse()
        augmenting_paths.append(path)

        # Tính bottleneck
        bottleneck = min(cap[path[i]][path[i+1]] for i in range(len(path)-1))

        # Cập nhật residual graph
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            cap[u][v] -= bottleneck
            cap[v][u] += bottleneck

        max_flow += bottleneck

    return max_flow, augmenting_paths
