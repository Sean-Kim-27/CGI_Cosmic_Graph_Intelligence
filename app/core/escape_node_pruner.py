"""
Cosmic Graph Intelligence - Escape Node Pruner

노드의 즉시 유용성(Uᵢ), 창의적 잠재력(Cᵢ), 노이즈 위험(Nᵢ),
메모리 보너스(Mᵢ)를 계산하여 생존 상태를 결정한다.

상태 흐름: active → orbiting → dormant → escaped → garbage
"""

from __future__ import annotations

from app.core.attraction import cosine_similarity
from app.models.schemas import CosmicNode, InputAnalysis, PruningDecision
from app.utils.logger import get_logger

log = get_logger("pruner")

# ──────────────────────────────────────────────
# 모드별 파라미터
# ──────────────────────────────────────────────
MODE_PARAMS: dict[str, dict[str, float]] = {
    "accurate":  {"lambda": 0.80, "mu": 0.80, "eta": 0.20},
    "balanced":  {"lambda": 0.60, "mu": 0.65, "eta": 0.25},
    "creative":  {"lambda": 0.45, "mu": 0.55, "eta": 0.30},
    "research":  {"lambda": 0.40, "mu": 0.60, "eta": 0.35},
}

# 임계값
T_ACTIVE = 0.65
T_CREATIVE = 0.40
T_NOISE = 0.45
T_SURVIVAL = 0.35
T_GARBAGE_U = 0.25
T_GARBAGE_C = 0.20
T_GARBAGE_N = 0.60


# ──────────────────────────────────────────────
# 점수 계산
# ──────────────────────────────────────────────
def _compute_immediate_utility(
    node: CosmicNode,
    analysis: InputAnalysis,
    query_embedding: list[float],
) -> float:
    """Uᵢ — 현재 문제 해결에 직접 기여하는 정도."""
    if not node.embedding or not query_embedding:
        return node.mass

    sim = cosine_similarity(node.embedding, query_embedding)
    relevance = max(0.0, (sim + 1.0) / 2.0)

    task_usefulness = node.mass
    cluster_support = node.energy * 0.5
    user_pref = 0.1  # MVP: 기본값

    u = (
        0.45 * relevance
        + 0.25 * task_usefulness
        + 0.20 * cluster_support
        + 0.10 * user_pref
    )
    return round(min(u, 1.0), 4)


def _compute_creative_potential(
    node: CosmicNode,
    query_embedding: list[float],
) -> float:
    """Cᵢ — 웜홀 연결 가능성."""
    if not node.embedding or not query_embedding:
        return 0.3

    sim = cosine_similarity(node.embedding, query_embedding)
    sim_norm = max(0.0, (sim + 1.0) / 2.0)

    # 적당히 먼 거리(0.3~0.6)에 있는 노드가 창의적 잠재력이 높다
    if 0.3 <= sim_norm <= 0.6:
        cross_domain_distance = 0.8
    elif sim_norm < 0.3:
        cross_domain_distance = 0.4  # 너무 먼 것은 오히려 위험
    else:
        cross_domain_distance = 0.3  # 너무 가까우면 창의성 낮음

    novelty = 1.0 - sim_norm  # 관련도 낮을수록 novelty 높음
    bridge_potential = node.energy * 0.7
    reinterpretability = 0.3  # MVP: 기본값

    c = (
        0.30 * novelty
        + 0.25 * bridge_potential
        + 0.20 * cross_domain_distance
        + 0.15 * 0.0  # entanglement_memory (MVP: 0)
        + 0.10 * reinterpretability
    )
    return round(min(c, 1.0), 4)


def _compute_noise_risk(node: CosmicNode) -> float:
    """Nᵢ — 결과 품질을 떨어뜨릴 위험."""
    # mass가 낮고 energy도 낮으면 노이즈 위험 높음
    base_risk = max(0.0, 0.5 - (node.mass + node.energy) / 2.0)

    # 설명이 짧거나 없으면 low_explainability
    low_explain = 0.2 if len(node.description) < 10 else 0.0

    n = (
        0.35 * 0.0  # contradiction (MVP: 별도 계산 안 함)
        + 0.25 * 0.0  # redundancy (graph_engine에서 이미 처리)
        + 0.20 * base_risk  # hallucination_risk
        + 0.10 * 0.0  # context_mismatch
        + 0.10 * low_explain
    )
    return round(min(n, 1.0), 4)


# ──────────────────────────────────────────────
# 노드 분류
# ──────────────────────────────────────────────
def classify_nodes(
    nodes: list[CosmicNode],
    analysis: InputAnalysis,
    query_embedding: list[float],
    *,
    mode: str = "balanced",
) -> list[PruningDecision]:
    """
    모든 노드를 active/orbiting/dormant/escaped/garbage로 분류한다.
    """
    params = MODE_PARAMS.get(mode, MODE_PARAMS["balanced"])
    lam = params["lambda"]
    mu = params["mu"]
    eta = params["eta"]

    decisions: list[PruningDecision] = []

    for node in nodes:
        U = _compute_immediate_utility(node, analysis, query_embedding)
        C = _compute_creative_potential(node, query_embedding)
        N = _compute_noise_risk(node)
        M = 0.0  # MVP: 메모리 보너스 미구현

        S = lam * U + (1 - lam) * C - mu * N + eta * M

        # 상태 판정
        if U >= T_ACTIVE:
            state = "active"
            reason = f"즉시 유용성 높음 (U={U:.2f})"
        elif C >= T_CREATIVE and N <= T_NOISE:
            state = "dormant_wormhole_candidate"
            reason = f"창의적 잠재력 높음 (C={C:.2f}), 노이즈 낮음 (N={N:.2f})"
        elif S >= T_SURVIVAL:
            state = "orbiting"
            reason = f"생존 점수 충분 (S={S:.2f})"
        elif U < T_GARBAGE_U and C < T_GARBAGE_C and N > T_GARBAGE_N:
            state = "garbage"
            reason = f"유용성·창의성 부족, 노이즈 높음"
        else:
            state = "escaped"
            reason = f"현재 세션에서 제외 (S={S:.2f})"

        # 노드에 점수 기록
        node.immediate_utility = U
        node.creative_potential = C
        node.noise_risk = N
        node.memory_bonus = M
        node.survival_score = round(S, 4)
        node.state = state

        decisions.append(
            PruningDecision(
                node_id=node.id,
                node_name=node.name,
                previous_state="active",
                next_state=state,
                immediate_utility=U,
                creative_potential=C,
                noise_risk=N,
                memory_bonus=M,
                survival_score=round(S, 4),
                reason=reason,
            )
        )

    # 로그
    state_counts: dict[str, int] = {}
    for d in decisions:
        state_counts[d.next_state] = state_counts.get(d.next_state, 0) + 1
    log.info("프루닝 완료: %s", state_counts)

    return decisions
