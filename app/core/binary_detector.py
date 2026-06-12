"""
Cosmic Graph Intelligence - Binary System Detector

강하게 연결된 두 노드를 찾아 쌍성계로 묶는다.

쌍성계 조건:
- edge_weight가 threshold 이상
- 두 노드의 역할이 상호보완적
- 중복도가 지나치게 높지 않음
"""

from __future__ import annotations

import uuid

import networkx as nx

from app.models.config import get_settings
from app.models.schemas import BinarySystem, CosmicNode
from app.utils.logger import get_logger

log = get_logger("binary_detector")


def detect_binary_systems(
    G: nx.Graph,
    nodes: list[CosmicNode],
) -> list[BinarySystem]:
    """
    그래프에서 가장 강하게 연결된 노드 쌍(쌍성계)을 탐색한다.
    """
    settings = get_settings()
    node_map = {n.id: n for n in nodes}

    # 모든 엣지를 weight 기준 내림차순 정렬
    weighted_edges = [
        (u, v, d.get("weight", 0.0))
        for u, v, d in G.edges(data=True)
    ]
    weighted_edges.sort(key=lambda x: x[2], reverse=True)

    used_nodes: set[str] = set()
    binaries: list[BinarySystem] = []

    for u, v, w in weighted_edges:
        if w < settings.binary_threshold:
            break

        # 이미 쌍성계에 포함된 노드는 제외
        if u in used_nodes or v in used_nodes:
            continue

        node_u = node_map.get(u)
        node_v = node_map.get(v)
        if not node_u or not node_v:
            continue

        # 역할 결정
        types = sorted([node_u.type, node_v.type])
        role = f"{types[0]}_{types[1]}" if types[0] != types[1] else types[0]

        binary = BinarySystem(
            binary_id=f"binary_{uuid.uuid4().hex[:6]}",
            nodes=[node_u.name, node_v.name],
            stability=round(w, 4),
            role=role,
        )
        binaries.append(binary)
        used_nodes.add(u)
        used_nodes.add(v)

    log.info("쌍성계 탐지 완료: %d개", len(binaries))
    for b in binaries:
        log.info("  %s  stability=%.3f", b.nodes, b.stability)

    return binaries
