"""
Cosmic Graph Intelligence - Attraction Calculator

두 노드 사이의 끌림(연결 강도)을 계산한다.

attraction(i, j)
  = semantic_similarity(i, j)
  × importance(i)
  × importance(j)
  × complementarity(i, j)
"""

from __future__ import annotations

import numpy as np

from app.models.schemas import CosmicNode
from app.utils.logger import get_logger

log = get_logger("attraction")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """두 벡터의 코사인 유사도를 계산한다."""
    va = np.array(a)
    vb = np.array(b)
    dot = float(np.dot(va, vb))
    norm = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if norm == 0:
        return 0.0
    return dot / norm


def _complementarity(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """
    두 노드의 상호보완성을 계산한다.
    타입이 다르면 보완적일 가능성이 높다.
    """
    if node_i.type != node_j.type:
        return 0.8
    return 0.4


def calculate_attraction(node_i: CosmicNode, node_j: CosmicNode) -> float:
    """
    두 노드 사이의 끌림을 계산한다.

    attraction = similarity × importance_i × importance_j × complementarity
    """
    if not node_i.embedding or not node_j.embedding:
        return 0.0

    similarity = cosine_similarity(node_i.embedding, node_j.embedding)
    # similarity를 0‒1 범위로 정규화 (코사인 유사도는 -1~1이므로)
    similarity = max(0.0, (similarity + 1.0) / 2.0)

    importance_i = node_i.mass
    importance_j = node_j.mass
    comp = _complementarity(node_i, node_j)

    attraction = similarity * importance_i * importance_j * comp
    return round(attraction, 4)
