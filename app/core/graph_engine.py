"""
Cosmic Graph Intelligence - Graph Engine

노드와 엣지로 구성된 그래프를 생성하고 관리한다.
NetworkX를 기반으로 attraction/repulsion을 계산하여 edge weight를 결정한다.
"""

from __future__ import annotations

import networkx as nx

from app.core.attraction import calculate_attraction
from app.core.repulsion import calculate_repulsion
from app.models.config import get_settings
from app.models.schemas import CosmicEdge, CosmicNode
from app.utils.logger import get_logger

log = get_logger("graph_engine")


def build_graph(nodes: list[CosmicNode]) -> tuple[nx.Graph, list[CosmicEdge]]:
    """
    노드 목록으로부터 가중 그래프를 생성한다.

    모든 노드 쌍에 대해 attraction - repulsion을 계산하고,
    threshold 이상인 엣지만 유지한다.
    """
    settings = get_settings()
    G = nx.Graph()
    edges: list[CosmicEdge] = []

    # 노드 추가
    for node in nodes:
        G.add_node(node.id, name=node.name, type=node.type, mass=node.mass)

    # 엣지 계산
    n = len(nodes)
    log.info("엣지 계산 시작: %d개 노드 → %d 쌍", n, n * (n - 1) // 2)

    for i in range(n):
        for j in range(i + 1, n):
            node_i = nodes[i]
            node_j = nodes[j]

            attraction = calculate_attraction(node_i, node_j)
            repulsion = calculate_repulsion(node_i, node_j)
            weight = attraction - repulsion

            if weight > settings.min_edge_threshold:
                G.add_edge(
                    node_i.id,
                    node_j.id,
                    weight=weight,
                    attraction=attraction,
                    repulsion=repulsion,
                )

                edge = CosmicEdge(
                    source=node_i.id,
                    target=node_j.id,
                    weight=round(weight, 4),
                    attraction=attraction,
                    repulsion=repulsion,
                    edge_type="semantic",
                )
                edges.append(edge)

    log.info("그래프 생성 완료: 노드=%d, 엣지=%d", G.number_of_nodes(), G.number_of_edges())
    return G, edges
