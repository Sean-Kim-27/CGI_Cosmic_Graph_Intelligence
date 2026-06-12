"""
Cosmic Graph Intelligence - Repulsion Calculator

두 노드 사이의 반발력(중복, 충돌, 모순)을 계산한다.

repulsion(i, j)
  = redundancy(i, j)
  + contradiction(i, j)
  + context_mismatch(i, j)
"""

from __future__ import annotations

from app.core.attraction import cosine_similarity
from app.models.schemas import CosmicNode
from app.utils.logger import get_logger

log = get_logger("repulsion")


def _redundancy(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """
    두 노드의 중복도를 계산한다.
    같은 타입이고 유사도가 매우 높으면 중복이다.
    """
    if node_i.type != node_j.type:
        return 0.0

    if not node_i.embedding or not node_j.embedding:
        return 0.0

    sim = cosine_similarity(node_i.embedding, node_j.embedding)
    sim_norm = max(0.0, (sim + 1.0) / 2.0)

    # 같은 타입의 노드가 유사도 0.85 이상이면 중복
    if sim_norm > 0.85:
        return (sim_norm - 0.85) * 5.0  # 0~0.75 범위
    return 0.0


def _contradiction(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """
    두 노드의 모순 정도를 계산한다.
    임베딩만으로는 모순 탐지가 어려우므로,
    간단한 휴리스틱으로 시작한다.
    """
    # MVP: 임베딩 유사도가 매우 낮고 같은 도메인이면 모순 가능성
    if not node_i.embedding or not node_j.embedding:
        return 0.0

    sim = cosine_similarity(node_i.embedding, node_j.embedding)
    sim_norm = max(0.0, (sim + 1.0) / 2.0)

    if sim_norm < 0.3 and node_i.type == node_j.type:
        return 0.2
    return 0.0


def _context_mismatch(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """문맥 불일치 정도. MVP에서는 최소화."""
    return 0.0


def calculate_repulsion(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """
    두 노드 사이의 반발력을 계산한다.

    repulsion = redundancy + contradiction + context_mismatch
    """
    redundancy = _redundancy(node_i, node_j)
    contradiction = _contradiction(node_i, node_j)
    mismatch = _context_mismatch(node_i, node_j)

    repulsion = redundancy + contradiction + mismatch
    return round(min(repulsion, 1.0), 4)
