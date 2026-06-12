"""
Cosmic Graph Intelligence - Black Hole Compressor

여러 노드, 클러스터, 쌍성계, 웜홀 연결의 정보를 압축하여
최종 LLM 추론에 사용할 context를 생성한다.
"""

from __future__ import annotations

from app.models.schemas import (
    BinarySystem,
    CosmicEdge,
    CosmicNode,
    InputAnalysis,
    PruningDecision,
)
from app.utils.logger import get_logger

log = get_logger("blackhole")


def compress_context(
    *,
    analysis: InputAnalysis,
    nodes: list[CosmicNode],
    decisions: list[PruningDecision],
    binaries: list[BinarySystem],
    wormhole_edges: list[CosmicEdge],
) -> str:
    """
    CGI 파이프라인의 모든 결과를 하나의 구조화된 context 문자열로 압축한다.
    이 context는 최종 LLM 호출 시 system prompt에 주입된다.
    """
    node_map = {n.id: n for n in nodes}

    # 상태별 노드 분류
    active = [d for d in decisions if d.next_state == "active"]
    orbiting = [d for d in decisions if d.next_state == "orbiting"]
    dormant = [d for d in decisions if d.next_state == "dormant_wormhole_candidate"]

    lines: list[str] = []

    # 1. 핵심 분석
    lines.append("## 입력 분석")
    lines.append(f"- 의도: {analysis.intent}")
    lines.append(f"- 핵심 키워드: {', '.join(analysis.keywords)}")
    lines.append(f"- 도메인: {', '.join(analysis.domain)}")
    lines.append("")

    # 2. 핵심 활성 노드
    lines.append("## 핵심 활성 노드 (Active)")
    for d in active:
        node = node_map.get(d.node_id)
        desc = node.description if node else ""
        lines.append(
            f"- **{d.node_name}** (유용성={d.immediate_utility:.2f}): {desc}"
        )
    lines.append("")

    # 3. 주변 후보 노드
    if orbiting:
        lines.append("## 주변 후보 노드 (Orbiting)")
        for d in orbiting:
            node = node_map.get(d.node_id)
            desc = node.description if node else ""
            lines.append(f"- {d.node_name}: {desc}")
        lines.append("")

    # 4. 쌍성계
    if binaries:
        lines.append("## 안정적 개념 조합 (쌍성계)")
        for b in binaries:
            lines.append(
                f"- {b.nodes[0]} + {b.nodes[1]} (안정성={b.stability:.2f}, 역할={b.role})"
            )
        lines.append("")

    # 5. 웜홀 연결 (창의적 shortcut)
    if wormhole_edges:
        lines.append("## 창의적 연결 (웜홀)")
        for edge in wormhole_edges:
            src_node = node_map.get(edge.source)
            tgt_node = node_map.get(edge.target)
            src_name = src_node.name if src_node else edge.source
            tgt_name = tgt_node.name if tgt_node else edge.target
            lines.append(
                f"- {src_name} ↔ {tgt_name} (연결 강도={edge.weight:.2f})"
            )
        lines.append("")

    # 6. 잠재적 아이디어 씨앗
    if dormant:
        lines.append("## 잠재적 아이디어 씨앗 (Dormant 웜홀 후보)")
        for d in dormant:
            node = node_map.get(d.node_id)
            desc = node.description if node else ""
            lines.append(
                f"- {d.node_name} (창의 잠재력={d.creative_potential:.2f}): {desc}"
            )
        lines.append("")

    # 7. 통합 지침
    lines.append("## 답변 생성 지침")
    lines.append("위의 구조화된 개념 그래프를 기반으로 답변을 생성해라.")
    lines.append("- 핵심 활성 노드를 중심으로 구체적인 답변을 구성해라.")
    lines.append("- 쌍성계 조합을 활용하여 실현 가능한 제안을 해라.")
    lines.append("- 웜홀 연결을 통해 예상치 못한 창의적 요소를 자연스럽게 포함해라.")
    lines.append("- 단순한 나열이 아니라, 노드 간 관계를 기반으로 통합된 아이디어를 제시해라.")

    context = "\n".join(lines)
    log.info("컨텍스트 압축 완료: %d자", len(context))
    return context
