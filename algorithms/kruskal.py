"""
Kruskal — Minimum Spanning Tree
Tách từ graph_gui.py :: GraphApp.handle_kruskal()
"""


def kruskal(graph: dict):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Kruskal với Union-Find.

    Args:
        graph: weighted adjacency list dạng dict (undirected).
               Ví dụ: {'A': [('B', 2), ('C', 5)], 'B': [('A', 2)], ...}

    Returns:
        (mst_edges, total_weight)
        mst_edges: danh sách tuple (u, v, weight) các cạnh trong MST.
        total_weight: tổng trọng số MST.
        Trả về ([], 0) nếu graph rỗng.
    """
    if not graph:
        return [], 0

    # Thu thập tất cả cạnh (tránh trùng lặp với undirected graph)
    seen_edges = set()
    edges = []
    for u, neighbors in graph.items():
        for v, w in neighbors:
            key = tuple(sorted([u, v]))
            if key not in seen_edges:
                seen_edges.add(key)
                edges.append((w, u, v))
    edges.sort()

    # Union-Find
    parent = {n: n for n in graph}
    rank   = {n: 0  for n in graph}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True

    mst_edges = []
    total_weight = 0

    for w, u, v in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w

    return mst_edges, total_weight
