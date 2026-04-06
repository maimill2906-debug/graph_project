"""
Dijkstra — Shortest Path (non-negative weights)
Tách từ graph_gui.py :: GraphApp.handle_dijkstra()
"""
import heapq


def dijkstra(graph: dict, start, end=None):
    """
    Tìm đường đi ngắn nhất từ start đến tất cả các node (hoặc đến end)
    bằng thuật toán Dijkstra.

    Args:
        graph: weighted adjacency list dạng dict.
               Ví dụ: {'A': [('B', 2), ('C', 5)], 'B': [('A', 2), ('C', 1)], ...}
               Mỗi phần tử trong list là tuple (neighbor, weight).
        start: node bắt đầu
        end:   node đích (tuỳ chọn). Nếu None → trả về khoảng cách tới tất cả node.

    Returns:
        Nếu end được chỉ định:
            (dist, path) — dist là chi phí ngắn nhất (float),
                           path là danh sách node trên đường đi.
            Trả về (float('inf'), []) nếu không có đường đi.
        Nếu end=None:
            dict khoảng cách ngắn nhất từ start tới mọi node.

    Raises:
        ValueError: nếu đồ thị có cạnh trọng số âm.
    """
    # Kiểm tra trọng số âm
    for u, neighbors in graph.items():
        for v, w in neighbors:
            if w < 0:
                raise ValueError(f"Dijkstra không hỗ trợ trọng số âm (cạnh {u}-{v}, w={w})")

    if start not in graph:
        if end is not None:
            return float('inf'), []
        return {}

    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if end is not None and u == end:
            break
        for v, w in graph.get(u, []):
            new_dist = dist[u] + w
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    if end is None:
        return dist

    if dist.get(end, float('inf')) == float('inf'):
        return float('inf'), []

    path = []
    x = end
    while x is not None:
        path.append(x)
        x = prev[x]
    path.reverse()
    return dist[end], path
