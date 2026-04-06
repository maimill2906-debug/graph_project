"""
test_manual.py — Test tay (baseline) viết bởi nhóm
Dùng để so sánh với test sinh bởi CodiumAI ở mục 5.3
Chạy: pytest tests/test_manual.py -v --tb=short
"""
import pytest
from algorithms.bfs import bfs_traversal, bfs_shortest_path
from algorithms.dfs import dfs_traversal, dfs_path
from algorithms.dijkstra import dijkstra
from algorithms.prim import prim
from algorithms.kruskal import kruskal
from algorithms.euler import euler_hierholzer, euler_fleury
from algorithms.ford_fulkerson import ford_fulkerson
from algorithms.bipartite import check_bipartite
from algorithms.graph_utils import adjacency_list_to_matrix, get_edge_list


# ══════════════════════════════════════════════════════════════
# BFS
# ══════════════════════════════════════════════════════════════
class TestBFS:
    def test_bfs_basic(self):
        """Đồ thị liên thông đơn giản"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}
        result = bfs_traversal(graph, 'A')
        assert result[0] == 'A'
        assert set(result) == {'A', 'B', 'C', 'D'}

    def test_bfs_single_node(self):
        """Đồ thị chỉ có 1 node, không có cạnh"""
        graph = {'A': []}
        assert bfs_traversal(graph, 'A') == ['A']

    def test_bfs_start_not_in_graph(self):
        """Node bắt đầu không tồn tại"""
        graph = {'A': ['B'], 'B': ['A']}
        assert bfs_traversal(graph, 'Z') == []

    def test_bfs_disconnected(self):
        """Đồ thị không liên thông — chỉ duyệt thành phần chứa start"""
        graph = {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']}
        result = bfs_traversal(graph, 'A')
        assert set(result) == {'A', 'B'}
        assert 'C' not in result

    def test_bfs_shortest_path_exists(self):
        """Đường đi tồn tại"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D'], 'D': ['B', 'C']}
        path = bfs_shortest_path(graph, 'A', 'D')
        assert path[0] == 'A' and path[-1] == 'D'
        assert len(path) == 3  # A → B → D hoặc A → C → D

    def test_bfs_shortest_path_no_path(self):
        """Không có đường đi"""
        graph = {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']}
        assert bfs_shortest_path(graph, 'A', 'C') == []

    def test_bfs_shortest_path_same_node(self):
        """Start == End"""
        graph = {'A': ['B'], 'B': ['A']}
        assert bfs_shortest_path(graph, 'A', 'A') == ['A']


# ══════════════════════════════════════════════════════════════
# DFS
# ══════════════════════════════════════════════════════════════
class TestDFS:
    def test_dfs_basic(self):
        """Đồ thị liên thông đơn giản"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}
        result = dfs_traversal(graph, 'A')
        assert result[0] == 'A'
        assert set(result) == {'A', 'B', 'C', 'D'}

    def test_dfs_single_node(self):
        graph = {'A': []}
        assert dfs_traversal(graph, 'A') == ['A']

    def test_dfs_start_not_in_graph(self):
        graph = {'A': ['B'], 'B': ['A']}
        assert dfs_traversal(graph, 'X') == []

    def test_dfs_path_exists(self):
        graph = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}
        path = dfs_path(graph, 'A', 'D')
        assert path[0] == 'A' and path[-1] == 'D'

    def test_dfs_path_no_path(self):
        graph = {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']}
        assert dfs_path(graph, 'A', 'D') == []


# ══════════════════════════════════════════════════════════════
# DIJKSTRA
# ══════════════════════════════════════════════════════════════
class TestDijkstra:
    def test_dijkstra_basic(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }
        dist, path = dijkstra(graph, 'A', 'D')
        assert dist == 4   # A→B→C→D = 1+2+1
        assert path == ['A', 'B', 'C', 'D']

    def test_dijkstra_no_path(self):
        graph = {'A': [('B', 1)], 'B': [('A', 1)], 'C': []}
        dist, path = dijkstra(graph, 'A', 'C')
        assert dist == float('inf')
        assert path == []

    def test_dijkstra_same_node(self):
        graph = {'A': [('B', 2)], 'B': [('A', 2)]}
        dist, path = dijkstra(graph, 'A', 'A')
        assert dist == 0

    def test_dijkstra_negative_weight_raises(self):
        graph = {'A': [('B', -1)], 'B': [('A', -1)]}
        with pytest.raises(ValueError):
            dijkstra(graph, 'A', 'B')

    def test_dijkstra_all_distances(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2)],
            'C': []
        }
        dist = dijkstra(graph, 'A')
        assert dist['A'] == 0
        assert dist['B'] == 1
        assert dist['C'] == 3


# ══════════════════════════════════════════════════════════════
# PRIM
# ══════════════════════════════════════════════════════════════
class TestPrim:
    def test_prim_basic(self):
        graph = {
            'A': [('B', 2), ('C', 3)],
            'B': [('A', 2), ('C', 1), ('D', 4)],
            'C': [('A', 3), ('B', 1), ('D', 5)],
            'D': [('B', 4), ('C', 5)]
        }
        edges, total = prim(graph, 'A')
        assert len(edges) == 3          # MST có n-1 = 3 cạnh
        assert total == 7               # 2 + 1 + 4 = 7

    def test_prim_empty_graph(self):
        assert prim({}) == ([], 0)

    def test_prim_single_node(self):
        edges, total = prim({'A': []}, 'A')
        assert edges == []
        assert total == 0


# ══════════════════════════════════════════════════════════════
# KRUSKAL
# ══════════════════════════════════════════════════════════════
class TestKruskal:
    def test_kruskal_basic(self):
        graph = {
            'A': [('B', 2), ('C', 3)],
            'B': [('A', 2), ('C', 1), ('D', 4)],
            'C': [('A', 3), ('B', 1), ('D', 5)],
            'D': [('B', 4), ('C', 5)]
        }
        edges, total = kruskal(graph)
        assert len(edges) == 3
        assert total == 7

    def test_kruskal_empty(self):
        assert kruskal({}) == ([], 0)

    def test_kruskal_same_result_as_prim(self):
        """Prim và Kruskal phải cho cùng tổng trọng số MST"""
        graph = {
            'A': [('B', 4), ('C', 2)],
            'B': [('A', 4), ('C', 1), ('D', 5)],
            'C': [('A', 2), ('B', 1), ('D', 8)],
            'D': [('B', 5), ('C', 8)]
        }
        _, total_prim    = prim(graph, 'A')
        _, total_kruskal = kruskal(graph)
        assert total_prim == total_kruskal


# ══════════════════════════════════════════════════════════════
# EULER
# ══════════════════════════════════════════════════════════════
class TestEuler:
    def test_hierholzer_cycle(self):
        """Đồ thị có chu trình Euler (tất cả bậc chẵn)"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}
        result = euler_hierholzer(graph, 'A')
        assert result[0] == result[-1]      # chu trình: đầu == cuối
        assert len(result) == 4             # 3 cạnh → 4 node trong list

    def test_hierholzer_no_euler(self):
        """Đồ thị không có đường/chu trình Euler"""
        graph = {'A': ['B', 'C', 'D'], 'B': ['A'], 'C': ['A'], 'D': ['A']}
        assert euler_hierholzer(graph) == []

    def test_fleury_path(self):
        """Đồ thị có đường Euler (đúng 2 node bậc lẻ)"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'C', 'D'], 'C': ['A', 'B'], 'D': ['B']}
        result = euler_fleury(graph, 'A')
        assert len(result) >= 2


# ══════════════════════════════════════════════════════════════
# FORD-FULKERSON
# ══════════════════════════════════════════════════════════════
class TestFordFulkerson:
    def test_basic_flow(self):
        graph = {
            'S': [('A', 10), ('B', 5)],
            'A': [('T', 10)],
            'B': [('T', 10)],
            'T': []
        }
        max_flow, _ = ford_fulkerson(graph, 'S', 'T')
        assert max_flow == 15

    def test_no_path(self):
        graph = {'S': [], 'T': []}
        max_flow, paths = ford_fulkerson(graph, 'S', 'T')
        assert max_flow == 0

    def test_bottleneck(self):
        """Bottleneck giới hạn flow"""
        graph = {
            'S': [('A', 100)],
            'A': [('T', 1)],
            'T': []
        }
        max_flow, _ = ford_fulkerson(graph, 'S', 'T')
        assert max_flow == 1

    def test_invalid_nodes(self):
        graph = {'S': [('A', 5)], 'A': []}
        max_flow, _ = ford_fulkerson(graph, 'X', 'Y')
        assert max_flow == 0


# ══════════════════════════════════════════════════════════════
# BIPARTITE
# ══════════════════════════════════════════════════════════════
class TestBipartite:
    def test_is_bipartite(self):
        graph = {'A': ['C', 'D'], 'B': ['C', 'D'], 'C': ['A', 'B'], 'D': ['A', 'B']}
        is_bip, g0, g1 = check_bipartite(graph)
        assert is_bip is True
        assert set(g0 + g1) == {'A', 'B', 'C', 'D'}

    def test_not_bipartite(self):
        """Tam giác — không phải bipartite"""
        graph = {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}
        is_bip, _, _ = check_bipartite(graph)
        assert is_bip is False

    def test_empty_graph(self):
        is_bip, g0, g1 = check_bipartite({})
        assert is_bip is True

    def test_single_node(self):
        is_bip, _, _ = check_bipartite({'A': []})
        assert is_bip is True


# ══════════════════════════════════════════════════════════════
# GRAPH UTILS
# ══════════════════════════════════════════════════════════════
class TestGraphUtils:
    def test_adjacency_list_to_matrix(self):
        graph = {'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}
        nodes, matrix = adjacency_list_to_matrix(graph)
        idx = {n: i for i, n in enumerate(nodes)}
        assert matrix[idx['A']][idx['B']] == 1
        assert matrix[idx['B']][idx['A']] == 1
        assert matrix[idx['A']][idx['C']] == 0

    def test_get_edge_list_undirected(self):
        graph = {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        edges = get_edge_list(graph, directed=False)
        assert len(edges) == 2   # (A,B) và (A,C), không trùng lặp

    def test_get_edge_list_directed(self):
        graph = {'A': ['B'], 'B': ['A']}
        edges = get_edge_list(graph, directed=True)
        assert len(edges) == 2   # (A,B) và (B,A) là hai cạnh khác nhau
