"""
Graph Utilities — Chuyển đổi biểu diễn đồ thị
Tách từ graph_gui.py :: GraphApp.handle_convert_representation()
"""


def adjacency_list_to_matrix(graph: dict, directed: bool = False):
    """
    Chuyển đổi từ danh sách kề sang ma trận kề.

    Args:
        graph:    adjacency list dạng dict (unweighted).
                  Ví dụ: {'A': ['B','C'], 'B': ['A'], 'C': ['A']}
        directed: True nếu đồ thị có hướng.

    Returns:
        (nodes, matrix)
        nodes:  danh sách các node (list)
        matrix: ma trận kề 2D (list of lists), giá trị 0/1
    """
    nodes = list(graph.keys())
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)

    matrix = [[0] * n for _ in range(n)]
    for u, neighbors in graph.items():
        for v in neighbors:
            if v in idx:
                matrix[idx[u]][idx[v]] = 1
                if not directed:
                    matrix[idx[v]][idx[u]] = 1

    return nodes, matrix


def adjacency_matrix_to_list(nodes: list, matrix: list, directed: bool = False):
    """
    Chuyển đổi từ ma trận kề sang danh sách kề.

    Args:
        nodes:    danh sách tên node
        matrix:   ma trận kề 2D
        directed: True nếu đồ thị có hướng

    Returns:
        adjacency list dạng dict
    """
    graph = {n: [] for n in nodes}
    n = len(nodes)
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                graph[nodes[i]].append(nodes[j])
                if not directed and nodes[j] not in graph[nodes[i]]:
                    pass  # đã thêm ở trên
    return graph


def get_edge_list(graph: dict, directed: bool = False):
    """
    Trả về danh sách cạnh từ adjacency list.

    Args:
        graph:    adjacency list dạng dict
        directed: True nếu đồ thị có hướng

    Returns:
        Danh sách tuple (u, v). Với undirected graph, mỗi cạnh chỉ xuất hiện 1 lần.
    """
    edges = []
    seen = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if directed:
                edges.append((u, v))
            else:
                key = tuple(sorted([u, v]))
                if key not in seen:
                    seen.add(key)
                    edges.append((u, v))
    return edges
