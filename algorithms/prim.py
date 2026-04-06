"""
Prim — Minimum Spanning Tree
Tách từ graph_gui.py :: GraphApp.handle_prim()
"""
import heapq


def prim(graph: dict, start=None):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Prim.

    Args:
        graph: weighted adjacency list dạng dict (undirected).
               Ví dụ: {'A': [('B', 2), ('C', 5)], 'B': [('A', 2)], ...}
        start: node bắt đầu. Nếu None → chọn node đầu tiên trong graph.

    Returns:
        (mst_edges, total_weight)
        mst_edges: danh sách tuple (u, v, weight) các cạnh trong MST.
        total_weight: tổng trọng số MST.
        Trả về ([], 0) nếu graph rỗng.
    """
    if not graph:
        return [], 0

    if start is None or start not in graph:
        start = next(iter(graph))

    visited = {start}
    heap = []
    for v, w in graph.get(start, []):
        heapq.heappush(heap, (w, start, v))

    mst_edges = []
    total_weight = 0

    while heap:
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w
        for x, w2 in graph.get(v, []):
            if x not in visited:
                heapq.heappush(heap, (w2, v, x))

    return mst_edges, total_weight
