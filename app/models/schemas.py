"""
Cosmic Graph Intelligence - 핵심 데이터 스키마

노드, 엣지, 클러스터, 메모리 등 CGI 파이프라인의
모든 데이터 구조를 정의한다.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# 노드
# ──────────────────────────────────────────────
class CosmicNode(BaseModel):
    """개념 노드 — 하나의 지식/개념 단위."""

    id: str
    name: str
    type: str = "concept"  # technology, concept, data, goal, ...
    mass: float = 0.5  # 중요도 (0‒1)
    energy: float = 0.5  # 활성도 (0‒1)
    embedding: list[float] = Field(default_factory=list)
    state: str = "active"  # active|orbiting|dormant|escaped|garbage|compressed
    description: str = ""
    metadata: dict = Field(default_factory=dict)

    # Pruner 점수 — 파이프라인 실행 중 계산
    immediate_utility: float = 0.0
    creative_potential: float = 0.0
    noise_risk: float = 0.0
    memory_bonus: float = 0.0
    survival_score: float = 0.0


# ──────────────────────────────────────────────
# 엣지
# ──────────────────────────────────────────────
class CosmicEdge(BaseModel):
    """두 노드 사이의 관계."""

    source: str
    target: str
    weight: float = 0.0
    attraction: float = 0.0
    repulsion: float = 0.0
    entanglement_score: float = 0.0
    edge_type: str = "semantic"  # semantic | wormhole | binary


# ──────────────────────────────────────────────
# 클러스터 / 쌍성계
# ──────────────────────────────────────────────
class BinarySystem(BaseModel):
    """안정적으로 결합한 두 노드 조합."""

    binary_id: str
    nodes: list[str]
    stability: float
    role: str = ""


class CosmicCluster(BaseModel):
    """여러 노드의 그룹."""

    id: str
    node_ids: list[str]
    stability: float = 0.0
    role: str = ""
    summary: str = ""


# ──────────────────────────────────────────────
# 프루닝 결정
# ──────────────────────────────────────────────
class PruningDecision(BaseModel):
    """Escape Node Pruner의 판정 결과."""

    node_id: str
    node_name: str = ""
    previous_state: str = "active"
    next_state: str = "active"
    immediate_utility: float = 0.0
    creative_potential: float = 0.0
    noise_risk: float = 0.0
    memory_bonus: float = 0.0
    survival_score: float = 0.0
    reason: str = ""


# ──────────────────────────────────────────────
# 입력 분석 결과
# ──────────────────────────────────────────────
class InputAnalysis(BaseModel):
    """Input Analyzer의 출력."""

    intent: str = "general"
    keywords: list[str] = Field(default_factory=list)
    domain: list[str] = Field(default_factory=list)
    output_type: str = "text"
    original_input: str = ""
