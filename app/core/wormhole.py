"""
Cosmic Graph Intelligence - Wormhole Shortcut Generator

서로 멀리 떨어져 있지만, 연결하면 창의적 결과를 만들 수 있는
노드들을 연결하는 shortcut edge를 생성한다.
"""

from __future__ import annotations

import networkx as nx

from app.core.attraction import cosine_similarity
from app.models.schemas import CosmicEdge, CosmicNode
from app.utils.logger import get_logger

log = get_logger("wormhole")


def generate_wormhole_shortcuts(
    G: nx.Graph,
    nodes: list[CosmicNode],
    *,
    max_wormholes: int = 5,
) -> list[CosmicEdge]:
    """
    그래프에서 직접 연결이 약하지만 창의적 잠재력이 높은 노드 쌍을
    찾아 웜홀 shortcut edge를 생성한다.

    선택 기준:
    1. 그래프에서 직접 연결이 없거나 weight가 낮은 노드 쌍
    2. 하나 이상이 dormant_wormhole_candidate 상태
    3. 두 노드의 creative_potential 합이 높음
    4. noise_risk 합이 낮음
    """
    node_map = {n.id: n for n in nodes}

    # active 또는 orbiting 노드
    core_nodes = [n for n in nodes if n.state in ("active", "orbiting")]
    # dormant 웜홀 후보
    dormant_nodes = [n for n in nodes if n.state == "dormant_wormhole_candidate"]

    if not core_nodes or not dormant_nodes:
        log.info("웜홀 후보 없음 (core=%d, dormant=%d)", len(core_nodes), len(dormant_nodes))
        return []

    candidates: list[tuple[CosmicNode, CosmicNode, float]] = []

    for core in core_nodes:
        for dormant in dormant_nodes:
            # 이미 강하게 연결되어 있으면 스킵
            if G.has_edge(core.id, dormant.id):
                edge_data = G[core.id][dormant.id]
                if edge_data.get("weight", 0) > 0.3:
                    continue

            # 웜홀 점수 계산
            creative_sum = core.creative_potential + dormant.creative_potential
            noise_penalty = (core.noise_risk + dormant.noise_risk) / 2.0

            # 적당한 거리(너무 가깝지도 멀지도 않은)의 노드가 좋은 웜홀
            if core.embedding and dormant.embedding:
                sim = cosine_similarity(core.embedding, dormant.embedding)
                sim_norm = max(0.0, (sim + 1.0) / 2.0)
                # 0.3~0.6 거리가 최적
                distance_bonus = 1.0 - abs(sim_norm - 0.45) * 2.0
                distance_bonus = max(0.0, distance_bonus)
            else:
                distance_bonus = 0.5

            wormhole_score = creative_sum * distance_bonus - noise_penalty
            if wormhole_score > 0.2:
                candidates.append((core, dormant, wormhole_score))

    # 점수 내림차순 정렬 후 상위 N개 선택
    candidates.sort(key=lambda x: x[2], reverse=True)
    selected = candidates[:max_wormholes]

    wormhole_edges: list[CosmicEdge] = []
    for core, dormant, score in selected:
        edge = CosmicEdge(
            source=core.id,
            target=dormant.id,
            weight=round(score, 4),
            attraction=round(score, 4),
            repulsion=0.0,
            edge_type="wormhole",
        )
        wormhole_edges.append(edge)

        # 그래프에도 추가
        G.add_edge(
            core.id,
            dormant.id,
            weight=score,
            edge_type="wormhole",
        )

        log.info(
            "웜홀 생성: %s ↔ %s (score=%.3f)",
            core.name,
            dormant.name,
            score,
        )

    log.info("웜홀 총 %d개 생성", len(wormhole_edges))
    return wormhole_edges
